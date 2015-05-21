from django.db import models
# from django.utils.translation import ugettext as _


class CrawledItem(models.Model):
    source = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ParliamentMember(CrawledItem):
    source_id = models.CharField(max_length=16)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    candidate_page = models.URLField(blank=True, null=True)
    raised_by = models.ForeignKey('PoliticalParty', blank=True, null=True)
    photo = models.ImageField(upload_to='/tmp/images', blank=True, null=True)
    term_of_office = models.CharField(max_length=32, blank=True, null=True)

    office_address = models.TextField(blank=True, null=True)
    constituency = models.CharField(max_length=128, blank=True, null=True)
    party_candidate = models.BooleanField(default=True)
    groups = models.ManyToManyField('Group', through='GroupMembership')

    biography = models.TextField(blank=True, null=True)

    @property
    def full_name(self):
        return u' '.join([self.first_name, self.last_name])

    def __unicode__(self):
        return self.full_name

    @property
    def fraction(self):
        return self.groups.get(type='fraction')


class PoliticalParty(CrawledItem):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Group(CrawledItem):
    GROUP_TYPES = (
        ('group', ('Group')),
        ('committee', ('Committee')),
        ('commission', ('Commission')),
        ('fraction', ('Fraction')),
        ('parliament', ('Parliament')),
    )

    name = models.CharField(max_length=128, unique=True)
    type = models.CharField(max_length=16,
                            choices=GROUP_TYPES)

    class Meta:
        unique_together = (('name', 'type'))

    def __unicode__(self):
        return u'{} ({})'.format(self.name, self.type)


class GroupMembership(CrawledItem):
    member = models.ForeignKey(ParliamentMember)
    group = models.ForeignKey(Group)
    position = models.CharField(max_length=64)
    since = models.DateField(blank=True, null=True)
    until = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'{} - {} ({})'.format(self.group.name,
                                      self.member.full_name,
                                      self.position)
