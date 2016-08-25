from collections import Counter, defaultdict
from django.core.urlresolvers import reverse
from django.db import models, connection
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

from manoseimas.mps_v2.utils import is_state_actor
from manoseimas.utils import reify, dict_fetch_all, todate
from manoseimas.scrapy import models as scrapy_models

import manoseimas.common.utils.words as words_utils


class CrawledItem(models.Model):
    source = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def get_mp_full_name(mp):
    return mp.full_name


def get_mp_votes(source_id, start_date='2012-11-16', end_date=None):
    start_date = todate(start_date)
    end_date = todate(end_date)
    votes = scrapy_models.PersonVote.objects.filter(
        p_asm_id=source_id,
        timestamp__range=(start_date, end_date),
    )
    return votes


class ParliamentMember(CrawledItem):
    slug = AutoSlugField(populate_from=('first_name', 'last_name'),
                         max_length=120)
    source_id = models.CharField(max_length=16)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    candidate_page = models.URLField(blank=True, null=True)
    raised_by = models.ForeignKey('PoliticalParty', blank=True, null=True)
    photo = models.ImageField(upload_to='profile_images',
                              blank=True, null=True)
    term_of_office = models.CharField(max_length=32, blank=True, null=True)

    office_address = models.TextField(blank=True, null=True)
    constituency = models.CharField(max_length=128, blank=True, null=True)
    party_candidate = models.BooleanField(default=True)
    groups = models.ManyToManyField('Group', through='GroupMembership',
                                    related_name='members')

    biography = models.TextField(blank=True, null=True)

    # Precomputed stats fields
    statement_count = models.PositiveIntegerField(blank=True, null=True)
    long_statement_count = models.PositiveIntegerField(blank=True, null=True)
    vote_percentage = models.FloatField(blank=True, null=True)
    discussion_contribution_percentage = models.FloatField(blank=True,
                                                           null=True)
    positions = JSONField(default=None, blank=True, null=True)
    proposed_law_project_count = models.PositiveIntegerField(blank=True,
                                                             null=True)
    passed_law_project_count = models.PositiveIntegerField(blank=True,
                                                           null=True)
    passed_law_project_ratio = models.FloatField(blank=True, null=True)

    precomputed_fields = (
        ('statement_count', 'get_statement_count'),
        ('long_statement_count', 'get_long_statement_count'),
        ('vote_percentage', 'get_vote_percentage'),
        ('discussion_contribution_percentage',
         'get_discussion_contribution_percentage'),
        ('positions', 'get_positions'),
        ('proposed_law_project_count', 'get_proposed_law_project_count'),
        ('passed_law_project_count', 'get_passed_law_project_count'),
        ('passed_law_project_ratio', 'get_passed_law_project_ratio'),
    )
    precomputation_depends_on = ('StenogramStatement',)

    @property
    def full_name(self):
        return u' '.join([self.first_name, self.last_name])

    def __unicode__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('mp_profile', kwargs={'mp_slug': self.slug})

    @property
    def fractions(self):
        return self.groups.filter(type=Group.TYPE_FRACTION)

    @property
    def fraction(self):
        ''' Current parliamentarian's fraction. '''
        if getattr(self, '_fraction', None):
            return self._fraction[0].group
        else:
            membership = GroupMembership.objects.filter(
                member=self,
                group__type=Group.TYPE_FRACTION,
                until=None
            )[:]

            if membership:
                self._fraction = membership
                return membership[0].group
            else:
                return None

    def get_statement_count(self):
        return self.statements.filter(as_chairperson=False).count()

    def get_long_statement_count(self):
        return self.statements.filter(as_chairperson=False).\
            filter(word_count__gte=50).count()

    def get_long_statement_percentage(self):
        statements = self.get_statement_count()
        long_statements = self.get_long_statement_count()
        return (float(long_statements) / statements * 100
                if statements else 0.0)

    def get_discussion_contribution_percentage(self):
        all_discussions = StenogramTopic.objects.count()
        contributed_discusions = StenogramStatement.objects.\
            filter(speaker=self, as_chairperson=False).\
            aggregate(topics=models.Count('topic_id',
                                          distinct=True))
        return (float(contributed_discusions['topics'])
                / all_discussions * 100.0) if all_discussions else 0.0

    @property
    def votes(self):
        return get_mp_votes(self.source_id)

    def get_vote_percentage(self):
        votes = scrapy_models.PersonVote.objects.filter(p_asm_id=self.source_id).count()
        # Get total votes during the time MP was in fractions
        fraction_memberships = GroupMembership.objects.filter(
            member=self,
            group__type=Group.TYPE_FRACTION)
        total_votes = 0
        for membership in fraction_memberships:
            start_date = membership.since.isoformat()
            end_date = (membership.until.isoformat()
                        if membership.until else None)
            total_votes += (
                scrapy_models.Voting.objects.
                filter(timestamp__range=(start_date, end_date)).
                count()
            )
        if total_votes:
            vote_percentage = float(votes) / total_votes * 100.0
        else:
            vote_percentage = 0.0
        return vote_percentage

    def get_proposed_law_project_count(self):
        return self.law_projects.count()

    def get_passed_law_project_count(self):
        return self.law_projects.filter(date_passed__isnull=False).count()

    def get_passed_law_project_ratio(self):
        avg_passing_time = LawProject.get_avg_passing_time()
        proposed_count = self.get_proposed_law_project_count()
        proposed_count = self.law_projects.exclude(
            date_passed__isnull=True,
            date__gt=models.Func(models.Func(function='CURDATE'),
                                 models.Func(
                                     avg_passing_time,
                                     template='INTERVAL %(expressions)s DAY'),
                                 function='DATE_SUB')
        ).count()
        if proposed_count:
            return (float(self.get_passed_law_project_count())
                    / proposed_count * 100.0)
        else:
            return 0.0

    def get_positions(self):
        from manoseimas.compatibility_test import services
        term = services.get_term_range(self.term_of_office)
        positions = services.get_topic_positions(term)
        return positions['mps'].get(self.pk, {})

    def get_collaborators_qs(self):
        collaborators = ParliamentMember.objects.filter(
            law_projects__in=self.law_projects.all()
        ).exclude(
            pk=self.pk
        )
        return collaborators

    def get_top_collaborators(self, count=5):
        collaborators_qs = self.get_collaborators_qs()
        collaborators = collaborators_qs.annotate(
            project_count=models.Count('*')
        ).distinct().order_by('-project_count')[:count]
        return collaborators

    @property
    def top_collaborators(self):
        return self.get_top_collaborators()

    @property
    def all_statements(self):
        return self.statements.all()

    @classmethod
    def FractionPrefetch(cls):
        return models.Prefetch(
            'groupmembership',
            queryset=GroupMembership.objects.select_related('group').filter(
                until=None,
                group__type=Group.TYPE_FRACTION,
                group__displayed=True),
            to_attr='_fraction'
        )


