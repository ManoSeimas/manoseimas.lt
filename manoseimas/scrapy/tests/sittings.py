# coding: utf-8

import unittest

from scrapy.http import HtmlResponse

from ..spiders.sittings import SittingsSpider

from .utils import fixture


class TestSittingsSpider(unittest.TestCase):
    def test_nedzinskas(self):
        spider = SittingsSpider()
        url = ('http://www3.lrs.lt/pls/inter/w5_sale_new.bals?'
               'p_bals_id=-10765')
        response = HtmlResponse(url, body=fixture('sitting_-10765.html'))
        items = list(spider.parse_person_votes(response))
        item = items[0]
        self.assertEqual(item['_id'], '-10765v')
        self.assertEqual(item['documents'], [u'XIP-2992', u'XIP-2993'])
        self.assertEqual(item['votes'][0], {
            'fraction': u'TTF',
            'name': u'Ačas Remigijus',
            'person': u'47852p',
            'vote': u'aye'
        })
