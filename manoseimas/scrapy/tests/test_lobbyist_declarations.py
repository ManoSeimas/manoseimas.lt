# -*- coding: utf-8 -*-
import unittest

import mock
import scrapy
from scrapy.http import Response, HtmlResponse, XmlResponse, TextResponse

from manoseimas.scrapy.items import LobbyistDeclaration
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.spiders.lobbyist_declarations import LobbyistDeclarationsSpider
from manoseimas.scrapy.tests.utils import fixture


class TestLobbyistDeclarationsSpider(unittest.TestCase):

    number_examples = [
        ('<entry>\n1.\n</entry>', {}),
    ]

    name_examples = [
        ('<entry>\nROMAS STUMBRYS\n</entry>', {
            'name': 'ROMAS STUMBRYS',
        }),
        ('<entry>\nBRONIUS ANTANAS RASIMAS\n</entry>', {
            'name': 'BRONIUS ANTANAS RASIMAS',
        }),
        ('<entry>\nUAB "ERNST &amp; YOUNG BALTIC"\n</entry>', {
            'name': 'UAB "ERNST & YOUNG BALTIC"',
        }),
        ('<entry>\nUAB “GLAXOSMITHKLINE LIETUVA”\n</entry>', {
            'name': u'UAB “GLAXOSMITHKLINE LIETUVA”',
        }),
        ('<entry>\nUAB „VENTO NUOVO“\n</entry>', {
            'name': u'UAB „VENTO NUOVO“',
        }),
        ('<entry>\nADVOKATŲ PROFESINĖ BENDRIJA "BALTIC LEGAL SOLUTIONS LIETUVA”\n</entry>', {
            'name': u'ADVOKATŲ PROFESINĖ BENDRIJA "BALTIC LEGAL SOLUTIONS LIETUVA”',
        }),
        ('<entry>\nVŠĮ "MOKESČIŲ IR VERSLO PROCESŲ ADMINISTRAVIMO CENTRAS"\n</entry>', {
            'name': u'VŠĮ "MOKESČIŲ IR VERSLO PROCESŲ ADMINISTRAVIMO CENTRAS"',
        }),
    ]

    law_projects_examples = [
        ('<entry>\n\n</entry>', {
        }),
        ('<entry>\n-\n</entry>', {
        }),
        ('<entry>\nLietuvos Respublikos asociacijų įstatymas.\n</entry>', {
            'law_projects': [u'Lietuvos Respublikos asociacijų įstatymas'],
        }),
        ('<entry>\n'
         '1) Teisės aktai, reguliuojantys viešųjų pirkimų procedūras;\n'
         '2)   Lietuvis higienos norma HN 80:2011 „Elektromagnetinis laukas darbo vietose ir gyvenamojoje aplinkoje“.\n'  # [sic]
         '3)  Radijo ryšio plėtros planas.\n'
         '<entry>',
         {
             'law_projects': [
                 u'Teisės aktai, reguliuojantys viešųjų pirkimų procedūras',
                 u'Lietuvis higienos norma HN 80:2011 „Elektromagnetinis laukas darbo vietose ir gyvenamojoje aplinkoje“',
                 u'Radijo ryšio plėtros planas',
             ],
         }),
    ]

    comments_examples = [
        ('<entry>\n\n</entry>', {
            'comments': '',
        }),
        ('<entry>\nLobistinės veiklos nevykdė\n</entry>', {
            'comments': u'Lobistinės veiklos nevykdė',
        }),
        ('<entry>\nLobistinė veikla sustabdyta\n</entry>', {
            'comments': u'Lobistinė veikla sustabdyta',
        }),
    ]

    def setUp(self):
        self.spider = LobbyistDeclarationsSpider()

    def run_examples(self, examples, wrapper, fn):
        for html, expected in examples:
            actual = wrapper(html, fn)
            self.assertEqual(expected, actual)

    def parse_field(self, html, fn):
        response = XmlResponse('http://localhost/test.html',
                               body='<book><row>%s</row></book>' % html)
        row = response.css('row')[0]
        node = response.css('entry')[0]
        declaration = Loader(self.spider, response, LobbyistDeclaration(), row)
        declaration.add_value(None, fn(node))
        item = declaration.load_item()
        actual = dict(item)
        return actual

    def test_parse_number(self):
        self.run_examples(self.number_examples, self.parse_field,
                          self.spider._parse_number)

    def test_parse_name(self):
        self.run_examples(self.name_examples, self.parse_field,
                          self.spider._parse_name)

    def test_parse_law_projects(self):
        self.run_examples(self.law_projects_examples, self.parse_field,
                          self.spider._parse_law_projects)

    def test_split_projects(self):
        self.assertEqual(self.spider._split_projects(' '), [])
        self.assertEqual(self.spider._split_projects(' - '), [])
        self.assertEqual(self.spider._split_projects(' foo '), ['foo'])
        self.assertEqual(self.spider._split_projects('foo.'), ['foo'])
        self.assertEqual(self.spider._split_projects('foo; bar.'), ['foo; bar'])
        self.assertEqual(self.spider._split_projects('foo;\nbar.'), ['foo', 'bar'])
        self.assertEqual(self.spider._split_projects('1) foo;\n2) bar.'), ['foo', 'bar'])

    def test_clean_project(self):
        self.assertEqual(self.spider._clean_project('foo'), 'foo')
        self.assertEqual(self.spider._clean_project(' foo '), 'foo')
        self.assertEqual(self.spider._clean_project('foo.'), 'foo')
        self.assertEqual(self.spider._clean_project('foo;'), 'foo')
        self.assertEqual(self.spider._clean_project('1) foo'), 'foo')
        self.assertEqual(self.spider._clean_project('20)  foo'), 'foo')
        self.assertEqual(self.spider._clean_project('1)  foo'), 'foo')

    def test_parse_comments(self):
        self.run_examples(self.comments_examples, self.parse_field,
                          self.spider._parse_comments)

    def test_parse(self):
        response = HtmlResponse('http://www.vtek.lt/index.php/deklaravimas', body=fixture('vtek_deklaravimas.html'))
        items = list(self.spider.parse(response))
        self.assertEqual(len(items), 3)
        self.assertTrue(isinstance(items[0], scrapy.Request))
        self.assertEqual(items[0].meta['year'], '2014')
        self.assertEqual(items[0].url,
                         'http://old.vtek.lt/vtek/images/vtek/Dokumentai/Lobizmas/lobistu_deklaracijos/Info_apie_lobistu_ataskaitas_2014_2015_04_08.doc')

    def test_parse_declaration_doc(self):
        response = Response('http://old.vtek.lt/vtek/.../deklaracija2012.doc', body='msword msword msword')
        response.request = scrapy.Request(response.url)
        response.request.meta['year'] = '2012'

        def mock_doc2xml(msword):
            assert msword == 'msword msword msword'
            return 'xml xml xml'

        with mock.patch('manoseimas.scrapy.spiders.lobbyist_declarations.doc2xml', mock_doc2xml):
            with mock.patch.object(self.spider, 'parse_declaration_xml') as p_d_x:
                list(self.spider.parse_declaration_doc(response))
                assert p_d_x.call_count == 1
                new_response = p_d_x.call_args[0][0]
                assert new_response.meta['year'] == '2012'
                assert new_response.body == 'xml xml xml'
                assert isinstance(new_response, XmlResponse)

    def test_parse_declaration_xml(self):
        response = XmlResponse('http://old.vtek.lt/vtek/.../deklaracija2012.doc',
                               body=fixture('lobist_veiklos_atatskaita_2012.doc.xml'))
        response.request = scrapy.Request(response.url)
        response.request.meta['year'] = '2012'

        items = list(self.spider.parse_declaration_xml(response))
        self.assertEqual(len(items), 30)
        self.assertEqual(items[0]['name'], 'ROMAS STUMBRYS')
        self.assertEqual(items[0]['comments'], u'Lobistinės veiklos nevykdė')