class PoliticalParty(CrawledItem):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Group(CrawledItem):
    TYPE_GROUP = 'group'
    TYPE_COMMITTEE = 'committee'
    TYPE_COMMISSION = 'commission'
    TYPE_FRACTION = 'fraction'
    TYPE_PARLIAMENT = 'parliament'

    GROUP_TYPES = (
        (TYPE_GROUP, _('Group')),
        (TYPE_COMMITTEE, _('Committee')),
        (TYPE_COMMISSION, _('Commission')),
        (TYPE_FRACTION, _('Fraction')),
        (TYPE_PARLIAMENT, _('Parliament')),
    )

    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', max_length=120)
    abbr = models.CharField(max_length=16, blank=True, null=True)
    type = models.CharField(max_length=64,
                            choices=GROUP_TYPES)
    displayed = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='fraction_logos',
                             blank=True, null=True)

    # Precomputed stats fields
    avg_statement_count = models.FloatField(blank=True, null=True)
    avg_long_statement_count = models.FloatField(blank=True, null=True)
    avg_vote_percentage = models.FloatField(blank=True, null=True)
    avg_discussion_contribution_percentage = models.FloatField(blank=True,
                                                               null=True)
    positions = JSONField(default=None, blank=True, null=True)
    avg_law_project_count = models.FloatField(blank=True, null=True)
    avg_passed_law_project_count = models.FloatField(blank=True, null=True)
    avg_passed_law_project_ratio = models.FloatField(blank=True, null=True)

    precomputed_fields = (
        ('avg_statement_count', 'get_avg_statement_count'),
        ('avg_long_statement_count', 'get_avg_long_statement_count'),
        ('avg_vote_percentage', 'get_avg_vote_percentage'),
        ('avg_discussion_contribution_percentage',
         'get_avg_discussion_contribution_percentage'),
        ('positions', 'get_positions'),
        ('avg_law_project_count',
         'get_avg_proposed_law_project_count'),
        ('avg_passed_law_project_count',
         'get_avg_passed_law_project_count'),
        ('avg_passed_law_project_ratio',
         'get_avg_passed_law_project_ratio'),
    )
    precomputation_filter = {
        'type__in': (TYPE_FRACTION, TYPE_PARLIAMENT),
    }
    precomputation_depends_on = ('ParliamentMember',)

    class Meta:
        unique_together = (('name', 'type'))

    def __unicode__(self):
        return u'{} ({})'.format(self.name, self.type)

    @property
    def active_members(self):
        return self.members.filter(groupmembership__until=None)

    @reify
    def active_member_count(self):
        return self.active_members.count()

    def get_avg_statement_count(self):
        agg = self.active_members.filter(
            statements__as_chairperson=False,
        ).annotate(
            models.Count('statements')
        ).aggregate(
            avg_statements=models.Avg('statements__count')
        )
        return agg['avg_statements']

    def get_avg_long_statement_count(self):
        agg = self.active_members.filter(
            statements__word_count__gte=50,
            statements__as_chairperson=False,
        ).annotate(
            models.Count('statements')
        ).aggregate(
            avg_statements=models.Avg('statements__count')
        )
        return agg['avg_statements']

    def get_avg_vote_percentage(self):
        total_percentage = 0.0
        for member in self.active_members:
            total_percentage += member.vote_percentage
        return (total_percentage / self.active_member_count
                if self.active_member_count else 0.0)

    def get_avg_discussion_contribution_percentage(self):
        agg = self.active_members.aggregate(
            avg_contrib=models.Avg('discussion_contribution_percentage')
        )
        return agg['avg_contrib']

    def get_positions(self):
        from manoseimas.compatibility_test import services
        positions = services.get_topic_positions()  # XXX: parliament term should be passed here
        return positions['fractions'].get(self.pk, {})

    def get_avg_proposed_law_project_count(self):
        agg = self.active_members.annotate(
            models.Count('law_projects')
        ).aggregate(
            avg_law_projects=models.Avg('law_projects__count')
        )
        return agg['avg_law_projects']

    def get_avg_passed_law_project_count(self):
        agg = self.active_members.filter(
            law_projects__date_passed__isnull=False
        ).annotate(
            models.Count('law_projects')
        ).aggregate(
            avg_passed_projects=models.Avg('law_projects__count')
        )
        return agg['avg_passed_projects']

    def get_avg_passed_law_project_ratio(self):
        agg = self.active_members.aggregate(
            avg_passed_ratio=models.Avg('passed_law_project_ratio')
        )
        return agg['avg_passed_ratio']

    def get_collaborating_fractions_percentage(self, count=5):

        member_projects = LawProject.objects.filter(
            proposers__in=self.active_members
        )
        # Retrieve proposer counts for each pair of (project_id, group_id)
        # for all fraction member projects
        project_signatories = LawProject.proposers.through.objects.filter(
            parliamentmember__groups__type=Group.TYPE_FRACTION,
            parliamentmember__groupmembership__until__isnull=True,
            lawproject__id__in=list(
                member_projects.values_list('id', flat=True).distinct()),
        ).values(
            'lawproject__id',
            'parliamentmember__groups__id',
        ).annotate(group_proposer_count=models.Count('pk'))

        project_signatories = list(project_signatories)

        # Build a dict: project -> group_id -> count
        # for retrieved projects
        projects = defaultdict(lambda: {})
        for s in project_signatories:
            proposer_count = s['group_proposer_count']
            project_id = s['lawproject__id']
            group_id = s['parliamentmember__groups__id']
            projects[project_id][group_id] = proposer_count

        # Calculate contribution ratios for each project
        project_percentages = {}
        for project_id, fraction_signatures in projects.items():
            total_signatories = sum(fraction_signatures.values())
            signature_percentages = {
                fraction_id: float(value) / total_signatories * 100.0
                for fraction_id, value in fraction_signatures.items()
            }
            project_percentages[project_id] = signature_percentages

        # Sum up contribution ratios for each fraction
        fraction_contrib_sums = defaultdict(lambda: 0.0)
        fraction_contrib_projects = defaultdict(lambda: 0)
        for project in project_percentages.values():
            for fraction, percentage in project.items():
                if fraction != self.pk:  # Ignore own percentages
                    fraction_contrib_sums[fraction] += percentage
                    fraction_contrib_projects[fraction] += 1

        # Compute fraction average contribution ratios
        fraction_contrib = {key: (fraction_contrib_sums[key]
                                  / fraction_contrib_projects[key])
                            for key in fraction_contrib_sums.keys()}

        # Take top N contributing fractions and retrieve their data
        top_signatory_pairs = sorted(
            fraction_contrib.items(),
            reverse=True,
            key=lambda v: v[1],
        )
        top_signatory_dict = dict(top_signatory_pairs[:count])
        top_signatories = list(Group.objects.filter(
            pk__in=top_signatory_dict.keys()
        ))
        # Augment ORM objects with average contribution percentage
        for signatory in top_signatories:
            signatory.signing_percentage = top_signatory_dict[signatory.pk]
        return sorted(top_signatories,
                      key=lambda s: s.signing_percentage,
                      reverse=True)

    @property
    def top_collaborating_fractions(self):
        return self.get_collaborating_fractions_percentage()


