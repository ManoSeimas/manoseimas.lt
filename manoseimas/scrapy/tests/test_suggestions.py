# -*- coding: utf-8 -*-
import unittest

from scrapy.http import HtmlResponse

from manoseimas.scrapy.items import Suggestion
from manoseimas.scrapy.spiders.suggestions import SuggestionsSpider
from manoseimas.scrapy.tests.utils import fixture


class TestHelpers(unittest.TestCase):

    def test_truncate(self):
        f = SuggestionsSpider._truncate
        self.assertEqual(f('abc', maxlen=5), 'abc')
        self.assertEqual(f('abcde', maxlen=5), 'abcde')
        self.assertEqual(f('abcdef', maxlen=5), 'ab...')

    def test_format_columns_for_log(self):
        f = SuggestionsSpider._format_columns_for_log
        self.assertEqual(f(['foo', 'bar', 'baz']), 'foo | bar | baz')
        self.assertEqual(f(['seriously' * 100, 'ha']),
                         'seriouslyseriouslyseriouslyseriouslyseriouslyse... | ha')

    def test_normalize_whitespace(self):
        f = SuggestionsSpider._normalize_whitespace
        self.assertEqual(f(u'  fooo \r\n bar  '), u'fooo bar')

    def test_extract_text(self):
        def f(html):
            response = HtmlResponse('http://localhost/test.html',
                                    body='<body>%s</body>' % html)
            node = response.xpath('body')[0]
            return SuggestionsSpider._extract_text(node)
        self.assertEqual(f('<td>\r\n<p> foo <span> bar </span> baz \r\n</td>'),
                         u'foo bar baz')


class TestTableParsing(unittest.TestCase):

    def check(self, html, expected):
        response = HtmlResponse('http://localhost/test.html',
                                body='<body>%s</body>' % html)
        table = response.xpath('//table')[0]
        spider = SuggestionsSpider()
        actual = list(spider._parse_table(table, response.url))
        self.assertEqual(actual, expected)

    def test_good_table(self):
        self.check('''
            <table>
              <tr>
                <td rowspan=2>Eil Nr.</td>
                <td rowspan=2>Pasiūlymo teikėjas, data</td>
                <td colspan=3>Siūloma keisti</td>
                <td rowspan=2>Pasiūlymo turinys</td>
                <td rowspan=2>Komiteto nuomonė</td>
                <td rowspan=2>Argumentai, pagrindžiantys nuomonę</td>
              </tr>
              <tr>
                <td>Str.</td>
                <td>Str. d.</td>
                <td>P.</td>
              </tr>
              <tr>
                <td>1.</td>
                <td> <p> <span> STT (2015-10-09, raštas Nr. g-2015-123) </span> </p> </td>
                <td></td>
                <td></td>
                <td></td>
                <td>Blah blah blah</td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td>Blah blah blah</td>
                <td> <p> <span> Pritarti. </span> <p> </td>
                <td></td>
              </tr>
              <tr>
                <td>2.</td>
                <td> <p> <span> LR Vyriausybė, 2015-10-09 </span> </p> </td>
                <td></td>
                <td></td>
                <td></td>
                <td>Blah blah blah</td>
                <td> <p> <span> Pritarti iš dalies. </span> <p> </td>
                <td></td>
              </tr>
            </table>
        ''', [
            Suggestion(
                submitter_and_date=u'STT (2015-10-09, raštas Nr. g-2015-123)',
                opinion=u'',
                source_url='http://localhost/test.html',
            ),
            Suggestion(
                submitter_and_date=u'STT (2015-10-09, raštas Nr. g-2015-123)',
                opinion=u'Pritarti',
                source_url='http://localhost/test.html',
            ),
            Suggestion(
                submitter_and_date=u'LR Vyriausybė, 2015-10-09',
                opinion=u'Pritarti iš dalies',
                source_url='http://localhost/test.html',
            ),
        ])

    def test_table_with_thead(self):
        self.check('''
            <table>
              <thead>
                <tr>
                  <td rowspan=2>Eil Nr.</td>
                  <td rowspan=2>Pasiūlymo teikėjas, data</td>
                  <td colspan=3>Siūloma keisti</td>
                  <td rowspan=2>Pasiūlymo turinys</td>
                  <td rowspan=2>Komiteto nuomonė</td>
                  <td rowspan=2>Argumentai, pagrindžiantys nuomonę</td>
                </tr>
                <tr>
                  <td>Str.</td>
                  <td>Str. d.</td>
                  <td>P.</td>
                </tr>
              </thead>
              <tr>
                <td>1.</td>
                <td> <p> <span> STT (2015-10-09, raštas Nr. g-2015-123) </span> </p> </td>
                <td></td>
                <td></td>
                <td></td>
                <td>Blah blah blah</td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td>Blah blah blah</td>
                <td> <p> <span> Pritarti. </span> <p> </td>
                <td></td>
              </tr>
              <tr>
                <td>2.</td>
                <td> <p> <span> LR Vyriausybė, 2015-10-09 </span> </p> </td>
                <td></td>
                <td></td>
                <td></td>
                <td>Blah blah blah</td>
                <td> <p> <span> Pritarti iš dalies. </span> <p> </td>
                <td></td>
              </tr>
            </table>
        ''', [
            Suggestion(
                submitter_and_date=u'STT (2015-10-09, raštas Nr. g-2015-123)',
                opinion=u'',
                source_url='http://localhost/test.html',
            ),
            Suggestion(
                submitter_and_date=u'STT (2015-10-09, raštas Nr. g-2015-123)',
                opinion=u'Pritarti',
                source_url='http://localhost/test.html',
            ),
            Suggestion(
                submitter_and_date=u'LR Vyriausybė, 2015-10-09',
                opinion=u'Pritarti iš dalies',
                source_url='http://localhost/test.html',
            ),
        ])

    def test_wrong_table(self):
        self.check('''
            <table border=0>
              <tr>
                <td>Blah blah blah just some text that's a table for no reason.</td>
              </tr>
            </table>
        ''', [])


