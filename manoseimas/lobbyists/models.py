from django.db import models
from django_extensions.db.fields import AutoSlugField


class CrawledItem(models.Model):
    source = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    raw_data = models.CharField(max_length=10240, blank=True)

    class Meta:
        abstract = True


class Lobbyist(CrawledItem):
    slug = AutoSlugField(populate_from='name', max_length=120)
    name = models.CharField(max_length=128)
    # XXX: should probably be a separate table
    representatives = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    company_code = models.CharField(max_length=32, blank=True)
    # date of inclusion into the official list of lobbyists
    date_of_inclusion = models.DateField()
    # number of the decision to include into the official list of lobbyinsts
    decision = models.CharField(max_length=128)
    # status message about lobbyist activity possibly being suspended
    status = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name


class LobbyistDeclaration(CrawledItem):
    lobbyist_name = models.CharField(max_length=128)
    lobbyist = models.ForeignKey('Lobbyist', blank=True, null=True)
    year = models.IntegerField()
    comments = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return u'{} ({})'.format(self.lobbyist_name, self.year)


class LobbyistClient(models.Model):
    declaration = models.ForeignKey('LobbyistDeclaration',
                                    related_name='clients')
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class LobbyistLawProject(models.Model):
    client = models.ForeignKey('LobbyistClient', related_name='law_projects')
    title = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.title