class GroupMembership(CrawledItem):
    member = models.ForeignKey(ParliamentMember,
                               related_name='groupmembership')
    group = models.ForeignKey(Group)
    position = models.CharField(max_length=128)
    since = models.DateField(blank=True, null=True)
    until = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'{} - {} ({})'.format(self.group.name,
                                      self.member.full_name,
                                      self.position)


class Stenogram(CrawledItem):
    source_id = models.CharField(max_length=16, db_index=True)
    date = models.DateField()
    sitting_no = models.IntegerField()
    sitting_name = models.TextField(blank=True, null=True)
    session = models.CharField(max_length=64, blank=True, null=True)

    def __unicode__(self):
        return u'{} Nr. {}'.format(self.date, self.sitting_no)


class StenogramTopic(CrawledItem):
    stenogram = models.ForeignKey(Stenogram, related_name='topics')
    title = models.TextField()
    timestamp = models.DateTimeField()
    presenters = models.ManyToManyField(ParliamentMember,
                                        related_name='presented_topics')

    def __unicode__(self):
        return self.title[:160]


class StenogramStatement(CrawledItem):
    topic = models.ForeignKey(StenogramTopic, related_name='statements')
    speaker = models.ForeignKey(ParliamentMember, related_name='statements',
                                blank=True, null=True)
    speaker_name = models.CharField(max_length=64)
    as_chairperson = models.BooleanField(default=False)
    text = models.TextField()
    word_count = models.PositiveIntegerField(default=0)

    precomputed_fields = (
        ('word_count', 'get_word_count'),
    )

    def get_speaker_name(self):
        return self.speaker.full_name if self.speaker else self.speaker_name

    def __unicode__(self):
        return u'{}: {}'.format(self.get_speaker_name(), self.text[:160])

    def get_word_count(self):
        return words_utils.get_word_count(self.text)


