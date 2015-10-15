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
                submitter=u'STT',
                date=u'2015-10-09',
                document=u'raštas Nr. g-2015-123',
                opinion=u'',
                source_url='http://localhost/test.html',
            ),
            Suggestion(
                submitter=u'STT',
                date=u'2015-10-09',
                document=u'raštas Nr. g-2015-123',
                opinion=u'Pritarti',
                source_url='http://localhost/test.html',
            ),
            Suggestion(
                submitter=u'LR Vyriausybė',
                date=u'2015-10-09',
                document=u'',
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
                submitter=u'STT',
                date=u'2015-10-09',
                document=u'raštas Nr. g-2015-123',
                opinion=u'',
                source_url='http://localhost/test.html',
            ),
            Suggestion(
                submitter=u'STT',
                date=u'2015-10-09',
                document=u'raštas Nr. g-2015-123',
                opinion=u'Pritarti',
                source_url='http://localhost/test.html',
            ),
            Suggestion(
                submitter=u'LR Vyriausybė',
                date=u'2015-10-09',
                document=u'',
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
         {'submitter': u'Generalinė prokuratūra',
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
            submitter=u'STT',
            date=u'2015-10-09',
            document=u'raštas Nr. g-2015-123',
            opinion=u'Pritarti',
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
        u'STT': [
            u'STT (',
            u'STT, ',
        ],
        u'Žemės ūkio ministerija': [
            u'Žemės ūkio ministerija (gauta',
        ],
        # Trailing incomplete date fragments are stripped
        u'STT': [
            u'STT 2014-',
            u'STT, 2013-01-',
        ],
        # Trailing periods are stripped
        u"Valstybės vaiko teisių ir įvaikinimo tarnyba prie socialinės apsaugos ir darbo ministerijos": [
            u"Valstybės vaiko teisių ir įvaikinimo tarnyba prie socialinės apsaugos ir darbo ministerijos.",
        ],
        # Exception: trailing periods are sometimes necessary
        u"R. Jocienė ir kt.": [],
        # Often quotes are entered incorrectly
        u'AB „Amber grid“': [
            u'AB „Amber grid“',
            u'AB ,,Amber grid“',
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
        u'Seimo kanceliarijos Teisės departamentas': [
            u'Seimo kanceliari-jos Teisės departa- mentas',
            u'Seimo kanceliarijos Teisės departamentas',
        ],
        # Hyphenation exceptions
        u'Pilietė A. Butkutė-Žverelo': [
            u'Pilietė A. Butkutė-Žverelo',
        ],
        u'Architektė-urbanistė Agnė Selemonaitė': [
            u'Architektė-urbanistė Agnė Selemonaitė',
        ],
        u'Koalicija „Moters teisės-visuotinės žmogaus teisės“': [
            u'Koalicija „Moters teisės-visuotinės žmogaus teisės“',
        ],
        # Some people have trouble spelling 'departamentas'
        u'Europos teisės departamentas': [
            u'Europos teisės departa-menras',
        ],
        u'Seimo kanceliarijos Teisės departamentas': [
            u'Seimo kanceliari-jos Teisės departa-menta-mentas',
        ],
        # Spaces are important
        u'Lietuvos Respublikos Prezidentės dekretas': [
            u'Lietuvos RespublikosPrezidentės dekretas',
        ],
        u'Seimo kanceliarijos Teisės departamentas': [
            u'Seimo kanceliari-jos Teisėsdepartamentas',
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
        ],
        u"Darbo grupė viešojo sektoriaus audito sistemai tobulinti": [
            u"Darbo grupė viešojo sektoriaus audito sistemai tobulinti",
            u"Darbo grupė viešojo sektoriaus audito sistemai tobulinti (sudaryta Lietuvos Respublikos Seimo valdybos 2013 m. gegužės 29 d. sprendimu Nr. SV-S-255)",
        ],
        u"Darbo saugos specialistų darbdavių asociacija": [
            u"Darbo saugos specialistų darbdavių asociacija",
            u"Darbų saugos specialistų darbdavių asociacija",
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
        u"Lietuvos Respublikos finansų ministerija": [
            u"Lietuvos Respublikos Finansų ministerija",
            u"Lietuvos Respublikos finansų ministerija",
        ],
        u"Lietuvos Respublikos generalinė prokuratūra": [
            u"Lietuvos Respublikos Generalinė prokuratūra",
            u"Lietuvos Respublikos generalinė prokuratūra",
        ],
        u"Lietuvos Respublikos Seimo biudžeto ir finansų komitetas": [
            u"Lietuvos Respublikos Seimo Biudžeto ir finansų komitetas",
            u"Lietuvos Respublikos Seimo biudžeto ir finansų komitetas",
        ],
        u"Lietuvos Respublikos specialiųjų tyrimų tarnyba": [
            u"Lietuvos Respublikos Specialiųjų tyrimų tarnyba",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyb a",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyba.",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyba",
            u"Lietuvos respublikos specialiųjų tyrimų tarnyba",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyba 2012-",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyba, 2013-01-",
            u"Lietuvos Respublikos Specialiųjų tyrimų tarnyba tarnyb a",
            u"Lietuvos Respublikos specialiųjų tyrimų tarnyba (toliau– STT)",
        ],
        u"Lietuvos Respublikos teisingumo ministerija": [
            u"Lietuvos Respublikos Teisingumo ministerija",
            u"Lietuvos Respublikos teisingumo ministerija",
        ],
        u"Lietuvos Respublikos transporto priemonių draudikų biuras": [
            u"Lietuvos Respublikos Transporto priemonių draudikų biuras",
            u"Lietuvos Respublikos transporto priemonių draudikų biuras",
        ],
        u"Lietuvos Respublikos trišalė taryba": [
            u"Lietuvos Respublikos Trišalė taryba",
            u"Lietuvos Respublikos trišalė taryba",
        ],
        u"Lietuvos Respublikos ūkio ministerija": [
            u"Lietuvos Respublikos Ūkio ministerija",
            u"Lietuvos Respublikos ūkio ministerija",
        ],
        u"Lietuvos Respublikos vaiko teisių apsaugos kontrolieriaus įstaiga": [
            u"Lietuvos Respublikos Vaiko teisių apsaugos kontrolės įstaiga",
            u"Lietuvos Respublikos vaiko teisių apsaugos kontrolieriaus įstaiga",
        ],
        u"Lietuvos Respublikos valstybės saugumo departamentas": [
            u"Lietuvos Respublikos Valstybės saugumo departamentas",
            u"Lietuvos Respublikos valstybės saugumo departamentas",
        ],
        u"Lietuvos Respublikos vyriausioji rinkimų komisija": [
            u"Lietuvos Respublikos Vyriausioji rinkimų komisija",
            u"Lietuvos Respublikos vyriausioji rinkimų komisija",
        ],
        u"Lietuvos savivaldybių asociacija": [
            u"Lietuvos Savivaldybių asociacija",
            u"Lietuvos savivaldybių asociacija",
        ],
        # Different capitalizations
        u"Legalaus verslo aljansas": [
            u"Legalaus Verslo aljansas",
        ],
        u"Lietuvos apeliacinis teismas": [
            u"Lietuvos Apeliacinis Teismas",
            u"Lietuvos Apeliacinis teismas",
            u"Lietuvos apeliacinis teismas",
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
        u"VŠĮ Lietuvos laisvosios rinkos institutas": [
            u"VŠĮ Lietuvos laisvosios rinkos institutas",
            u"VšĮ Lietuvos laisvosios rinkos institutas",
        ],
        # Some fun typos here too
        u'Lietuvos Aukščiausiasis Teismas': [
            u"Lietuvos Aukčiausiasis Teismas",
            u"Lietuvos Aukščiausiais Teismas",
            u"Lietuvos Aukščiausiasis Teismas",
            u"Lietuvos Aukščiausiasis teismas",
            u"Lietuvos Aukščiausias Teismas",
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
                submitter=u'LR Vyriausybė',
                date=u'2015-10-09',
                document=u'',
                opinion=u'Pritarti iš dalies',
                source_url='http://localhost/test.html?p_id=12345',
                source_id='12345',
                source_index=0,
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
