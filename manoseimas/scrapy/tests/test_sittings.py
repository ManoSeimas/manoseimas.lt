# coding: utf-8

import unittest

from scrapy.http import HtmlResponse

from ..spiders.sittings import SittingsSpider

from .utils import fixture


def parse_question(question_id):
    spider = SittingsSpider()
    url = ('http://www3.lrs.lt/pls/inter/w5_sale_new.klaus_stadija?'
           'p_svarst_kl_stad_id='+question_id)
    response = HtmlResponse(url, body=fixture('questions/'+question_id+'.html'))
    return list(spider.parse_question(response))


def parse_voting(voting_id):
    spider = SittingsSpider()
    url = ('http://www3.lrs.lt/pls/inter/w5_sale_new.bals?'
           'p_bals_id='+voting_id)
    response = HtmlResponse(url, body=fixture('votings/'+voting_id+'.html'))
    return list(spider.parse_person_votes(response))


class TestSittingsSpider(unittest.TestCase):

    maxDiff = None

    @unittest.skip('FIXME: no fixtures for CouchDB')
    def test_question(self):
        questions = fixture('questions.json')
        for q in questions:
            items = parse_question(q[0])
            # question
            item = items[0]
            self.assertEqual(item['_id'], q[0]+'q')

            # voting
            if len(items) > 1:
                item = items[1]
                self.assertEqual(item['_id'], q[1]+'v')
            else:
                self.assertIsNone(q[1])

    @unittest.skip('FIXME: no fixtures for CouchDB')
    def test_votings(self):
        votings = fixture('votings.json')
        for v in votings:
            print "Processing %s" % v['_id']
            items = parse_voting(v['_id'])

            item = items[0]
            self.assertEqual(item['_id'], v['_id']+'v')
            self.assertEqual(item['documents'], v['documents'])
            self.assertEqual(item['votes'][0], v['votes'][0])

"""
    def test_voting(self):
        items = parse_voting("-10765")

        item = items[0]
        self.assertEqual(item['_id'], '-10765v')
        self.assertEqual(item['documents'], [u'XIP-2992', u'XIP-2993'])
        self.assertEqual(item['votes'][0], {
            'fraction': u'TTF',
            'name': u'Ačas Remigijus',
            'person': u'47852p',
            'vote': u'aye'
        })

    def test_voting2(self):
        items = parse_voting("-11071")

        item = items[0]
        self.assertEqual(item['_id'], '-11071v')
        self.assertEqual(item['documents'], [u'XIP-2779(2)', u'XIP-2780(2)', u'XIP-2781(2)'])
        self.assertEqual(item['votes'][0], {
            'fraction': u'TSLKDF',
            'name': u'Adomėnas Mantas',
            'person': u'48690p',
            'vote': u'abstain'
        })
"""
