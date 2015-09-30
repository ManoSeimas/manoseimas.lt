# -*- coding: utf-8 -*-
import unittest

import mock
import scrapy
from scrapy.http import HtmlResponse

from manoseimas.scrapy.spiders.lobbyist_declarations import LobbyistDeclarationsSpider
from manoseimas.scrapy.tests.utils import fixture


class TestLobbyistDeclarationsSpider(unittest.TestCase):

    def setUp(self):
        self.spider = LobbyistDeclarationsSpider()

    def test_parse(self):
        response = HtmlResponse('http://www.vtek.lt/index.php/deklaravimas', body=fixture('vtek_deklaravimas.html'))
        items = list(self.spider.parse(response))
        self.assertEqual(len(items), 3)
        self.assertTrue(isinstance(items[0], scrapy.Request))
        self.assertEqual(items[0].meta['year'], '2014')
        self.assertEqual(items[0].url,
                         'http://old.vtek.lt/vtek/images/vtek/Dokumentai/Lobizmas/lobistu_deklaracijos/Info_apie_lobistu_ataskaitas_2014_2015_04_08.doc')

    def test_parse_declaration_doc(self):
        response = HtmlResponse('http://old.vtek.lt/vtek/.../deklaracija2012.doc', body='msword msword msword')
        response.request = scrapy.Request(response.url)
        response.request.meta['year'] = '2012'

        def mock_doc2xml(msword):
            assert msword == 'msword msword msword'
            return 'xml xml xml'

        with mock.patch('manoseimas.scrapy.spiders.lobbyist_declarations.doc2xml', mock_doc2xml):
            with mock.patch.object(self.spider, 'parse_declaration_xml') as p_d_x:
                list(self.spider.parse_declaration_doc(response))
                assert p_d_x.call_count == 1
                assert p_d_x.call_args[0][0].meta['year'] == '2012'
                assert p_d_x.call_args[0][0].body == 'xml xml xml'

    def test_parse_declaration_xml(self):
        response = HtmlResponse('http://old.vtek.lt/vtek/.../deklaracija2012.doc',
                                body=fixture('lobist_veiklos_atatskaita_2012.doc.xml'))
        response.request = scrapy.Request(response.url)
        response.request.meta['year'] = '2012'

        items = list(self.spider.parse_declaration_xml(response))
        self.assertEqual(len(items), 30)
        self.assertEqual(items[0]['name'], 'ROMAS STUMBRYS')
        self.assertEqual(items[0]['comments'], u'Lobistinės veiklos nevykdė')
