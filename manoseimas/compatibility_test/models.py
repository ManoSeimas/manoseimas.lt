# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from jsonfield import JSONField


class Topic(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=40)
    description = models.TextField()
    votings = models.ManyToManyField('scrapy.Voting', through='TopicVoting')
    image = models.ImageField(upload_to='topic_images',
                              blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temos'


class TopicVoting(models.Model):
    topic = models.ForeignKey(Topic)
    voting = models.ForeignKey('scrapy.Voting')
    factor = models.IntegerField(default=1)  # voting importance

    def __unicode__(self):
        return self.voting.get_title()


class CompatTest(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='test_images',
                              blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Testas'
        verbose_name_plural = 'Testai'


class TestGroup(models.Model):
    name = models.CharField(max_length=200)
    test = models.ForeignKey(CompatTest, null=True, related_name='groups')
    topics = models.ManyToManyField(Topic, related_name='groups', blank=True)

    # TODO: unique(test, topic)

    def __unicode__(self):
        return '%s - %s' % (self.test, self.name)

    class Meta:
        ordering = ('test', 'name')
        verbose_name = 'Testo grupė'
        verbose_name_plural = 'Testo grupės'


class Argument(models.Model):
    name = models.CharField(max_length=150)
    short_description = models.TextField(max_length=300)
    description = models.TextField(blank=True)
    supporting = models.BooleanField(default=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='arguments')


class UserResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    test = models.ForeignKey(CompatTest, null=True)
    result = JSONField()