class TestTableDiscrimination(unittest.TestCase):

    def assertInteresting(self, html):
        self.check(html, True)

    def assertNotInteresting(self, html):
        self.check(html, False)

    def check(self, html, expected):
        response = HtmlResponse('http://localhost/test.html',
                                body='<body>%s</body>' % html)
        table = response.xpath('//table')[0]
        spider = SuggestionsSpider()
        actual = spider._is_table_interesting(table, response.url)
        self.assertEqual(actual, expected)

    def test_interesting(self):
        self.assertInteresting('''
            <table>
              <tr>
                <td rowspan=2>Eil Nr.</td>
                <td rowspan=2>Pasiūlymo teikėjas, data</td>
                <td colspan=3>Siūloma keisti</td>
                <td rowspan=2>Pasiūlymo turinys</td>
                <td rowspan=2>Komiteto nuomonė</td>
                <td rowspan=2>Argumentai, pagrindžiantys nuomonę</td>
              </tr>
              <tr>
                <td>Str.</td>
                <td>Str. d.</td>
                <td>P.</td>
              </tr>
            </table>
        ''')

    def test_committee_decision_table(self):
        self.assertNotInteresting('''
            <table border=0>
              <tr>
                <td>Eil Nr.</td>
                <td>Projekto Nr.</td>
                <td>Teisės akto projekto pavadinimas</td>
                <td>Teikia</td>
                <td>Siūlo</td>
                <td>Svarstymo mėnuo</td>
              </tr>
            </table>
        ''')

    def test_weird_paragraph(self):
        self.assertNotInteresting('''
            <table border=0>
              <tr>
                <td>Blah blah blah just some text that's a table for no reason.</td>
              </tr>
            </table>
        ''')

    def test_committee_decision_list(self):
        self.assertNotInteresting('''
            <table>
              <tr>
                <td>Dėl kažko:</td>
                <td>Blah blah blah blah blah.</td>
              </tr>
            </table>
        ''')


class TestRowParsing(unittest.TestCase):

    def test_parse_submitter(self):
        f = SuggestionsSpider._parse_submitter
        self.assertEqual(f(u''), u'')
        self.assertEqual(f(u'Seimo kanceliarijos Teisės departamentas, 2015-10-09'),
                         u'Seimo kanceliarijos Teisės departamentas, 2015-10-09')

    def test_parse_opinion(self):
        f = SuggestionsSpider._parse_opinion
        self.assertEqual(f(u''), u'')
        self.assertEqual(f(u'Pritarti'), u'Pritarti')
        self.assertEqual(f(u'Pritarti.'), u'Pritarti')

    def check(self, html, *expected):
        response = HtmlResponse('http://localhost/test.html',
                                body='<body><table>%s</table></body>' % html)
        cells = response.xpath('//tr[1]/td')
        indexes = [0, 1, 2, 5, 6, 7]
        actual = list(SuggestionsSpider._parse_row(cells, indexes))
        self.assertEqual(list(expected), actual)

    def test_parse_row(self):
        self.check('''
            <tr>
              <td>3.</td>
              <td> <p> <span> STT (2015-10-09, raštas Nr. g-2015-123) </span> </p> </td>
              <td></td>
              <td></td>
              <td></td>
              <td>Blah blah blah</td>
              <td> <p> <span> Pritarti. </span> <p> </td>
              <td></td>
            </tr>
        ''', Suggestion(
            submitter_and_date=u'STT (2015-10-09, raštas Nr. g-2015-123)',
            opinion=u'Pritarti',
        ))


