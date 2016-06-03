from django.db import models

from jsonfield import JSONField


class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    # [[mp_id, fraction_id, pozicija], ...]
    # recalculating on each voting adding
    positions = JSONField()
    votings = models.ManyToManyField('scrapy.Voting', through='TopicVoting')


class TopicVoting(models.Model):
    topic = models.ForeignKey(Topic)
    voting = models.ForeignKey('scrapy.Voting')
    factor = models.PositiveIntegerField(default=1)  # voting importance


class CompatTest(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()


class TestGroup(models.Model):
    name = models.CharField(max_length=200)
    test = models.ForeignKey(CompatTest, null=True)
    topics = models.ManyToManyField(Topic)


class Argument(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    supporting = models.BooleanField(default=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
