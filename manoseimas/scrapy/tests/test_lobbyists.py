# -*- coding: utf-8 -*-
import datetime
import unittest

from scrapy.http import HtmlResponse

from manoseimas.scrapy.items import Lobbyist
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.spiders.lobbyists import LobbyistsSpider
from manoseimas.scrapy.tests.utils import fixture


class TestLobbyistsSpider(unittest.TestCase):

    number_examples = [
        ('<td>1.</td>', {}),
        ('<td>35</td>', {}),
    ]

    name_examples = [
        ('<td>BRONIUS ANTANAS RASIMAS</td>', {
            'name': 'Bronius Antanas Rasimas',
        }),
        ('<td><a href="http://www.lamco.lt/">MYKOLAS JUOZAPAVIČIUS</a></td>', {
            'name': u'Mykolas Juozapavičius',
            'url': 'http://www.lamco.lt/',
        }),
        ('<td>NINA BARBORA EVANS 2012 02 21 sprendimu Nr. KS-16 (L) sustabdyta lobistinė veikla iki prašymo atnaujinti.</td>', {
            'name': 'Nina Barbora Evans',
            'status': u'2012 02 21 sprendimu Nr. KS-16 (L) sustabdyta lobistinė veikla iki prašymo atnaujinti.',
        }),
        ('<td>MINDAUGAS VOLDEMARAS<br /> 2015 03 04 sprendimu Nr. KS-20 (L) sustabdyta lobistinė veikla iki prašymo atnaujinti.</td>', {
            'name': 'Mindaugas Voldemaras',
            'status': u'2015 03 04 sprendimu Nr. KS-20 (L) sustabdyta lobistinė veikla iki prašymo atnaujinti.',
        }),
        ('<td><p><a href="http://www.ey.com/GLOBAL/content.nsf/Lithuania_E/Lithuania_Home">UAB "ERNST &amp; YOUNG BALTIC"</a></p><p>Gintautas Bartkus, Jonas Platelis</p></td>', {
            'name': 'UAB "ERNST & YOUNG BALTIC"',
            'representatives': 'Gintautas Bartkus, Jonas Platelis',
            'url': 'http://www.ey.com/GLOBAL/content.nsf/Lithuania_E/Lithuania_Home',
        }),
        ('<td><p><a href="http://www.blslawfirm.com/bls-lithuania/home">ADVOKATŲ PROFESINĖ BENDRIJA "BALTIC LEGAL SOLUTIONS LIETUVA"</a></p><p>Gytis Kaminskas, Gintautas Bartkus</p></td>', {
            'name': u'ADVOKATŲ PROFESINĖ BENDRIJA "BALTIC LEGAL SOLUTIONS LIETUVA"',
            'representatives': 'Gytis Kaminskas, Gintautas Bartkus',
            'url': 'http://www.blslawfirm.com/bls-lithuania/home',
        }),
        ('<td><p><a href="http://www.inlinen.eu/">UAB "INLINEN"</a></p><p>Linas Pečiulaitis</p></td>', {
            'name': 'UAB "INLINEN"',
            'representatives': u'Linas Pečiulaitis',
            'url': 'http://www.inlinen.eu/',
        }),
        ('<td><a href="http://www.juris.lt/">UAB "VOX JURIS"</a><br />2015-04-15 sprendimu Nr. KS-31 (L) lobistinė veikla nutraukta.</td>', {
            'name': 'UAB "VOX JURIS"',
            'url': 'http://www.juris.lt/',
            'status': u'2015-04-15 sprendimu Nr. KS-31 (L) lobistinė veikla nutraukta.',
        }),
        ('<td><p>VŠĮ "MOKESČIŲ IR VERSLO PROCESŲ ADMINISTRAVIMO CENTRAS"</p><p>Sandra Šarkauskaitė</p></td>', {
            'name': u'VŠĮ "MOKESČIŲ IR VERSLO PROCESŲ ADMINISTRAVIMO CENTRAS"',
            'representatives': u'Sandra Šarkauskaitė',
        }),
    ]

    company_code_examples = [
        ('<td>123456789</td>', {'company_code': '123456789'}),
        ('<td>&nbsp;</td>', {'company_code': ''}),
    ]

    inclusion_examples = [
        ('<td>2015 05 20 Nr. KS-36 (L)</td>', {
            'date_of_inclusion': datetime.date(2015, 05, 20),
            'decision': 'Nr. KS-36 (L)',
        }),
        ('<td>2012 10 02 Nr. KS - 108 (L)</td>', {
            'date_of_inclusion': datetime.date(2012, 10, 02),
            'decision': 'Nr. KS - 108 (L)',
        }),
        ('<td>2012 04 17 Nr. KS -22 (L)</td>', {
            'date_of_inclusion': datetime.date(2012, 04, 17),
            'decision': 'Nr. KS -22 (L)',
        }),
        ('<td style="text-align: center;">2011 12 06 Nr. KS - 75 (L)</td>', {
            'date_of_inclusion': datetime.date(2011, 12, 06),
            'decision': 'Nr. KS - 75 (L)',
        }),
        ('<td>2002 10 04 Nr. 23 (L)</td>', {
            'date_of_inclusion': datetime.date(2002, 10, 04),
            'decision': 'Nr. 23 (L)',
        }),
    ]

    lobbyist_examples = [
        ('''
            <tr>
            <td>13.</td>
            <td>
            <p><a href="http://www.gsk.lt/">UAB “GLAXOSMITHKLINE LIETUVA”</a></p>
            <p>Kęstutis Čereška, Armindas Varkala, Arnas Beržanskis, Vilius Kirvaitis</p>
            </td>
            <td>111785261</td>
            <td>2007 12 20 Nr. KS - 88 (L)</td>
            </tr>
        ''', {
            'name': u'UAB “GLAXOSMITHKLINE LIETUVA”',
            'url': 'http://www.gsk.lt/',
            'representatives': u'Kęstutis Čereška, Armindas Varkala, Arnas Beržanskis, Vilius Kirvaitis',
            'company_code': '111785261',
            'date_of_inclusion': datetime.date(2007, 12, 20),
            'decision': 'Nr. KS - 88 (L)',
            'source_url': 'http://localhost/test.html',
            'raw_data': u'''
                <tr>
                <td>13.</td>
                <td>
                <p><a href="http://www.gsk.lt/">UAB “GLAXOSMITHKLINE LIETUVA”</a></p>
                <p>Kęstutis Čereška, Armindas Varkala, Arnas Beržanskis, Vilius Kirvaitis</p>
                </td>
                <td>111785261</td>
                <td>2007 12 20 Nr. KS - 88 (L)</td>
                </tr>
            '''.strip().replace('\n    ', '\n'),
        }),
    ]

    maxDiff = None

    def setUp(self):
        self.spider = LobbyistsSpider()

    def run_examples(self, examples, wrapper, fn):
        for html, expected in examples:
            actual = wrapper(html, fn)
            if 'raw_data' in expected and 'raw_data' in actual:
                # let's see a useful diff of these
                expected['raw_data'] = self.fixup_libxml2(expected['raw_data'])
                actual['raw_data'] = self.fixup_libxml2(actual['raw_data'])
                self.assertEqual(expected['raw_data'], actual['raw_data'])
            self.assertEqual(expected, actual)

    def fixup_libxml2(self, html):
        # Older libxml2 versions destroy some of the whitespace when you
        # parse and convert the html tree back to a string.  This causes
        # test failures on Travis CI.
        return html.replace('<tr><td>', '<tr>\n            <td>')

    def parse_field(self, html, fn):
        response = HtmlResponse('http://localhost/test.html',
                                body='<table><tr>%s</tr></table>' % html)
        row = response.css('tr')[0]
        node = response.css('td')[0]
        lobbyist = Loader(self.spider, response, Lobbyist(), row)
        lobbyist.add_value(None, fn(node))
        item = lobbyist.load_item()
        actual = dict(item)
        return actual

    def parse_row(self, html, fn):
        response = HtmlResponse('http://localhost/test.html',
                                body='<table>%s</table>' % html)
        row = response.css('tr')[0]
        item = fn(response, row)
        actual = dict(item)
        return actual

    def test_parse_number(self):
        self.run_examples(self.number_examples, self.parse_field,
                          self.spider._parse_number)

    def test_parse_name(self):
        self.run_examples(self.name_examples, self.parse_field,
                          self.spider._parse_name)

    def test_parse_company_code(self):
        self.run_examples(self.company_code_examples, self.parse_field,
                          self.spider._parse_company_code)

    def test_parse_inclusion(self):
        self.run_examples(self.inclusion_examples, self.parse_field,
                          self.spider._parse_inclusion)

    def test_parse_lobbyist(self):
        self.run_examples(self.lobbyist_examples, self.parse_row,
                          self.spider._parse_lobbyist)

    def test_maybe_titlecase_fixes_person_names(self):
        self.assertEqual(self.spider.maybe_titlecase(u'ALGIRDAS JUŠKYS'), u'Algirdas Juškys')
        self.assertEqual(self.spider.maybe_titlecase(u'BRONIUS ANTANAS RASIMAS'), u'Bronius Antanas Rasimas')

    def test_maybe_titlecase_leaves_company_names_alone(self):
        for name in ['UAB "VOX JURIS"',
                     u'VŠĮ "MOKESČIŲ IR VERSLO PROCESŲ ADMINISTRAVIMO CENTRAS"',
                     u'ADVOKATŲ PROFESINĖ BENDRIJA "BALTIC LEGAL SOLUTIONS LIETUVA"',
                     u'UAB “GLAXOSMITHKLINE LIETUVA”']:
            self.assertEqual(self.spider.maybe_titlecase(name), name)

    def test_parse(self):
        response = HtmlResponse('www.vtek.lt/index.php/deklaravimas', body=fixture('vtek_deklaravimas.html'))
        items = list(self.spider.parse(response))
        self.assertEqual(len(items), 35)
        self.assertEqual(items[0]['name'], 'Romas Stumbrys')
        self.assertEqual(items[-1]['name'], 'Arnas Marcinkus')
