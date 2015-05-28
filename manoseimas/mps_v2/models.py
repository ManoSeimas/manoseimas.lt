from django.db import models
from autoslug import AutoSlugField

from django.utils.translation import ugettext_lazy as _


class CrawledItem(models.Model):
    source = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def get_mp_full_name(mp):
    return mp.full_name


class ParliamentMember(CrawledItem):
    slug = AutoSlugField(populate_from=get_mp_full_name)
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
    def fractions(self):
        return self.groups.filter(type='fraction')

    @property
    def current_fraction(self):
        membership = GroupMembership.objects.filter(member=self.id,
                                                    group__type='fraction',
                                                    until=None)[:]

        if membership:
            return membership[0].group
        else:
            return None

    @property
    def other_group_memberships(self):
        # Not fraction groups
        return GroupMembership.objects.filter(member=self)\
            .exclude(group__type='fraction')


class PoliticalParty(CrawledItem):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Group(CrawledItem):
    GROUP_TYPES = (
        ('group', _('Group')),
        ('committee', _('Committee')),
        ('commission', _('Commission')),
        ('fraction', _('Fraction')),
        ('parliament', _('Parliament')),
    )

    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')
    type = models.CharField(max_length=64,
                            choices=GROUP_TYPES)

    class Meta:
        unique_together = (('name', 'type'))

    def __unicode__(self):
        return u'{} ({})'.format(self.name, self.type)


class GroupMembership(CrawledItem):
    member = models.ForeignKey(ParliamentMember)
    group = models.ForeignKey(Group)
    position = models.CharField(max_length=128)
    since = models.DateField(blank=True, null=True)
    until = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'{} - {} ({})'.format(self.group.name,
                                      self.member.full_name,
                                      self.position)
