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
    url = ('http://www3.lrs.lt/pls/inter/w5_sale_new.klaus_stadija?p_svarst_kl_stad_id=' + question_id)
    response = HtmlResponse(url, body=fixture('questions/' + question_id + '.html'))
    return list(spider.parse_question(response))


def parse_voting(voting_id):
    spider = SittingsSpider()
    url = ('http://www3.lrs.lt/pls/inter/w5_sale_new.bals?p_bals_id=' + voting_id)
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
            self.assertGreater(len(items), 140)

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
        items = parse_voting("-10765")

        item = items[-1]
        self.assertEqual(item['_id'], '-10765v')
        self.assertEqual([x['number'] for x in item['documents']], [u'XIP-2992', u'XIP-2993'])
        self.assertEqual(item['votes'][0], {
            '_id': u'-10765:47852',
            'fraction': u'TTF',
            'name': u'Ačas Remigijus',
            'person': u'47852p',
            'vote': u'aye',
            'datetime': u'2011-03-24 12:42:09',
        })

    def test_voting2(self):
        pipeline = ManoseimasPipeline()

        items = parse_voting("-11071")

        item = items[-1]
        self.assertEqual(item['_id'], '-11071v')
        self.assertEqual([x['number'] for x in item['documents']], [u'XIP-2779(2)', u'XIP-2780(2)', u'XIP-2781(2)'])
        self.assertEqual(item['votes'][0], {
            '_id': u'-11071:48690',
            'fraction': u'TSLKDF',
            'name': u'Adomėnas Mantas',
            'person': u'48690p',
            'vote': u'abstain',
            'datetime': u'2011-04-26 10:58:31',
        })

        p_vote = items[0]
        self.assertTrue(isinstance(p_vote, PersonVote))
        pipeline.process_item(p_vote, None)
        obj = models.PersonVote.objects.get(key=p_vote['_id'])
        self.assertEqual(obj.name, u'Adomėnas Mantas')

    def test_voting_pipeline(self):
        crawl(
            Pipeline=ManoseimasPipeline, spider=SittingsSpider(),
            param='p_svarst_kl_stad_id', method='parse_question', path='questions/%s.html', urls=[
                'http://www3.lrs.lt/pls/inter/w5_sale_new.klaus_stadija?p_svarst_kl_stad_id=-9209',
            ],
        )

        crawl(
            Pipeline=ManoseimasPipeline, spider=SittingsSpider(),
            param='p_bals_id', method='parse_person_votes', path='votings/%s.html', urls=[
                'http://www3.lrs.lt/pls/inter/w5_sale_new.bals?p_bals_id=-10764',
            ],
        )

        voting = models.Voting.objects.get()
        self.assertEqual(voting.key, u'-10764v')
        self.assertEqual(voting.name, u'dėl savaitės (nuo 2011-03-28) darbotvarkės patvirtinimo;')
        self.assertEqual(voting.timestamp, datetime.datetime(2011, 3, 24, 12, 19, 12))
        self.assertEqual(voting.source, u'http://www3.lrs.lt/pls/inter/w5_sale_new.bals?p_bals_id=-10764')
        self.assertEqual(sorted(voting.value.keys()), [
            '_id',
            'datetime',
            'documents',
            'formulation',
            'no_vote',
            'question',
            'registration',
            'result',
            'source',
            'total_votes',
            'type',
            'vote_abstain',
            'vote_aye',
            'vote_no',
            'votes',
        ])
