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
                submitter=u'Lietuvos Respublikos specialiųjų tyrimų tarnyba',
                date=u'2015-10-09',
                document=u'raštas Nr. g-2015-123',
                opinion=u'',
                source_url='http://localhost/test.html',
                raw=u'STT (2015-10-09, raštas Nr. g-2015-123)',
            ),
            Suggestion(
                submitter=u'Lietuvos Respublikos specialiųjų tyrimų tarnyba',
                date=u'2015-10-09',
                document=u'raštas Nr. g-2015-123',
                opinion=u'Pritarti',
                source_url='http://localhost/test.html',
                raw=u'STT (2015-10-09, raštas Nr. g-2015-123)',
            ),
            Suggestion(
                submitter=u'Lietuvos Respublikos Vyriausybė',
                date=u'2015-10-09',
                document=u'',
                opinion=u'Pritarti iš dalies',
                source_url='http://localhost/test.html',
                raw=u'LR Vyriausybė, 2015-10-09',
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
                submitter=u'Lietuvos Respublikos specialiųjų tyrimų tarnyba',
                date=u'2015-10-09',
                document=u'raštas Nr. g-2015-123',
                opinion=u'',
                source_url='http://localhost/test.html',
                raw=u'STT (2015-10-09, raštas Nr. g-2015-123)',
            ),
            Suggestion(
                submitter=u'Lietuvos Respublikos specialiųjų tyrimų tarnyba',
                date=u'2015-10-09',
                document=u'raštas Nr. g-2015-123',
                opinion=u'Pritarti',
                source_url='http://localhost/test.html',
                raw=u'STT (2015-10-09, raštas Nr. g-2015-123)',
            ),
            Suggestion(
                submitter=u'Lietuvos Respublikos Vyriausybė',
                date=u'2015-10-09',
                document=u'',
                opinion=u'Pritarti iš dalies',
                source_url='http://localhost/test.html',
                raw=u'LR Vyriausybė, 2015-10-09',
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


class TestSubmitterParsing(unittest.TestCase):

    examples = [
        (u'',
         {'submitter': '',
          'date': '',
          'document': ''}),
        (u'Seimo kanceliarijos Teisės departamentas, 2015-10-09',
         {'submitter': u'Seimo kanceliarijos Teisės departamentas',
          'date': '2015-10-09',
          'document': ''}),
        (u'Submitter (2015-10-12)',
         {'submitter': u'Submitter',
          'date': '2015-10-12',
          'document': ''}),
        (u'Submitter ( 2015-10-12 )',
         {'submitter': u'Submitter',
          'date': '2015-10-12',
          'document': ''}),
        (u'Submitter ( 2015-10-12, nutarimas Nr. 123)',
         {'submitter': u'Submitter',
          'date': '2015-10-12',
          'document': u'nutarimas Nr. 123'}),
        (u'Submitter, 2015 10 12 Nutarimas Nr. 42',
         {'submitter': u'Submitter',
          'date': '2015-10-12',
          'document': 'Nutarimas Nr. 42'}),
        (u'Submitter2015-10-12',
         {'submitter': u'Submitter',
          'date': '2015-10-12',
          'document': ''}),
        (u'Submitter, 20151012 (Nr.123 )',
         {'submitter': u'Submitter',
          'date': '2015-10-12',
          'document': 'Nr.123'}),
        (u'Submitter, 2015-10-12 Nr. XIIP-1234(5)',
         {'submitter': u'Submitter',
          'date': '2015-10-12',
          'document': 'Nr. XIIP-1234(5)'}),
        (u'BFK 2012-12 -12 d.',
         {'submitter': u'BFK',
          'date': '2012-12-12',
          'document': ''}),
        (u'Submitter 2013 - 09- 02',
         {'submitter': u'Submitter',
          'date': '2013-09-02',
          'document': ''}),
        (u'Generalinė prokuratūra 2013-1 1-07',
         {'submitter': u'Lietuvos Respublikos generalinė prokuratūra',
          'date': '2013-11-07',
          'document': ''}),
        (u'Lietuvos savivaldybių asociacija 2014-5-29',
         {'submitter': u'Lietuvos savivaldybių asociacija',
          'date': '2014-05-29',
          'document': ''}),
        (u'Seimo kanceliarijos Teisės departamentas(2013-08-0 2 )',
         {'submitter': u'Seimo kanceliarijos Teisės departamentas',
          'date': '2013-08-02',
          'document': ''}),
        (u'Ekonomikos komitetas, 2015 m. rugsėjo 16 d. išvada Nr. 108-P-22',
         {'submitter': u'Ekonomikos komitetas',
          'date': '2015-09-16',
          'document': u'išvada Nr. 108-P-22'}),
        (u"Žemės ūkio ministerija 2013-05-03 1MS-34-(11.27)",
         {'submitter': u'Žemės ūkio ministerija',
          'date': '2013-05-03',
          'document': '1MS-34-(11.27)'}),
        (u"Darbo grupė viešojo sektoriaus audito sistemai tobulinti (sudaryta Lietuvos Respublikos Seimo valdybos 2013 m. gegužės 29 d. sprendimu Nr. SV-S-255) 2013-10-15",
         {'submitter': u'Darbo grupė viešojo sektoriaus audito sistemai tobulinti',
          'date': '2013-10-15',
          'document': ''}),
        (u'Durpių įmonių asociacija „Lietuviškos durpės“ Ruošė: Ginutis Juozapavičius G-2013-6053',
         {'submitter': u'Durpių įmonių asociacija „Lietuviškos durpės“ Ruošė: Ginutis Juozapavičius',
          'date': '',
          'document': u'G-2013-6053'}),
        (u'Lietuvos Aukščiausiasis teismas 2013-04 XIP-3018',
         {'submitter': u'Lietuvos Aukščiausiasis Teismas',
          'date': '',
          'document': u'XIP-3018'}),
        (u"Lietuvos Respublikos vyriausybės Nutarimas Nr. 441",
         {'submitter': u"Lietuvos Respublikos Vyriausybė",
          'date': '',
          'document': u'Nutarimas Nr. 441'}),
        (u"Lietuvos Respublikos vyriausybės nutarimas Nr. 441",
         {'submitter': u"Lietuvos Respublikos Vyriausybė",
          'date': '',
          'document': u'nutarimas Nr. 441'}),
        (u"Lietuvos Respublikos vyriausybė, 2013m. lapkričio 27 d. nutarimas Nr. XIIP-1087",
         {'submitter': u"Lietuvos Respublikos Vyriausybė",
          'date': '2013-11-27',
          'document': u'nutarimas Nr. XIIP-1087'}),
        (u"Lietuvos Respublikos Vyriausybė, (Nutarimas Nr. 1403), 2014-12-15",
         {'submitter': u"Lietuvos Respublikos Vyriausybė",
          'date': '2014-12-15',
          'document': u'Nutarimas Nr. 1403'}),
        (u"Vyriausybės nutarimas Nr. 545 (2013-06-12)",
         {'submitter': u"Lietuvos Respublikos Vyriausybė",
          'date': '2013-06-12',
          'document': u'nutarimas Nr. 545'}),
        (u"Vyriausybė (nut. Nr.159; 2014-02-19)",
         {'submitter': u"Lietuvos Respublikos Vyriausybė",
          'date': '2014-02-19',
          'document': u'nut. Nr.159'}),
        (u"Specialiųjų tyrimų tarnybos antikorupcinio vertinimo išvada 2013-02-05",
         {'submitter': u"Lietuvos Respublikos specialiųjų tyrimų tarnyba",
          'date': '2013-02-05',
          'document': u''}),
    ]

    def test(self):
        for example, expected in self.examples:
            actual = SuggestionsSpider._parse_submitter(example)
            self.assertEqual(actual.pop('raw'), example)
            self.assertEqual(actual, expected)

    @unittest.skip("Not implemented yet")
    def test_parse_submitter_unhandled_cases(self):
        f = SuggestionsSpider._parse_submitter
        self.assertEqual(f(u'Lietuvos savivaldybių asociacija (Nr. G-2013-10370)'),
                         {'submitter': u'Lietuvos savivaldybių asociacija',
                          'date': '',
                          'document': 'Nr. G-2013-10370'})
        self.assertEqual(f(u'Seimo kanceliarijos Teisės departamen tas 2013-13-05'),
                         {'submitter': u'Seimo kanceliarijos Teisės departamen tas',
                          'date': '',
                          'document': ' 2013-13-05'})


class TestRowParsing(unittest.TestCase):

    def test_clean_opinion(self):
        f = SuggestionsSpider._clean_opinion
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
            submitter=u'Lietuvos Respublikos specialiųjų tyrimų tarnyba',
            date=u'2015-10-09',
            document=u'raštas Nr. g-2015-123',
            opinion=u'Pritarti',
            raw=u'STT (2015-10-09, raštas Nr. g-2015-123)',
        ))