class Voting(models.Model):
    voting = models.ForeignKey('scrapy.Voting', related_name='stenogram_votings', null=True)
    stenogram_topic = models.ForeignKey(StenogramTopic, related_name='votings')
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ('voting', 'stenogram_topic')


def percentile_property(attr):
    def inner_fn(self):
        total = self.total
        return int((total - getattr(self, attr) + 1.0)
                   / total * 100 + 0.5)
    return property(inner_fn)


class Ranking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    votes_rank = models.IntegerField(default=0)
    statement_count_rank = models.IntegerField(default=0)
    long_statement_count_rank = models.IntegerField(default=0)
    discusion_contribution_percentage_rank = models.IntegerField(default=0)
    passed_law_project_ratio_rank = models.IntegerField(default=0)

    class Meta:
        abstract = True

    @reify
    def total(self):
        return self.__class__.objects.count()

    votes_percentile = percentile_property(
        'votes_rank')
    statement_count_percentile = percentile_property(
        'statement_count_rank')
    long_statement_count_percentile = percentile_property(
        'long_statement_count_rank')
    discusion_contribution_percentage_percentile = percentile_property(
        'discusion_contribution_percentage_rank')
    passed_law_project_ratio_percentile = percentile_property(
        'passed_law_project_ratio_rank')


class MPRanking(Ranking):
    target = models.OneToOneField(ParliamentMember,
                                  related_name='ranking')


