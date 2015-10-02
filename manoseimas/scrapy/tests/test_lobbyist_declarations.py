# -*- coding: utf-8 -*-
import unittest

import mock
import scrapy
from scrapy.http import Response, HtmlResponse, XmlResponse

from manoseimas.scrapy.items import LobbyistDeclaration
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.spiders.lobbyist_declarations import LobbyistDeclarationsSpider
from manoseimas.scrapy.tests.utils import fixture


class TestLobbyistDeclarationsSpider(unittest.TestCase):

    maxDiff = None

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
        ('<entry>\n\n</entry>', []),
        ('<entry>\n-\n</entry>', []),
        ('<entry>\nLietuvos Respublikos asociacijų įstatymas.\n</entry>', [
            u'Lietuvos Respublikos asociacijų įstatymas',
        ]),
        ('<entry>\n'
         '1) Teisės aktai, reguliuojantys viešųjų pirkimų procedūras;\n'
         '2)   Lietuvis higienos norma HN 80:2011 „Elektromagnetinis laukas darbo vietose ir gyvenamojoje aplinkoje“.\n'  # [sic]
         '3)  Radijo ryšio plėtros planas.\n'
         '<entry>',
         [
             u'Teisės aktai, reguliuojantys viešųjų pirkimų procedūras',
             u'Lietuvis higienos norma HN 80:2011 „Elektromagnetinis laukas darbo vietose ir gyvenamojoje aplinkoje“',
             u'Radijo ryšio plėtros planas',
         ]),
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

    lobbyist_examples = [
        ('''
            <row>
             <entry>
            25.
             </entry>
             <entry>
            KĘSTUTIS KVAINAUSKAS
             </entry>
             <entry>
            1) Lietuvos Respublikos azartinių lošimų įstatymas;
            2) Lietuvos Respublikos statybos įstatymas;
             </entry>
             <entry>
             </entry>
            </row>
         ''',
         {
             'name': u'KĘSTUTIS KVAINAUSKAS',
             'law_projects': [
                 u'Lietuvos Respublikos azartinių lošimų įstatymas',
                 u'Lietuvos Respublikos statybos įstatymas',
             ],
             'comments': u'',
             'source_url': u'http://localhost/test.html',
         }),
        ('''
            <row>
             <entry>
            21.
             </entry>
             <entry>
            LIUDVIKAS RAGAUSKIS
             </entry>
             <entry>
            1. Visuomeninė organizacija Žvėryno bendruomenė
             </entry>
             <entry>
            1. Lietuvos Respublikos vietos savivaldos tarybų rinkimų įstatymas;
             </entry>
             <entry>
             </entry>
            </row>
            <row>
             <entry>
             </entry>
             <entry>
             </entry>
             <entry>
            2. VšĮ „Gamtos ateitis"
             </entry>
             <entry>
            1. Lietuvos Respublikos atliekų tvarkymo įstatymas;
             </entry>
             <entry>
             </entry>
            </row>
            <row>
             <entry>
             </entry>
             <entry>
             </entry>
             <entry>
            3. VšĮ „Konstitucinių teisių gynimo agentūra“
             </entry>
             <entry>
            1. Lietuvos Respublikos rinkimų kodeksas;
            2. Lietuvos Respublikos žemės reformos įstatymas;
            3. Lietuvos Respublikos saugomų teritorijų įstatymas;
            4. Lietuvos Respublikos teismų įstatymas;
            5. Lietuvos Respublikos teritorijų planavimo įstatymas;
            6. Lietuvos Respublikos žemės įstatymas;
            7. Lietuvos Respublikos nekilnojamojo kultūros paveldo apsaugos įstatymas.
             </entry>
             <entry>
             </entry>
            </row>
            <row>
             <entry>
             </entry>
             <entry>
             </entry>
             <entry>
            4. VšĮ „Vilniaus metro“
             </entry>
             <entry>
            1. Lietuvos Respublikos geležinkelių transporto kodekso patvirtinimo, įsigaliojimo ir taikymo įstatymas;
            2. Lietuvos Respublikos metropoliteno įstatymas;
             </entry>
             <entry>
             </entry>
            </row>
      ''',
      {
          'name': u'LIUDVIKAS RAGAUSKIS',
          'clients': [
              {
                  'client': u'Visuomeninė organizacija Žvėryno bendruomenė',
                  'law_projects': [
                      u'Lietuvos Respublikos vietos savivaldos taryb\u0173 rinkim\u0173 \u012fstatymas',
                  ],
              },
              {
                  'client': u'VšĮ „Gamtos ateitis"',
                  'law_projects': [
                      u'Lietuvos Respublikos atliek\u0173 tvarkymo \u012fstatymas',
                  ],
              },
              {
                  'client': u'VšĮ „Konstitucinių teisių gynimo agentūra“',
                  'law_projects': [
                      u'Lietuvos Respublikos rinkim\u0173 kodeksas',
                      u'Lietuvos Respublikos \u017eem\u0117s reformos \u012fstatymas',
                      u'Lietuvos Respublikos saugom\u0173 teritorij\u0173 \u012fstatymas',
                      u'Lietuvos Respublikos teism\u0173 \u012fstatymas',
                      u'Lietuvos Respublikos teritorij\u0173 planavimo \u012fstatymas',
                      u'Lietuvos Respublikos \u017eem\u0117s \u012fstatymas',
                      u'Lietuvos Respublikos nekilnojamojo kult\u016bros paveldo apsaugos \u012fstatymas',
                  ],
              },
              {
                  'client': u'VšĮ „Vilniaus metro“',
                  'law_projects': [
                      u'Lietuvos Respublikos gele\u017einkeli\u0173 transporto kodekso patvirtinimo, \u012fsigaliojimo ir taikymo \u012fstatymas',
                      u'Lietuvos Respublikos metropoliteno \u012fstatymas',
                  ],
              },
          ],
          'source_url': u'http://localhost/test.html',
          'comments': u'',
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

    def parse_law_projects(self, html, fn):
        response = XmlResponse('http://localhost/test.html',
                               body='<book>%s</book>' % html)
        node = response.css('entry')[0]
        return fn(node)

    def parse_lobbyist(self, html, fn):
        response = HtmlResponse('http://localhost/test.html',
                                body='<book>%s</book>' % html)
        rows = response.css('row')
        item = fn(response, rows)
        actual = dict(item)
        return actual

    def test_parse_number(self):
        self.run_examples(self.number_examples, self.parse_field,
                          self.spider._parse_number)

    def test_parse_name(self):
        self.run_examples(self.name_examples, self.parse_field,
                          self.spider._parse_name)

    def test_parse_law_projects(self):
        self.run_examples(self.law_projects_examples, self.parse_law_projects,
                          self.spider._parse_law_projects)

    def test_parse_lobbyist(self):
        self.run_examples(self.lobbyist_examples, self.parse_lobbyist,
                          self.spider._parse_lobbyist)

    def test_split_projects(self):
        self.assertEqual(self.spider._split_projects(' '), [])
        self.assertEqual(self.spider._split_projects(' - '), [])
        self.assertEqual(self.spider._split_projects(' foo '), ['foo'])
        self.assertEqual(self.spider._split_projects('foo.'), ['foo'])
        self.assertEqual(self.spider._split_projects('foo; bar.'), ['foo; bar'])
        self.assertEqual(self.spider._split_projects('foo;\nbar.'), ['foo', 'bar'])
        self.assertEqual(self.spider._split_projects('1) foo;\n2) bar.'), ['foo', 'bar'])

    def test_clean_list_item(self):
        self.assertEqual(self.spider._clean_list_item('foo'), 'foo')
        self.assertEqual(self.spider._clean_list_item(' foo '), 'foo')
        self.assertEqual(self.spider._clean_list_item('foo.'), 'foo')
        self.assertEqual(self.spider._clean_list_item('foo;'), 'foo')
        self.assertEqual(self.spider._clean_list_item('1) foo'), 'foo')
        self.assertEqual(self.spider._clean_list_item('20)  foo'), 'foo')
        self.assertEqual(self.spider._clean_list_item('1)  foo'), 'foo')
        self.assertEqual(self.spider._clean_list_item('1.  foo'), 'foo')

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

    def test_parse_declaration_xml_4_columns(self):
        # this format was used for 2012 and 2013 declarations
        response = XmlResponse('http://old.vtek.lt/vtek/.../deklaracija2012.doc',
                               body=fixture('lobist_veiklos_atatskaita_2012.doc.xml'))
        response.request = scrapy.Request(response.url)
        response.request.meta['year'] = '2012'

        items = list(self.spider.parse_declaration_xml(response))
        self.assertEqual(len(items), 30)
        self.assertEqual(items[0]['name'], 'ROMAS STUMBRYS')
        self.assertEqual(items[0]['comments'], u'Lobistinės veiklos nevykdė')

    def test_parse_declaration_xml_5_columns(self):
        # this format was used for 2014 declarations
        response = XmlResponse('http://old.vtek.lt/vtek/.../deklaracija2014.doc',
                               body=fixture('Info_apie_lobistu_ataskaitas_2014_2015_04_08.doc.xml'))
        response.request = scrapy.Request(response.url)
        response.request.meta['year'] = '2014'

        items = list(self.spider.parse_declaration_xml(response))
        self.assertEqual(len(items), 34)
        self.assertEqual(items[0]['name'], 'ROMAS STUMBRYS')
        self.assertEqual(items[-1]['name'], u'UAB INLINEN')
        self.assertEqual(items[-1]['comments'], u'Lobistinės veiklos nevykdė')
