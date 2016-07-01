# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

from django.db.models import Avg

from manoseimas.scrapy.models import PersonVote


def get_topic_positions(topic):
    votings = topic.votings.values_list('key', flat=True)
    qs = (
        PersonVote.objects.
        filter(voting_id__in=votings).
        values('p_asm_id', 'name', 'fraction').
        annotate(vote=Avg('vote'))
    )
    return {x.pop('p_asm_id'): x for x in qs}
