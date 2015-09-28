from django.db import models
from django_extensions.db.fields import AutoSlugField


class CrawledItem(models.Model):
    source = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    raw_data = models.CharField(max_length=1024, blank=True)

    class Meta:
        abstract = True


class Lobbyist(models.Model):
    slug = AutoSlugField(populate_from='name', max_length=120)
    name = models.CharField(max_length=128)
    # XXX: should probably be a separate table
    representatives = models.CharField(max_length=255)
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