class TestSubmitterCleaning(unittest.TestCase):

    # Map expected value to a list of input values that should produce it.
    # It's also expected that the cleaning function is idempotent, so the
    # expected value itself is implicitly added to the input value list.
    examples = {
        # Blank values get passed through
        u'': [],
        u'-': [],
        # When you split "name (date, document no)" or "name, date" you end up
        # with trailing " (" or ", ".
        u'Teisės institutas': [
            u'Teisės institutas (',
            u'Teisės institutas, ',
        ],
        u'Žemės ūkio ministerija': [
            u'Žemės ūkio ministerija (gauta',
        ],
        u'Kristina M.': [
            u'Kristina M. (gauta el. paštu)',
        ],
        # Trailing incomplete date fragments are stripped
        u'UAB VVTF': [
            u'UAB VVTF 2014-',
            u'UAB VVTF, 2013-01-',
            u"UAB VVTF 12-12-06",
        ],
        # Trailing comments
        u"Konkurencijos taryba": [
            u"Konkurencijos taryba (sutrumpintai)",
        ],
        # Exception: trailing periods are sometimes necessary
        u"R. Jocienė ir kt.": [],
        # Often quotes are entered incorrectly
        u'AB „Amber grid“': [
            u'AB „Amber grid“',
            u'AB ,,Amber grid“',
        ],
        u'Lietuvos asociacija „Gyvastis“': [
            u'Lietuvos asociacija „Gyvastis',
        ],
        u'Asociacija „Lietuvos maisto pramonė“': [
            u"Asociacija „Lietuvos maisto pramonė",
        ],
        # Spacing after initials
        u"Etninės kultūros globos tarybos pirmininkė D. Urbanavičienė": [
            u"Etninės kultūros globos tarybos pirmininkė D. Urbanavičienė",
            u"Etninės kultūros globos tarybos pirmininkė D.Urbanavičienė",
        ],
        # Hyphenation
        u'A. Drevinskas': [
            u'A.Drevin-skas',
            u'A. Drevinskas',
        ],
        # Hyphenation exceptions
        u'Pilietė A. Butkutė-Žverelo': [
            u'Pilietė A. Butkutė-Žverelo',
        ],
        u'Architektė-urbanistė A. Selemonaitė': [
            u'Architektė-urbanistė Agnė Selemonaitė',
        ],
        u'Koalicija „Moters teisės-visuotinės žmogaus teisės“': [
            u'Koalicija „Moters teisės-visuotinės žmogaus teisės“',
        ],
        # Name shortening
        u'V. Pavardenis': [
            u'Vytautas Pavardenis',
        ],
        u"Seimo narys Č. V. Stankevičius": [
            u"Seimo narys Česlovas Vytautas Stankevičius",
        ],
        u"Sveikatos reikalų komiteto neetatinė ekspertė Doc. Dr. A. Širinskienė": [
            u"Sveikatos reikalų komiteto neetatinė ekspertė Doc. Dr. Agnė Širinskienė",
        ],
        # Don't shorten when there's no surname
        u'Gintaras': [
            u'Gintaras',
        ],
        # Some people have trouble spelling 'departamentas'
        u'Europos teisės departamentas': [
            u'Europos teisės departa-menras',
        ],
        # Spaces are important
        u'Lietuvos Respublikos Prezidentės dekretas': [
            u'Lietuvos RespublikosPrezidentės dekretas',
        ],
        u"Sveikatos reikalų komiteto neetatinė ekspertė prof. R. Kalėdienė": [
            u"Sveikatos reikalų komiteto neetatinė ekspertė prof . R. Kalėdienė",
        ],
        u'Politikos mokslų intituto profesorė dr. D. Jankauskienė': [
            u'P olitikos mokslų intituto profesorė dr. D. Jankauskienė',
        ],
        # Typos
        u'VŠĮ „Žaliasis taškas“': [
            u'VŠĮ „Žaliais taškas“',
            u'VŠĮ „Žaliasis taškas“',
        ],
        u"VŠĮ Vilniaus universiteto ligoninės Santariškių klinikos": [
            u"VšĮ Vilnaius universiteto ligoninės Santariškių klinikos",
            u"VšĮ Vilniaus universiteto ligoninės Santariškių klinikos",
        ],
        # Different spellings
        u'Žuvininkystės įmonių asociacija „Lampetra“': [
            u'Žuvininkystės įmonių asociacija „LAMPETRA“',
            u'Žuvininkystės įmonių asociacija „Lampetra“',
        ],
        u'AB „Lesto“': [
            u'AB „Lesto“',
            u'AB LESTO',
        ],
        u"AB „Lietuvos dujos“": [
            u"AB „Lietuvos dujos“",
            u"AB Lietuvos dujos“",
        ],
        u"AB „Litgrid“": [
            u"AB „Litgrid“",
            u"AB Litgrid",
        ],
        u"AB „LOTOS Geonafta įmonių grupė“, UAB „Minijos nafta“, UAB „LL investicijos“": [
            u"AB „LOTOS Geonafta įmonių grupė“ UAB „Minijos nafta“, UAB „LL investicijos“",
            u"AB LOTOS Geonafta įmonių grupė, UAB „Minijos nafta“, UAB „LL investicijos“",
        ],
        u"Asociacija „Infobalt“": [
            u"Asociacija „INFOBALT“",
            u"Asociacija „Infobalt“",
        ],
        u"Asociacija „Investuotojų forumas“": [
            u"Asociacija „Investors‘ Forum,“",
            u"Asociacija „Investuotojų forumas“",
        ],
        u"Asociacija „Lietuvos antstolių rūmai“": [
            u"Asociacija „Lietuvos antstolių rūmai“",
            u"Asociacija Lietuvos antstolių rūmai",
        ],
        u"Audito komitetas": [
            u"Audito Komitetas",
            u"Audito komitetas",
        ],
        u"Biudžeto ir finansų komitetas": [
            u"Biudžeto ir finansų komitetas",
            u"Biudžeto ir finansų komitetas, 2012-12-12109-P-41(4)",
            u"Biudžeto ir finansų komitetas (patikslinta išvada)",
            u"Lietuvos Respublikos Seimo Biudžeto ir finansų komitetas",
            u"Lietuvos Respublikos Seimo biudžeto ir finansų komitetas",
        ],
        u"Darbo grupė viešojo sektoriaus audito sistemai tobulinti": [
            u"Darbo grupė viešojo sektoriaus audito sistemai tobulinti",
            u"Darbo grupė viešojo sektoriaus audito sistemai tobulinti (sudaryta Lietuvos Respublikos Seimo valdybos 2013 m. gegužės 29 d. sprendimu Nr. SV-S-255)",
            u"Darbo grupė viešojo sektoriaus audito sistemai tobulinti (sudaryta Lietuvos Respublikos Seimo valdybos ",
        ],
        u"Darbo saugos specialistų darbdavių asociacija": [
            u"Darbo saugos specialistų darbdavių asociacija",
            u"Darbų saugos specialistų darbdavių asociacija",
        ],
        u"Europos teisės departamentas": [
            u"Europos Teisės departamentas",
            u"Europos teisės departamentas",
            u"Europos Teisės departamentas išvada XIP-",
            u"Europos Teisės departamentas prie Lietuvos Respublikos teisingumo ministerijos",
            u"Europos teisės departamentas prie Lietuvos RespublikosTeisingumo ministerijos",
            u"Europos teisės departamentas prie Lietuvos Respublikos teisingumo ministerijos",
            u"Europos teisės departamentas prie Lietuvos Respublikos teisingumo ministrerijos",
            u"Europos teisės departamentas prie Lietuvos Respublikos vyriausybės",
            u"Europos Teisės departamentas prie LR Teisingumo ministerijos",
            u"Europos teisės departamentas prie LR Teisingumo ministerijos",
            u"Europos teisės departamentas prie LR teisingumo ministerijos",
            u"Europos Teisės departamentas prie LR TM",
            u"Europos teisės departamentas prie LR TM",
            u"Europos teisės departamentas prie TD",
            u"Europos teisės departamentas prie Teisingum 0 ministerijo s",
            u"Europos teisės departamentas prie Teisingumo ministerijas",
            u"Europos Teisės departamentas prie Teisingumo ministerijos",
            u"Europos teisės departamentas Prie Teisingumo ministerijos",
            u"Europos teisės departamentas prie Teisingumo ministerijos",
            u"Europos teisės departamentas, prie Teisingumo ministerijos",
            u"Europos teisės departamentasprie Teisingumo ministerijos",
            u"Europos teisės departamentas prie teisingumo ministerijos",
            u"Europos teisės departamentas, prie teisingumo ministerijos",
            u"Europos teisės departamentas prie Teisingumo ministerijos 2013-0",
            u"Europos teisės departamentas prie Teisingumo ministerijos dėl įstatymo projekto Nr. XIIP-970",
            u"Europos teisės departamentas prie Teisingumo ministerijos dėl projekto Nr. XIIP-288",
            u"Europos teisės departamentas prie TM",
            u"Europos teisės departamento",
            u"Europos teisės departamento išvada prie Teisingumo ministerijos",
            u"Europos teisės departamento prie LR Teisingumo ministerijos",
            u"Europos teisės departamento prie TM išvada",
            u"Europos teisės departametas",
        ],
        u"Lietuvos miško savininkų asociacija": [
            u"Lietuvos miško savininkų asociacija",
            u"Lietuvos miškų savininkų asociacija",
        ],
        u"Lietuvos nacionalinė vežėjų automobiliais asociacija „Linava“": [
            u"Lietuvos nacionalinė vežėjų asociacija LINAVA",
            u"Lietuvos nacionalinė vežėjų automobiliais asociacija „LINAVA“",
            u"Lietuvos nacionalinė vežėjų automobiliais asociacija LINAVA",
            u"Lietuvos nacionalinė vežėjų automobiliais asociacija „Linava“",
            u"Lietuvos nacionalinė vežėjų automobiliais asociacija „Linava“",
            u"„Linava“",
        ],
        u"Lietuvos nealkoholinių gėrimų gamintojų bei importuotojų asociacija": [
            u"Lietuvos nealkoholinių gėrimų gamintojų bei importuotojų asociacija",
            u"Lietuvos nealkoholinių gėrimų gamintojų ir importuotojų asociacija",
        ],
        u"Lietuvos pramonininkų konfederacija": [
            u"Lietuvos pramonininkų Konfederacija",
            u"Lietuvos pramonininkų konfederacija",
            u"Lietuvos pramoninkų konfederacija",
        ],
        u"Finansų ministerija": [
            u"Lietuvos Respublikos Finansų ministerija",
            u"Lietuvos Respublikos finansų ministerija",
        ],
        u"Lietuvos Respublikos generalinė prokuratūra": [
            u"Lietuvos Respublikos Generalinė prokuratūra",
            u"Lietuvos Respublikos generalinė prokuratūra",
            u"Generalinė prokuratūra",
        ],
        u"Lietuvos Respublikos specialiųjų tyrimų tarnyba": [
            u"Lietuvos Respublikos Specialiųjų tyrimų tarnyba tarnyb a",
            u"Lietuvos Respublikos Specialiųjų tyrimų tarnyba",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyb a",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyba (toliau– STT)",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyba 2012-",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyba",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyba, 2013-01-",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyba.",
            u"Lietuvos respublikos specialiųjų tyrimų tarnyba",
            u"LR Specialiųjų tyrimų tarnyba",
            u"Specialiųjų tyrimų tarnyba",
            u"STT",
            u'STT (',
            u'STT, ',
            u'STT 2014-',
            u'STT, 2013-01-',
        ],
        u"Teisingumo ministerija": [
            u"Lietuvos Respublikos Teisingumo ministerija",
            u"Lietuvos Respublikos teisingumo ministerija",
        ],
        u"Lietuvos Respublikos transporto priemonių draudikų biuras": [
            u"Lietuvos Respublikos Transporto priemonių draudikų biuras",
            u"Lietuvos Respublikos transporto priemonių draudikų biuras",
            u"Lietuvos transporto priemonių draudikų biuras",
        ],
        u"Ūkio ministerija": [
            u"Lietuvos Respublikos Ūkio ministerija",
            u"Lietuvos Respublikos ūkio ministerija",
        ],
        u"Lietuvos Respublikos vaiko teisių apsaugos kontrolieriaus įstaiga": [
            u"Lietuvos Respublikos Vaiko teisių apsaugos kontrolierius",
            u"Lietuvos Respublikos Vaiko teisių apsaugos kontrolės įstaiga",
            u"Lietuvos Respublikos vaiko teisių apsaugos kontrolieriaus įstaiga",
            u"Lietuvos Respublikos vaiko teisių apsaugos kontrolierius",
            u"Vaiko teisių apsaugos kontrolieriaus įstaiga",
            u"Vaiko teisių apsaugos kontrolierius",
            u"Vaiko teisių apsaugos kontrolierė",
            u"LR Vaiko teisių apsaugos kontrolierius",
        ],
        u"Lietuvos Respublikos valstybės saugumo departamentas": [
            u"Lietuvos Respublikos Valstybės saugumo departamentas",
            u"Lietuvos Respublikos saugumo departamentas",
            u"Lietuvos Respublikos valstybės saugumo departamentas",
            u"LR Valstybės saugumo departamentas",
            u"Valstybės saugumo departamentas",
        ],
        u"Lietuvos Respublikos vyriausioji rinkimų komisija": [
            u"Lietuvos Respublikos Vyriausioji rinkimų komisija",
            u"Lietuvos Respublikos vyriausioji rinkimų komisija",
            u"Vyriausioji rinkimų komisija",
        ],
        u"Lietuvos savivaldybių asociacija": [
            u"Lietuvos Savivaldybių asociacija",
            u"Lietuvos savivaldybių asociacija",
        ],
        u"Lietuvos Respublikos Prezidentė": [
            u"LR Prezidentė",
        ],
        u"Lietuvos Respublikos Prezidentės dekretas": [
            u"Lietuvos Respublikos Prezidentės dekretas",
        ],
        # Different capitalizations
        u"Legalaus verslo aljansas": [
            u"Legalaus Verslo aljansas",
        ],
        u"Lietuvos apeliacinis teismas": [
            u"Lietuvos Apeliacinis Teismas",
            u"Lietuvos Apeliacinis teismas",
            u"Lietuvos apeliacinis teismas",
            u"Apeliacinis teismas",
        ],
        u"Lietuvos advokatūra": [
            u"Lietuvos Advokatūra",
            u"Lietuvos advokatūra",
        ],
        u"Lietuvos karjerų asociacija": [
            u"LIETUVOS KARJERŲ ASOCIACIJA",
            u"Lietuvos karjerų asociacija",
        ],
        u"Vytauto Didžiojo universitetas": [
            u"Vytauto Didžiojo Universitetas",
            u"Vytauto Didžiojo universitetas",
        ],
        u'Marijampolės regiono plėtros taryba': [
            u'MARIJAMPOLĖS REGIONO PLĖTROS TARYBA',
        ],
        u"Teisėjų taryba": [
            u"Teisėjų Taryba",
            u"Teisėjų taryba",
        ],
        u"Lietuvos nepriklausomybės akto signataras Zigmas Vaišvila": [
            u"Lietuvos Nepriklausomybės Akto signataras Zigmas Vaišvila",
        ],
        u"Lietuvos nepriklausomybės akto signatarų klubas": [
            u"Lietuvos Nepriklausomybės Akto signatarų klubas",
        ],
        u"Lietuvos nepriklausomybės aktų signatarų klubo prezidentė B. Valionytė": [
            u"Lietuvos nepriklausomybės aktų signatarų klubo prezidentė B. Valionytė",
        ],
        u"Statybos ir architektūros teismo ekspertų sąjunga": [
            u"STATYBOS IR ARCHITEKTŪROS TEISMO EKSPERTŲ SĄJUNGA",
            u"Statybos ir architektūros teismo ekspertų sąjunga",
        ],
        # Just different
        u'Seimo kanceliarijos Teisės departamentas': [
            u"(TD)",
            u"LR Seimo kanceliarijos Teisės departamentas",
            u"LR Seimo kanceliarijos teisės departamentas",
            u"LRS Seimo kanceliarijos teisės departamentas",
            u"LRS Teisės departamentas",
            u"LRS kanceliarijos Teisės departamentas",
            u"Lietuvos Respublikos Seimo kanceliarijos Teisės departamentas",
            u"Seimo Kanceliarijos Teisės departamentas",
            u"Seimo Teisės departamentas",
            u"Seimo kancelarijos Teisės departamentas",
            u"Seimo kanceliarij os Teisės departamentas",
            u"Seimo kanceliarijos Teisės Departamentas",
            u"Seimo kanceliarijos Teisės departamantas, 2014-09išvada Nr. XIIP-",
            u"Seimo kanceliarijos Teisės departamentas (TD)",
            u"Seimo kanceliarijos Teisės departamentas 201-12-07",
            u"Seimo kanceliarijos Teisės departamentas 2011-05-10v",
            u"Seimo kanceliarijos Teisės departamentas 2014-05-2",
            u"Seimo kanceliarijos Teisės departamentas dėl įstatymo projekto Nr. XIIP-288",
            u"Seimo kanceliarijos Teisės departamentas dėl įstatymo projekto Nr. XIIP-970",
            u"Seimo kanceliarijos Teisės departamentas",
            u"Seimo kanceliarijos Teisės departamentas, 2014 Nr. XIIP-1309(2)-04-09",
            u"Seimo kanceliarijos Teisės departamentas, 2015-03-3",
            u"Seimo kanceliarijos Teisės departamentas, 2015-05-5",
            u"Seimo kanceliarijos Teisės departamento (TD) išvada",
            u"Seimo kanceliarijos Teisės departamento išvada",
            u"Seimo kanceliarijos Teisės departamento",
            u"Seimo kanceliarijos Teisės departamntas",
            u"Seimo kanceliarijos teisės departamentas",
            u"Seimo kanceliarijos teisės departamentas;",
            u"TD",
            u"Teisės departamentas",
            u'Seimo kanceliari-jos Teisės departa- mentas',
            u'Seimo kanceliarijos Teisės departamentas',
            u'Seimo kanceliari-jos Teisės departa-menta-mentas',
            u'Seimo kanceliari-jos Teisėsdepartamentas',
        ],
        u"Finansinių nusikaltimų tyrimo tarnyba prie Vidaus reikalų ministerijos": [
            u"Finansinių nusikaltimų tyrimo tarnyba prie Lietuvos Respublikos vidaus reikalų ministerijos",
            u"Finansinių nusikaltimų tyrimo tarnyba prie LR vidaus reikalų ministerijos",
            u"Finansinių nusikaltimų tyrimo tarnyba prie Vidaus reikalų ministerijos",
            u"Finansinių nusikaltimų tyrimų tarnyba prie Vidaus reikalų ministerijos",
        ],
        u"Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos": [
            u"Informacinės visuomenės komitetas",
            u"Informacinės visuomenės plėtros komitetas",
            u"Informacinės visuomenės plėtros komitetas prie SM",
            u"IVPK",
        ],
        u"Jungtinių Tautų vyriausiojo pabėgėlių komisaro regioninis Šiaurės Europos biuras": [
            u"JTVPK",
            u"Jungtinių Tautų vyriausiojo pabėgėlių komisaro regioninis Šiaurės Europos biuras (JTVPK)",
        ],
        u"Kauno miesto savivaldybės administracija": [
            u"Kauno miesto savivaldybės administracija",
            u"Kauno m. savivaldybės administracija",
        ],
        u"Lietuvos agrarinės ekonomikos institutas": [
            u"LAEI",
        ],
        u'Local American Working Group (LAWG)': [
            u'LAWG',
        ],
        u'Kultūros ministerija': [
            u'Kultūros ministerija',
            u'LR kultūros ministerija',
        ],
        u"Aplinkos ministerija": [
            u"Aplinkos ministerija",
            u"Lietuvos Respublikos aplinkos ministerija",
        ],
        u"Energetikos ministerija": [
            u"Energetikos ministerija",
            u"Lietuvos Respublikos Energetikos ministerija",
        ],
        u"Žemės ūkio ministerija": [
            u"LR Žemės ūkio ministerija",
            u"Lietuvos Respublikos žemės ūkio ministerija",
            u"Žemės ūkio ministerija",
            u"ŽŪM",
        ],
        u"Valstybinė mokesčių inspekcija prie Finansų ministerijos": [
            u"Valstybinė mokesčių inspekcija prie Finansų ministerijos",
            u"Valstybinė mokesčių inspekcija prie Lietuvos Respublikos finansų ministerijos",
            u"Valstybinė mokesčių inspekcija",
        ],
        u"Valstybinė teismo medicinos tarnyba prie Teisingumo ministerijos": [
            u"Valstybinė teismo medicinos tarnyba prie Teisingumo ministerijos",
            u"Valstybinė teismo medicinos tarnyba",
            u"Valstybinės teismo medicinos tarnyba prie Lietuvos Respublikos Teisingumo ministerijos",
        ],
        u"Lietuvos Respublikos Konstitucinis Teismas": [
            u"Konstitucinis Teismas",
            u"Lietuvos Respublikos Konstitucinis Teismas",
        ],
        u"Lietuvos vyriausiasis administracinis teismas": [
            u"Lietuvos Vyriausiasis administracinis teismas",
            u"Lietuvos vyriausiasis administracinis teismas",
        ],
        u'Lietuvos žemės ūkio bendrovių asociacija': [
            u'LŽŪBA',
        ],
        u"Nacionalinė tabako ir alkoholio kontrolės koalicija": [
            u"Nacionalin ė tabako ir alkoholio kontrolės koalicija",
        ],
        u"Narkotikų, tabako ir alkoholio kontrolės departamentas A. Veryga": [
            u"Narkotikų, tabako ir alkoholio kontrolės departmentas A. Veryga",
        ],
        u"Lietuvos draudikų asociacija": [
            u"Lietuvos draudik ų asociacija",
            u"Lietuvos draudikų asociacija",
        ],
        u"Lietuvos farmacijos darbuotojų profesinė sąjunga": [
            u"Lietuvos farmacijos darbuotojų profesinė sąjunga",
            u"Lietuvos farmacijos darbuotojų profesinės sąjunga",
        ],
        u"Lietuvos geografų draugija": [
            u"LIETUVOS GEOGRAFŲ DRAUGIJA",
        ],
        u"Lietuvos laisvosios rinkos institutas": [
            u"Laisvosios rinkos institutas",
            u"Lietuvos laisvosios rinkos institutas",
            u"VŠĮ Lietuvos laisvosios rinkos institutas",
            u"VŠĮ Lietuvos laisvosios rinkos institutas",
            u"VšĮ Lietuvos laisvosios rinkos institutas",
            u"Lietuvos laisvosios rinkos institutas (pateikiama sutrumpintai)",
        ],
        u"Lietuvos kelių policijos tarnyba": [
            u"Kelių policijos tarnyba",
            u"Lietuvos kelių policijos tarnyba",
        ],
        u"Lietuvos nacionalinės sveikatos tarybos pirmininkas J. Pundzius": [
            u"Lietuvos nacionalinė sveikatos tarybos pirmininkas J. Pundzius",
        ],
        u"Valstybės vaiko teisių apsaugos ir įvaikinimo tarnyba prie Socialinės apsaugos ir darbo ministerijos": [
            u"Valstybės vaiko teisių apsaugos ir įvaikinimo tarnyba prie SADM",
            u"Valstybės vaiko teisių apsaugos ir įvaikinimo tarnyba prie Socialinės apsaugos ir darbo ministerijos",
            u"Valstybės vaiko teisių ir įvaikinimo tarnyba prie socialinės apsaugos ir darbo ministerijos",
            u"Valstybės vaiko teisių ir įvaikinimo tarnyba prie socialinės apsaugos ir darbo ministerijos.",
        ],
        u"Valstybės valdymo ir savivaldybių komitetas": [
            u"Valstybės valdymo ir savivaldybės komitetas",
            u"Valstybės valdymo ir savibaldybių komitetas",
            u"Valstybės valdymo ir savivaldybių komitetas",
            u"Valstybės valdymo ir savivaldybių reikalų komitetas",
            u"Valstybės ir savivaldybių komitetas",
            u"Valstybių valdymo ir savivaldybių komitetas",
        ],
        u"Socialinių reikalų ir darbo komitetas": [
            u"Socialinių reikalų ir darbo Komitetas",
            u"Socialinių reikalų ir darbo komitetas",
            u"Socialinių reikalų ir darbo komiteto",
            u"Socialinių reikalų ir darbo komiteto pasiūlymas",
            u"Seimo Socialinių reikalų ir darbo komitetas",
            u"Seimo socialinių reikalų ir darbo komitetas",
            u"Lietuvos Respublikos Socialinių reikalų ir darbo komitetas",
        ],
        u"Mykolo Romerio universitetas": [
            u"Mykolo Riomerio universitetas",
            u"Mykolo Romerio universitetas",
        ],
        u"Mykolo Romerio universiteto Teisės fakultetas": [
            u"MRU Teisės fakultetas",
            u"Mykolo Romerio universiteto Teisės fakultetas",
            u"Mykolo Romerio universiteto Teisės fakultetas",
            u"Mykolo Romerio universtiteto Teisės fakultetas",
        ],
        u"Lietuvos Respublikos Vyriausybė": [
            u"Lietuvos Respublikos Vyriausybė",
            u"Lietuvos Respublikos vyriausybė",
            u"Lietuvos Respublikos Vyriausybės",
            u"Lietuvos Respublikos vyriausybės",
        ],
        u"Valstybinė kainų ir energetikos kontrolės komisija": [
            u"Valstybinė kainų energetikos kontrolės komisija",
            u"Valstybinė kainų ir energetikos kontrolės komisija",
        ],
        u"Valstybinė ligonių kasa prie Sveikatos apsaugos ministerijos": [
            u"Valstybinė ligonių kasa",
            u"Valstybinė ligonių kasa prie SAM",
            u"Valstybinė ligonių kasa prie Sveikatos apsaugos ministerijos",
        ],
        u"Valstybinė vaistų kontrolės tarnyba prie Sveikatos apsaugos ministerijos": [
            u"Valstybinė vaistų kontrolės tarnyba",
            u"Valstybinė vaistų kontrolės tarnyba prie Sveikatos apsaugos ministerijos",
        ],
        u"Lietuvos Respublikos valstybės kontrolė": [
            u"Valstybės kontrolė",
            u"Lietuvos Respublikos valstybės kontrolė",
            u"Lietuvos Respublikos valstybės kontrolės Valstybinio audito", # išvada Nr. 9-7, 2013-07-04
        ],
        u"Vilniaus universiteto Filologijos fakultetas": [
            u"Vilniaus universiteto Filologijos fakultetas",
            u"Vilniaus universiteto filologijos fakultetas",
        ],
        u"Valstybinė duomenų apsaugos inspekcija": [
            u"Valstybinė duomenų apsaugos inspekcija",
            u"Valstybinė duomenų inspekcija",
        ],
        u"Teisės ir teisėtvarkos komiteto patarėja R. Karpavičiūtė": [
            u"TTK biuro patarėja R. Karpavičiūtė",
            u"Teisės ir teisėtvarkos komiteto biuro patarėja R. Karpavičiūtė",
            u"Teisės ir teisėtvarkos komiteto patarėja R. Karpavičiūtė",
            u"Teisės ir teisėtvarkos patarėja R. Karpavičiūtė",
            u"Tesės ir teisėtvarkos komiteto patarėja R. Karpavičiūtė",
        ],
        u"Teisės ir teisėtvarkos komiteto patarėja L. Zdanavičienė": [
            u"Teisės ir teisėtvarkos komiteto patarėja L. Zdanavčienė",
            u"Teisės ir teisėtvarkos komiteto patarėja L. Zdanavičienė",
        ],
        u"Teisės ir teisėtvarkos komiteto patarėjas V. Kanapinskas": [
            u"Seimo kanceliarijos Teisės ir teisėtvarkos komiteto biuro patarėjas Virginijus Kanapinskas",
        ],
        u"Nacionalinis pareigūnų profesinių sąjungų susivienijimas": [
            u"Nacionalinis pareigūnų profesinių sąjungų susivienijimas",
            u"Nacionalinis pareigūnų profesinių sąjungų susivienijimus",
        ],
        u"Lietuvos sveikatos mokslų universitetas": [
            u"Lietuvos sveikatos mokslo universitetas",
            u"Lietuvos sveikatos mokslų universitetas",
        ],
        u"Lietuvos techninės apžiūros įmonių asociacija „Transeksta“": [
            u"Lietuvos techninės apžiūros įmonių asociacija TRANSEKSTA",
            u"Lietuvos techninės apžiūros įmonių asociacija „Transeksta“",
            u"Lietuvos techninės apžiūros įmonių asociacija Transeksta",
        ],
        u"Lietuvos teisėsaugos pareigūnų federacija": [
            u"Lietuvos Teisėsaugos pareigūnų federacija",
            u"Lietuvos teisėsaugos pareigūnų federacija",
        ],
        u"Lietuvos teisės institutas": [
            u"Lietuvos Teisės institutas",
            u"Lietuvos teisės institutas",
        ],
        u"Lietuvos vyskupų konferencija": [
            u"Lietuvos Vyskupų Konferencija",
            u"Lietuvos vyskupų konferencija",
        ],
        u"Lietuvos Respublikos trišalė taryba": [
            u"Lietuvos Respublikos Trišalė taryba",
            u"Lietuvos Respublikos trišalė taryba",
            u"Lietuvos trišalė taryba",
        ],
        u"Lietuvos Respublikos teisėjų asociacija": [
            u"Lietuvos Respublikos teisėjų asociacija",
            u"Lietuvos teisėjų asociacija",
        ],
        u"Lietuvos Respublikos valstybinė kultūros paveldo komisija": [
            u"Valstybinė kultūros paveldo komisija",
            u"Lietuvos Respublikos valstybinė kultūros paveldo komisija",
        ],
        u"Lietuvos heraldikos komisija": [
            u"Lietuvos heraldikos komisija",
            u"Hieraldikos komisija",
        ],
        u"Lietuvos Respublikos žemės ūkio rūmai": [
            u"Žemės ūkio rūmai",
            u"Lietuvos Respublikos žemės ūkio rūmai",
        ],
        u"Lietuvos respublikiniai būsto valdymo ir priežiūros rūmai": [
            u"Respublikiniai būsto valdymo ir priežiūros rūmai",
            u"Lietuvos respublikiniai būsto valdymo ir priežiūros rūmai",
        ],
        u"Tarptautinė žmogaus teisių gynimo organizacija „Fair Trials International“": [
            u"Nevyriausybinė organizacija FAIR TRIALS INTERNATIONAL\"",
            u"Tarptautinė žmogaus teisių gynimo organizacija „Fair Trials International“",
        ],
        # Oh my
        u"Onkohematologinių ligonių bendrija „Kraujas“ ir kt.": [
            u"Onkohematologinių ligonių bendrija „Kraujas\" ir kt.",
        ],
        u"Asociacija „Gyvastis“, ir kt.": [
            u"Asociacija „Gyvastis\", ir kt.",
        ],
        u"Lietuvos vaikų vėžio asociacija „Paguoda“ ir kt.": [
            u"Lietuvos vaikų vėžio asociacija „Paguoda \" ir kt.",
        ],
        u"Asociacija „Pozityvus gyvenimas“, ir kt.": [
            u"Asociacija „Pozityvus gyvenimas\", ir kt.",
        ],
        u"Onkologinėmis ligomis sergančių moterų draugija „Eivena“, ir kt.": [
            u"Onkologinėmis ligomis sergančių moterų draugija „Eivena \", ir kt.",
        ],
        u"VŠĮ „Kartu lengviau“ (sergantieji smegenų navikais), ir kt.": [
            u"VŠĮ „Kartu lengviau\" (sergantieji smegenų navikais), ir kt.",
        ],
        u"Lietuvos sergančiųjų genetinėmis nervųraumenų ligomis asociacija „Sraunija“, ir kt.": [
            u"Lietuvos sergančiųjų genetinėmis nervųraumenų ligomis asociacija „Sraunija\", ir kt.",
        ],
        u"Bechterevo liga sergančių draugija „Judesys“, ir kt.": [
            u"Bechterevo liga sergančių draugija Judesys“, ir kt.",
        ],
        # Some fun typos here too
        u'Lietuvos Aukščiausiasis Teismas': [
            u"Lietuvos Aukčiausiasis Teismas",
            u"Lietuvos Aukščiausiais Teismas",
            u"Lietuvos Aukščiausiasis Teismas",
            u"Lietuvos Aukščiausiasis teismas",
            u"Lietuvos Aukščiausias Teismas",
            u"Aukščiausiasis Teismas",
        ],
        u"Vilniaus Gedimino technikos universitetas": [
            u"Vilniaus Gedmino technikos universitetas",
        ],
        # Some people put their home addresses, phone numbers, emails or IP addresses
        u'A. Mitašiūnas': [
            u"Antanas Mitašiūnas, Kalvarijų 999-99, LT-99999 Vilnius, tel. 9-999-99999"
        ],
        u"R. Vyčaitė": [
            u"Rimantė Vyčaitė, gyv. A. Vivulskio g. 99-99, Vilnius",
        ],
        u"R. Marijona Bliznikienė": [
            u"Ramutė Marijona Bliznikienė, gyv. Naugarduko 999-99, Vilnius",
        ],
        u"J. Vaitkus": [
            u"Juozas Vaitkus el. paštu juoas.vaitkus@ff.vu.lt",
        ],
        u"Rūta": [
            u"Rūta 84.46.242.173",
        ],
    }

    def test(self):
        for expected, inputs in sorted(self.examples.items()):
            for example in sorted(inputs + [expected]):
                actual = SuggestionsSpider._clean_submitter(example)
                self.assertEqual(actual, expected)


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
        self.assertEqual(items[0]['submitter'], u'Seimo kanceliarijos Teisės departamentas')
        self.assertEqual(items[0]['date'], u'2015-09-08')
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
                submitter=u'Lietuvos Respublikos Vyriausybė',
                date=u'2015-10-09',
                document=u'',
                opinion=u'Pritarti iš dalies',
                source_url='http://localhost/test.html?p_id=12345',
                source_id='12345',
                source_index=0,
                raw=u'LR Vyriausybė, 2015-10-09',
            ),
        ])

    def check(self, html, expected):
        response = HtmlResponse('http://localhost/test.html?p_id=12345',
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

    def test_table_with_mismatching_colspans(self):
        # Regression data for bogus data due to colspans in data not matching colspans in header
        response = HtmlResponse('http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=456205&p_tr2=2',
                                body=fixture('suggestion_456205.html'))
        spider = SuggestionsSpider()
        items = list(spider.parse_document(response))
        self.assertEqual(len(items), 52)

    def test_table_with_more_mismatching_columns(self):
        # Regression data for bogus data due to colspan irregularity
        response = HtmlResponse('http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=491388&p_tr2=2',
                                body=fixture('suggestion_491388.html'))
        spider = SuggestionsSpider()
        items = list(spider.parse_document(response))
        self.assertEqual(len(items), 53)
        for item in items:
            self.assertTrue(len(item['opinion']) < 100, item)

    def test_table_with_even_more_mismatching_columns(self):
        # Regression data for bogus data due to colspan irregularity
        response = HtmlResponse('http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=485154&p_tr2=2',
                                body=fixture('suggestion_485154.html'))
        spider = SuggestionsSpider()
        items = list(spider.parse_document(response))
        self.assertEqual(len(items), 11)
        for item in items:
            self.assertTrue(len(item['opinion']) < 100, item)
