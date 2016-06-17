from django.db import models

from jsonfield import JSONField


class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    # [[mp_id, fraction_id, pozicija], ...]
    # recalculating on each voting adding
    positions = JSONField()
    votings = models.ManyToManyField('scrapy.Voting', through='TopicVoting')

    def __unicode__(self):
        return self.name


class TopicVoting(models.Model):
    topic = models.ForeignKey(Topic)
    voting = models.ForeignKey('scrapy.Voting')
    factor = models.PositiveIntegerField(default=1)  # voting importance

    def __unicode__(self):
        return self.voting.get_title()


class CompatTest(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class TestGroup(models.Model):
    name = models.CharField(max_length=200)
    test = models.ForeignKey(CompatTest, null=True)
    topics = models.ManyToManyField(Topic, related_name='groups')

    # TODO: unique(test, topic)

    def __unicode__(self):
        return self.name


class Argument(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    supporting = models.BooleanField(default=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='arguments')