class TestTableColumnParsing(unittest.TestCase):

    def check(self, html, *expected_for_each_row):
        response = HtmlResponse('http://localhost/test.html',
                                body='<body>%s</body>' % html)
        table = response.xpath('//table')[0]
        for row, expected in enumerate(expected_for_each_row, 1):
            result = SuggestionsSpider._parse_table_columns(table, row=row)
            self.assertEqual(result, expected)

    def test_simple_table(self):
        # Note: the tables we are parsing don't use <th>.
        self.check('''
            <table>
              <tr>
                <td>One</td>
                <td>Two</td>
              </tr>
              <tr>
                <td>data</td>
                <td>data</td>
              </tr>
            </table>
        ''', [
            'One', 'Two',
        ])

    def test_colspan(self):
        self.check('''
            <table>
              <tr>
                <td rowspan=2>One</td>
                <td colspan=3>Two</td>
                <td rowspan=2>Three</td>
              </tr>
              <tr>
                <td>Two.1</td>
                <td>Two.2</td>
                <td>Two.3</td>
              </tr>
              <tr>
                <td>data</td>
                <td>data</td>
                <td>data</td>
                <td>data</td>
                <td>data</td>
              </tr>
            </table>
        ''', [
            'One', 'Two', 'Three',
        ], [
            'Two.1', 'Two.2', 'Two.3',
        ])

    def test_thead(self):
        # Yes, the tables I've seen have <thead> but no <tbody>.
        self.check('''
            <table>
              <thead>
                <tr>
                  <td>One</td>
                  <td>Two</td>
                </tr>
              </thead>
              <tr>
                <td>data</td>
                <td>data</td>
              </tr>
            </table>
        ''', [
            'One', 'Two',
        ])

    def test_complex_titles(self):
        # Note: the tables we are parsing don't use <th>.
        self.check('''
            <table>
              <tr>
                <td> <p> <span>Multi</span>\n word </p></td>
                <td> titles </td>
              </tr>
            </table>
        ''', [
            'Multi word', 'titles',
        ])


class TestRowspanColspanHandling(unittest.TestCase):

    def check(self, html, expected):
        response = HtmlResponse('http://localhost/test.html',
                                body='<body>%s</body>' % html)
        rows = response.xpath('//tr')
        result = SuggestionsSpider._process_rowspan_colspan(rows)
        actual = [[td.xpath('text()').extract()[0] for td in tr] for tr in result]
        self.assertEqual(actual, expected)

    def test_no_colspan_rowspan(self):
        self.check('''
            <table>
                <tr>
                    <td>A</td>
                    <td>B</td>
                </tr>
                <tr>
                    <td>C</td>
                    <td>D</td>
                </tr>
            </table>
        ''', [
            ['A', 'B'],
            ['C', 'D'],
        ])

    def test_colspan(self):
        self.check('''
            <table>
                <tr>
                    <td>A</td>
                    <td colspan="2">B</td>
                    <td>C</td>
                </tr>
                <tr>
                    <td colspan="3">D</td>
                    <td>E</td>
                </tr>
            </table>
        ''', [
            ['A', 'B', 'B', 'C'],
            ['D', 'D', 'D', 'E'],
        ])

    def test_rowspan(self):
        self.check('''
            <table>
                <tr>
                    <td>A</td>
                    <td rowspan="2">B</td>
                    <td>C</td>
                </tr>
                <tr>
                    <td>D</td>
                    <td>E</td>
                </tr>
                <tr>
                    <td>F</td>
                    <td>G</td>
                    <td>H</td>
                </tr>
            </table>
        ''', [
            ['A', 'B', 'C'],
            ['D', 'B', 'E'],
            ['F', 'G', 'H'],
        ])

    def test_rowspan_first_column(self):
        self.check('''
            <table>
                <tr>
                    <td rowspan="2">A</td>
                    <td>B</td>
                    <td>C</td>
                </tr>
                <tr>
                    <td>D</td>
                    <td>E</td>
                </tr>
                <tr>
                    <td>F</td>
                    <td>G</td>
                    <td>H</td>
                </tr>
            </table>
        ''', [
            ['A', 'B', 'C'],
            ['A', 'D', 'E'],
            ['F', 'G', 'H'],
        ])

    def test_rowspan_last_column(self):
        self.check('''
            <table>
                <tr>
                    <td>A</td>
                    <td>B</td>
                    <td rowspan="2">C</td>
                </tr>
                <tr>
                    <td>D</td>
                    <td>E</td>
                </tr>
                <tr>
                    <td>F</td>
                    <td>G</td>
                    <td>H</td>
                </tr>
            </table>
        ''', [
            ['A', 'B', 'C'],
            ['D', 'E', 'C'],
            ['F', 'G', 'H'],
        ])

    def test_rowspan_more_than_two(self):
        self.check('''
            <table>
                <tr>
                    <td>A</td>
                    <td rowspan="3">B</td>
                    <td>C</td>
                </tr>
                <tr>
                    <td>D</td>
                    <td>E</td>
                </tr>
                <tr>
                    <td>F</td>
                    <td>G</td>
                </tr>
            </table>
        ''', [
            ['A', 'B', 'C'],
            ['D', 'B', 'E'],
            ['F', 'B', 'G'],
        ])


