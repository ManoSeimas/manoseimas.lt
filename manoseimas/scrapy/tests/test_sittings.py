# coding: utf-8

import datetime

from django.test import TestCase

from scrapy.http import HtmlResponse

from ..spiders.sittings import SittingsSpider

from .utils import fixture
from manoseimas.scrapy import models
from manoseimas.scrapy.items import PersonVote
from manoseimas.scrapy.pipelines import ManoseimasPipeline
from manoseimas.scrapy.tests.utils import crawl



def parse_question(question_id):
    spider = SittingsSpider()
    url = ('http://www.lrs.lt/sip/portal.show?p_r=15275&p_k=1&p_a=sale_klaus_stadija&p_svarst_kl_stad_id=' + question_id)
    response = HtmlResponse(url, body=fixture('questions/' + question_id + '.html'))
    return list(spider.parse_question(response))


def parse_voting(voting_id):
    spider = SittingsSpider()
    url = ('http://www.lrs.lt/sip/portal.show?p_r=15275&p_k=1&p_a=sale_bals&p_bals_id=' + voting_id)
    response = HtmlResponse(url, body=fixture('votings/' + voting_id + '.html'))
    return list(spider.parse_person_votes(response))


class TestSittingsSpider(TestCase):

    maxDiff = None

    def test_question(self):
        questions = fixture('questions.json')
        for q in questions:
            items = parse_question(q[0])
            # question
            item = items[0]
            self.assertEqual(item['_id'], q[0] + 'q')

            # voting
            if len(items) > 1:
                item = items[1]
                self.assertEqual(item['_id'], q[1] + 'v')
            else:
                self.assertIsNone(q[1])

    def test_votings(self):
        pipeline = ManoseimasPipeline()
        votings = fixture('votings.json')
        for v in votings:
            items = parse_voting(v['_id'])
            #self.assertGreater(len(items), 80)

            p_vote = items[0]
            self.assertTrue(isinstance(p_vote, PersonVote))
            pipeline.process_item(p_vote, None)
            self.assertTrue(models.PersonVote.objects.filter(key=p_vote['_id']).exists())

            item = items[-1]
            self.assertEqual(item['_id'], v['_id'] + 'v')
            self.assertEqual(item['documents'], v['documents'])
            self.assertEqual(item['votes'][0], v['votes'][0])

            pipeline.process_item(item, None)
            self.assertTrue(models.Voting.objects.filter(key=item['_id']).exists())

    def test_voting(self):
        items = parse_voting("-26942")

        item = items[-1]
        self.assertEqual(item['_id'], '-26942v')
        self.assertEqual([x['number'] for x in item['documents']], [u'XIIIP-944', u'XIIIP-945'])
        self.assertEqual(item['votes'][0], {
            'name': u'Andrikis Rimas',
            'datetime': u'2017-06-30 14:17:54',
            'person': u'79163p',
            'fraction': u'TTF',
            'vote': u'abstain',
            '_id': u'-26942:79163',
            'voting_id': u'-26942v'
            })
