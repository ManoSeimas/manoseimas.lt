# coding: utf-8

import datetime

from django.db import models

from jsonfield import JSONField


class ScrapyPipe(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    key = models.CharField(max_length=255, unique=True)
    value = JSONField()

    class Meta:
        abstract = True

    def update_from_item(self, item):
        self.key = item['_id']
        self.value = self.value if self.value else {}
        for key, value in item.items():
            self.value[key] = value
        self.update_from_item_extra(item)
        return self

    def update_from_item_extra(self, item):
        pass


class Question(ScrapyPipe):
    pass


class Person(ScrapyPipe):
    p_asm_id = models.CharField(max_length=16, default='')  # also known as source_id

    def update_from_item_extra(self, item):
        self.p_asm_id = item['_id']


class PersonVote(ScrapyPipe):
    voting_id = models.CharField(max_length=16)
    p_asm_id = models.CharField(max_length=16)
    fraction = models.CharField(max_length=16)
    name = models.CharField(max_length=255)
    vote = models.SmallIntegerField(default=0)
    timestamp = models.DateTimeField(null=True)

    def update_from_item_extra(self, item):
        votemap = {
            'aye': 2,
            'no': -2,
            'abstain': -1,
            'no-vote': -1,
        }
        self.voting_id = item['voting_id']
        self.p_asm_id = item['person']
        self.fraction = item['fraction']
        self.name = item['name']
        self.vote = votemap[item['vote']]
        self.timestamp = datetime.datetime.strptime(item['datetime'], '%Y-%m-%d %H:%M:%S')

    def save(self, *args, **kwargs):
        if self.fraction == u'LLRAF':
            self.fraction = u'LLRAKŠSF'
        elif self.fraction == u'TS-LKDF':
            self.fraction == u'TSLKDF'
        super(PersonVote, self).save(*args, **kwargs)


class Voting(ScrapyPipe):
    name = models.CharField(max_length=200)
    timestamp = models.DateTimeField(null=True)
    source = models.URLField()

    def update_from_item_extra(self, item):
        if 'formulation' in item:
            self.name = item['formulation']
        elif 'formulation_a' in item:
            self.name = 'a) %s; b) %s' % (item['formulation_a'], item['formulation_b'])
        self.timestamp = datetime.datetime.strptime(item['datetime'], '%Y-%m-%d %H:%M:%S')
        if 'source' in item:
            self.source = item['source']['url']
        self.value.setdefault('documents', [])

    def get_title(self):
        if self.value['documents']:
            return self.value['documents'][0]['name']
        elif 'formulation' in self.value:
            return self.value['formulation']
        elif 'formulation_a' in self.value:
            return 'a) %s; b) %s' % (self.value['formulation_a'], self.value['formulation_b'])

    def __unicode__(self):
        return self.name