class GroupRanking(Ranking):
    target = models.OneToOneField(Group,
                                  related_name='ranking')

    @reify
    def total(self):
        return self.__class__.objects.filter(
            target__type=self.target.type
        ).count()


class LawProject(CrawledItem):
    source_id = models.CharField(max_length=16, db_index=True, unique=True)
    date = models.DateField()
    project_name = models.TextField()
    project_number = models.CharField(max_length=32)
    project_url = models.URLField()

    proposers = models.ManyToManyField(ParliamentMember,
                                       related_name='law_projects')

    date_passed = models.DateField(blank=True, null=True)
    passing_source_id = models.CharField(max_length=16, blank=True,
                                         null=True, db_index=True)
    passing_doc_number = models.CharField(max_length=32, blank=True, null=True)
    passing_doc_url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        if self.date_passed:
            return u'{} ({}) - passed {}'.format(self.project_number,
                                                 self.date, self.date_passed)
        else:
            return u'{} ({})'.format(self.project_number, self.date)

    @reify
    def proposer_count(self):
        return self.proposers.count()

    def get_fraction_contributions(self):
        ''' Returns list of fractions with percent of their members
            in proposers list.
        '''
        proposers = self.proposers.prefetch_related(
            ParliamentMember.FractionPrefetch()
        )
        fraction_counts = Counter(map(lambda p: p.fraction, proposers))
        fractions = []
        for fraction, count in fraction_counts.items():
            if fraction:  # may be None if one of proposers is not in fraction
                fraction.fraction_contribution = (float(count)
                                                  / self.proposer_count
                                                  * 100.0)
                fractions.append(fraction)
        return fractions

    @classmethod
    def get_avg_passing_time(cls):
        avg = cls.objects.filter(date_passed__isnull=False).aggregate(
            avg_passing_time=models.Avg(
                models.Func(
                    models.F('date_passed'),
                    models.F('date'),
                    function='DATEDIFF',
                )
            )
        )
        return avg.get('avg_passing_time', 0.0)


class Suggester(CrawledItem):
    """Submittter of a suggestion."""
    slug = AutoSlugField(populate_from='title', max_length=120)
    title = models.TextField()


class CommitteeResolution(CrawledItem):
    source_id = models.CharField(max_length=16, unique=True)
    title = models.TextField()


class Suggestion(CrawledItem):
    source_resolution = models.ForeignKey(CommitteeResolution,
                                          db_column='source_id',
                                          to_field='source_id')
    source_index = models.IntegerField()

    submitter = models.ManyToManyField(Suggester, related_name='suggestions')
    date = models.DateField(blank=True, null=True)
    document = models.TextField(blank=True)
    opinion = models.TextField(blank=True)

    class Meta:
        unique_together = (('source_resolution', 'source_index'))

    def __unicode__(self):
        return u'{} ({})'.format(self.submitter, self.opinion)

    @classmethod
    def suggestion_and_project_count(self):
        """Count suggestions and law projects for each suggester."""
        cursor = connection.cursor()
        cursor.execute("""
            SELECT submitter_slug,
                   submitter AS title,
                   COUNT(source_id) AS law_project_count,
                   SUM(proposal_count) AS suggestion_count
            FROM (
                (SELECT
                    t1.slug as submitter_slug,
                    t1.title AS submitter,
                    t3.source_id AS source_id,
                    COUNT(t3.id) AS proposal_count
                    FROM
                        mps_v2_suggester AS t1,
                        mps_v2_suggestion_submitter as t2,
                        mps_v2_suggestion as t3
                        WHERE
                            t1.id=t2.suggester_id AND t2.suggestion_id=t3.id
                    GROUP BY submitter, source_id
                 ) AS t4
            )
            GROUP BY submitter_slug, submitter;
        """)
        rows = dict_fetch_all(cursor)

        counts = [{
            'title': row['title'],
            'url': reverse('suggester_profile',
                           kwargs={'suggester_slug': row['submitter_slug']}),
            'suggestion_count': int(row['suggestion_count']),
            'law_project_count': int(row['law_project_count']),
            'state_actor': is_state_actor(row['title']),
        } for row in rows]

        return counts

    @classmethod
    def suggestion_and_project_count_state(self):
        return [
            item
            for item in self.suggestion_and_project_count()
            if item['state_actor']
        ]

    @classmethod
    def suggestion_and_project_count_other(self):
        return [
            item
            for item in self.suggestion_and_project_count()
            if not item['state_actor']
        ]
