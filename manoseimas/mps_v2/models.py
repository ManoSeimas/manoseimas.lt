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
    date_of_birth = models.CharField(max_length=16)
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    candidate_page = models.URLField()
    raised_by = models.ForeignKey('PoliticalParty')
    photo = models.ImageField(upload_to='/tmp/images')  # FIXME
    term_of_office = models.CharField(max_length=32)

    office_address = models.TextField()
    constituency = models.CharField(max_length=128)
    party_candidate = models.BooleanField(default=True)
    groups = models.ManyToManyField('Group', through='GroupMembership')

    biography = models.TextField()

    @property
    def full_name(self):
        return ' '.join([self.first_name, self.last_name])


class PoliticalParty(CrawledItem):
    name = models.CharField(max_length=128, unique=True)


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


class GroupMembership(CrawledItem):
    member = models.ForeignKey(ParliamentMember)
    group = models.ForeignKey(Group)
    position = models.CharField(max_length=64)
    since = models.DateField(blank=True, null=True)
    until = models.DateField(blank=True, null=True)
