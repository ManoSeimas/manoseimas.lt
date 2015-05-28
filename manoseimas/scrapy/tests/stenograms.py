# coding: utf-8

import unittest
from scrapy.http import HtmlResponse
from scrapy.link import Link

from manoseimas.scrapy.tests.utils import fixture


from manoseimas.scrapy.spiders.stenograms import StenogramSpider


class LinkExtractorsTestCase(unittest.TestCase):

    def test_stenogram_link_extractor(self):
        url = ('http://www3.lrs.lt/pls/inter/w5_sale.fakt_pos'
               '?p_fakt_pos_id=-500911')
        response = HtmlResponse(url, body=fixture('sitting_500911.html'))

        link_extractor = StenogramSpider.stenogram_link_extractor
        links = link_extractor.extract_links(response)
        self.assertEqual(links,
                         [Link(url=('http://www3.lrs.lt/pls/inter/'
                                    'dokpaieska.showdoc_l?p_id=1034324'),
                               text=u'Stenograma')])


class StenogramCrawlerTestCase(unittest.TestCase):

    def setUp(self):
        super(StenogramCrawlerTestCase, self).setUp()
        url = 'http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=1034324'
        self.response = HtmlResponse(url,
                                     body=fixture('stenogram_1034324.html'))
        self.spider = StenogramSpider()

    def test_parse_stenogram(self):
        self.spider.parse_stenogram(self.response)