class TestSuggestionsSpider(unittest.TestCase):

    def test_parse_document(self):
        response = HtmlResponse('http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=1076487&p_tr2=2',
                                body=fixture('suggestion_1076487.html'))
        spider = SuggestionsSpider()
        items = list(spider.parse_document(response))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['submitter_and_date'], u'Seimo kanceliarijos Teisės departamentas, 2015-09-08')
        self.assertEqual(items[0]['opinion'], 'Pritarti')
        self.assertEqual(items[0]['source_url'], response.url)

    def test_empty_rows(self):
        self.check('''
            <table>
              <tr>
                <td rowspan=2>Eil Nr.</td>
                <td rowspan=2>Pasiūlymo teikėjas, data</td>
                <td colspan=3>Siūloma keisti</td>
                <td rowspan=2>Pasiūlymo turinys</td>
                <td rowspan=2>Komiteto nuomonė</td>
                <td rowspan=2>Argumentai, pagrindžiantys nuomonę</td>
              </tr>
              <tr>
                <td>Str.</td>
                <td>Str. d.</td>
                <td>P.</td>
              </tr>
              <tr>
                <td>1.</td>
                <td></td> <!-- EMPTY! -->
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td> wat is even</td>
                <td></td>
              </tr>
              <tr>
                <td>2.</td>
                <td> <p> <span> LR Vyriausybė, 2015-10-09 </span> </p> </td>
                <td></td>
                <td></td>
                <td></td>
                <td>Blah blah blah</td>
                <td> <p> <span> Pritarti iš dalies. </span> <p> </td>
                <td></td>
              </tr>
            </table>
        ''', [
            Suggestion(
                submitter_and_date=u'LR Vyriausybė, 2015-10-09',
                opinion=u'Pritarti iš dalies',
                source_url='http://localhost/test.html',
            ),
        ])

    def check(self, html, expected):
        response = HtmlResponse('http://localhost/test.html',
                                body='<body><div>%s</div></body>' % html)
        spider = SuggestionsSpider()
        actual = list(spider.parse_document(response))
        self.assertEqual(actual, expected)

    def test_table_with_unexpected_thead(self):
        # Regression test for
        # WARNING: 2 empty rows discarded at http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=1022652&p_tr2=2
        response = HtmlResponse('http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=1022652&p_tr2=2',
                                body=fixture('suggestion_1022652.html'))
        spider = SuggestionsSpider()
        items = list(spider.parse_document(response))
        self.assertEqual(len(items), 6)

    def test_table_with_extra_colspans(self):
        # Regression data for bogus data due to unexpected colspans
        # (also blank row skipping)
        response = HtmlResponse('http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=1024338&p_tr2=2',
                                body=fixture('suggestion_1024338.html'))
        spider = SuggestionsSpider()
        items = list(spider.parse_document(response))
        self.assertEqual(items[-2]['opinion'], 'Pritarti')
