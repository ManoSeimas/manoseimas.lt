# coding: utf-8
# flake8: noqa

import unittest
import datetime

from scrapy.http import HtmlResponse
from scrapy.link import Link
from scrapy.selector import Selector

from manoseimas.scrapy.tests.utils import fixture

from manoseimas.scrapy.textutils import strip_tags, extract_text
from manoseimas.scrapy.spiders.stenograms import StenogramSpider
from manoseimas.scrapy.spiders.stenograms import as_statement
from manoseimas.scrapy.spiders.stenograms import SittingChairpersonProcessor


source_text = u"""<p class="Roman"><b>
<span style="font-size:9.0pt">PIRMININKĖ.</span></b> Ačiū.
Pas&shy;ku&shy;ti&shy;nis klau&shy;sia <span style="letter-spacing:-.1pt">
M.&nbsp;Za&shy;s&shy;čiu&shy;rins&shy;kas.
Pri&shy;me&shy;nu, kad klau&shy;si&shy;mui – 1&nbsp;min.</span></p>"""

statement_source_text = u"""<p class="Roman"><b>
<span style="font-size:9.0pt">PIRMININKĖ.</span></b>(<i>LSF</i>) Ačiū.
Pas&shy;ku&shy;ti&shy;nis klau&shy;sia <span style="letter-spacing:-.1pt">
M.&nbsp;Za&shy;s&shy;čiu&shy;rins&shy;kas.
Pri&shy;me&shy;nu, kad klau&shy;si&shy;mui – 1&nbsp;min.</span></p>"""


class StenogramUtilsTestCase(unittest.TestCase):

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

    def test_strip_tags(self):
        tagged_text = '<p><a>pavadinimas</a> text (<i>randomtag</i>)</p>'
        stripped = strip_tags(tagged_text)
        self.assertEquals('pavadinimas text (randomtag)',
                          stripped)

    def test_clean_text(self):
        xs = Selector(text=source_text)
        text = extract_text(xs.xpath('//p'), kill_tags=['b'])
        self. assertEqual((u'Ačiū. Paskutinis klausia M.\xa0Zasčiurinskas. '
                           u'Primenu, kad klausimui – 1\xa0min.'),
                          text)

    def test_as_statement(self):
        xs = Selector(text=statement_source_text)
        text = as_statement(xs.xpath('//p'))
        self. assertEqual((u'Ačiū. Paskutinis klausia M.\xa0Zasčiurinskas. '
                           u'Primenu, kad klausimui – 1\xa0min.'),
                          text)

    def test_sitting_chairperson_processor(self):
        scpp = SittingChairpersonProcessor()
        self.assertEqual((u'L. GRAUŽINIENĖ', None),
                         scpp.process_mp(u'PIRMININKĖ (L. GRAUŽINIENĖ).',
                                         None))
        self.assertEqual((u'S. JOVAIŠA', u'TS-LKDF'),
                         scpp.process_mp(u'S. JOVAIŠA',
                                         u'TS-LKDF'))
        self.assertEqual((u'L. GRAUŽINIENĖ', None),
                         scpp.process_mp(u'PIRMININKĖ', None))
        self.assertEqual((u'A. SYSAS', 'LSDPF'),
                         scpp.process_mp(u'PIRMININKAS (A. SYSAS, LSDPF)',
                                         None))
        self.assertEqual((u'A. SYSAS', 'LSDPF'),
                         scpp.process_mp(u'PIRMININKAS', None))


class StenogramCrawlerTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        super(StenogramCrawlerTestCase, self).setUp()
        url = 'http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=1034324'
        self.response = HtmlResponse(url,
                                     body=fixture('stenogram_1034324.html'))
        self.partial_response = HtmlResponse(
            url,
            body=fixture('stenogram_1034324_partial.html')
        )
        self.spider = StenogramSpider()

        self.parsed_paras = [
            {'fraction': None,
             'speaker': u'PIRMININK\u0116 (L.\xa0GRAU\u017dINIEN\u0116)',
             'statement': u'Gerbiamieji kolegos, prad\u0117sime gegu\u017e\u0117s 21\xa0d. (ketvirtadienio) rytin\u012f plenarin\u012f pos\u0117d\u012f. (Gongas)',
             'type': 'statement_start'},
            {'time': datetime.time(10, 1),
             'type': 'time'},
            {'title': u'Informaciniai prane\u0161imai',
             'type': 'title'},
            {'statement': u'Prie\u0161 prad\u0117dama kalb\u0117ti apie darbotvark\u0119 noriu priminti, k\u0105 mums \u012feinant \u012f pos\u0117d\u017ei\u0173 sal\u0119 primin\u0117 jauni \u017emon\u0117s, kad gegu\u017e\u0117s 25\xa0d. yra Dingusi\u0173 vaik\u0173 pamin\u0117jimo diena. Bus rengiami renginiai, tod\u0117l organizatoriai kvie\u010dia visus Seimo narius aktyviai dalyvauti \u0161iuose renginiuose.',
             'type': 'statement_fragment'},
            {'statement': u'Taip pat noriu informuoti, kad kvie\u010diame \u012fsira\u0161yti \u012f Seimo Tarpparlamentini\u0173 ry\u0161i\u0173 su Graikijos Respublika draug\u0173 grup\u0119. U\u017esira\u0161yti galime iki gegu\u017e\u0117s\u2026 (Balsai sal\u0117je) \u010cia jau terminas net pra\u0117j\u0119s. Grup\u0117s pos\u0117dis vyko 19\xa0d., irgi pra\u0117j\u0119s. Kiek suprantu, jau \u012fvyko, taip? Klausiu P.\xa0\u010cimbaro. Ar jau buvo grup\u0117s susitikimas, ar ne? Graikijos Respublikos draug\u0173 grup\u0117s susitikimas jau buvo ar ne? Ne. Tai dar kart\u0105 kvie\u010diu visus aktyviai \u012fsitraukti \u012f Seimo Tarpparlamentini\u0173 ry\u0161i\u0173 su Graikijos Respublika draug\u0173 grup\u0119. Koordinatorius \u2013 P.\xa0\u010cimbaras, jeigu kas nors neai\u0161ku.',
             'type': 'statement_fragment'},
            {'statement': u'D\u0117l Darbo partijos frakcijos seni\u016bno pavaduotoj\u0173. Informuojame, kad \u0161i\u0173 met\u0173 gegu\u017e\u0117s 20\xa0d. frakcijos pos\u0117dyje Darbo partijos frakcija nutar\u0117 atstatydinti Darbo partijos frakcijos seni\u016bno pavaduoj\u0105 V.\xa0Fiodorov\u0105. Tokia \u017einia. Papra\u0161ysime Darbo partijos frakcijos pateikti pakeitimus d\u0117l Seimo nutarimo d\u0117l Seni\u016bn\u0173 sueigos, man atrodo, jis ten buvo.',
             'type': 'statement_fragment'},
            {'time': datetime.time(10, 4),
             'type': 'time'},
            {'title': u'Seni\u016bn\u0173 sueigos patikslintos 2015\xa0m. gegu\u017e\u0117s 21\xa0d. (ketvirtadienio) pos\u0117d\u017ei\u0173 darbotvark\u0117s tikslinimas ir tvirtinimas',
             'type': 'title'},
            {'statement': u'Gerbiamieji kolegos, ar j\u016bs mane dar girdite? Pra\u0161y\u010diau s\u0117sti \u012f savo darbo vietas. Prad\u0117sime \u0161ios dienos darbotvarke. D\u0117l darbotvark\u0117s niekas nenorite? R.\xa0Juknevi\u010dien\u0117. Pra\u0161om.',
             'type': 'statement_fragment'},
            {'fraction': u'TS-LKDF',
             'speaker': u'R.\xa0JUKNEVI\u010cIEN\u0116',
             'statement': u'(TS-LKDF*). Ponia Pirmininke, a\u0161 nesu Seni\u016bn\u0173 sueigos nar\u0117, bet buvau informuota, kad Seni\u016bn\u0173 sueigoje buvo kalbama d\u0117l \u012f opozicin\u0119 darbotvark\u0119 \u012fra\u0161yto 1 klausimo. Buvo siekiama tokio bendro sutarimo d\u0117l to, kad pagal partij\u0173 susitarim\u0105, kuris buvo pasira\u0161ytas pra\u0117jusiais metais, buvo sutarta, kad Seimo plenariniame pos\u0117dyje turi vykti diskusija nacionalinio saugumo klausimais. Mes t\u0105 klausim\u0105 i\u0161k\u0117l\u0117me ir tikrai labai nor\u0117tume, kad b\u016bt\u0173 geranori\u0161kas vis\u0173 frakcij\u0173, Seimo vadovyb\u0117s bendradarbiavimas, tod\u0117l mes sutinkame \u0161iandien i\u0161braukti \u0161\u012f klausim\u0105 i\u0161 darbotvark\u0117s, ta\u010diau labai nor\u0117\u010diau, kad mes dabar geranori\u0161kai bendru sutarimu tiesiog \u012f protokol\u0105 \u012fra\u0161ytume, kad b\u016btent bir\u017eelio 11\xa0d., kada jau bus tokia ramesn\u0117 aplinka (beje, ir pasiruo\u0161imui laiko reikia), mes gal\u0117tume toki\u0105 diskusij\u0105 surengti. Jeigu b\u016bt\u0173 geranori\u0161kas sutarimas, mes tuomet sutinkame i\u0161braukti \u0161i\u0105 rezoliucij\u0105 i\u0161 darbotvark\u0117s. Labai jums a\u010di\u016b.',
             'type': 'statement_start'},
            {'fraction': None,
             'speaker': u'PIRMININK\u0116',
             'statement': u'Gerai, a\u010di\u016b. Gal i\u0161 karto galime apsispr\u0119sti? Gal galime bendrai sutarti, kad vis tiek diskusija \u012fvyks. Kadangi visos partijos pasira\u0161\u0117, tai mes manome, kad tikrai visos partijos kartu turi ir priimti. Yra si\u016bloma bir\u017eelio 11\xa0d., reikia suderinti su institucij\u0173 vadovais ir kitais, kad gal\u0117t\u0173 dalyvauti. Ar galime pritarti bendru sutarimu? (Balsai sal\u0117je) Geria. Labai a\u010di\u016b. D\u0117koju u\u017e supratim\u0105.',
             'type': 'statement_start'},
            {'statement': u'Gerbiamasis A.\xa0Matulas.',
             'type': 'statement_fragment'},
            {'fraction': u'TS-LKDF',
             'speaker': u'A.\xa0MATULAS',
             'statement': u'Gerbiamoji Pirmininke, gerbiamieji kolegos, kadangi prie\u0161 tai labai gra\u017eiai sutar\u0117me, i\u0161brauk\u0117me i\u0161 darbotvark\u0117s vien\u0105 rezoliucij\u0105, kuri tur\u0117jo b\u016bti pateikta turb\u016bt viso Seimo vardu, a\u0161 labai pra\u0161au frakcijos vardu, kad nepasikartot\u0173 praeitos opozicin\u0117s darbotvark\u0117s situacija. Gal b\u016bt\u0173 galima pritarti, kad vienu metu yra pateikiami si\u016blymai (perskaitant visus si\u016blymus) \u012ftraukti \u012f pavasario sesijos darbotvark\u0119 visus klausimus ir balsuoti, kad neb\u016bt\u0173 taip, kad atmetame, o mums neleid\u017eiama net pristatyti. Tikrai \u0161iandien yra pateikti dalykiniai, ne politizuoti klausimai, tai labai pra\u0161au viso Seimo sutikti, kad balsuotume u\u017e \u012ftraukim\u0105 \u012f darbotvark\u0119 vienu metu u\u017e visus. Sutaupytume laiko ir pagal pavasario sesijos darb\u0173 program\u0105 mums atsirast\u0173 galimyb\u0117. Kaip jau ten balsuosite, taip, bet bent jau leiskite pristatyti. Labai a\u010di\u016b.',
             'type': 'statement_start'},
            {'fraction': None,
             'speaker': u'PIRMININK\u0116',
             'statement': u'Labai a\u010di\u016b. Bet negaliu dabar teikti balsuoti j\u016bs\u0173 pra\u0161ymo. Tikiuosi, kad Seimo nariai i\u0161girdo ir, svarstydami opozicin\u0119 darbotvark\u0119, tikrai pa\u017ei\u016br\u0117s \u012f teikiamo \u012fstatymo turin\u012f.',
             'type': 'statement_start'},
            {'statement': u'Gerbiamasis S.\xa0Jovai\u0161a. Pra\u0161om.',
             'type': 'statement_fragment'},
            {'fraction': u'TS-LKDF',
             'speaker': u'S.\xa0JOVAI\u0160A',
             'statement': u'A\u0161 d\u0117l to paties techninio klausimo. Yra opozicijos darbotvark\u0117s 2-12 klausimas, \u012fstatymo projektas Nr.\xa0XIIP-3100, bet n\u0117ra \u012fra\u0161yto nutarimo d\u0117l \u0161ios sesijos darb\u0173 programos papildymo. A\u0161 \u010dia pra\u017ei\u016br\u0117ta?',
             'type': 'statement_start'}
            ]

        self.grouped_topics = [
            {'title': u'Informaciniai prane\u0161imai',
             'time': datetime.time(10, 1),
             'statements': [
                 {'fraction': None,
                  'speaker': u'L.\xa0GRAU\u017dINIEN\u0116',
                  'statement': [u'Prie\u0161 prad\u0117dama kalb\u0117ti apie darbotvark\u0119 noriu priminti, k\u0105 mums \u012feinant \u012f pos\u0117d\u017ei\u0173 sal\u0119 primin\u0117 jauni \u017emon\u0117s, kad gegu\u017e\u0117s 25\xa0d. yra Dingusi\u0173 vaik\u0173 pamin\u0117jimo diena. Bus rengiami renginiai, tod\u0117l organizatoriai kvie\u010dia visus Seimo narius aktyviai dalyvauti \u0161iuose renginiuose.',
                                u'Taip pat noriu informuoti, kad kvie\u010diame \u012fsira\u0161yti \u012f Seimo Tarpparlamentini\u0173 ry\u0161i\u0173 su Graikijos Respublika draug\u0173 grup\u0119. U\u017esira\u0161yti galime iki gegu\u017e\u0117s\u2026 (Balsai sal\u0117je) \u010cia jau terminas net pra\u0117j\u0119s. Grup\u0117s pos\u0117dis vyko 19\xa0d., irgi pra\u0117j\u0119s. Kiek suprantu, jau \u012fvyko, taip? Klausiu P.\xa0\u010cimbaro. Ar jau buvo grup\u0117s susitikimas, ar ne? Graikijos Respublikos draug\u0173 grup\u0117s susitikimas jau buvo ar ne? Ne. Tai dar kart\u0105 kvie\u010diu visus aktyviai \u012fsitraukti \u012f Seimo Tarpparlamentini\u0173 ry\u0161i\u0173 su Graikijos Respublika draug\u0173 grup\u0119. Koordinatorius \u2013 P.\xa0\u010cimbaras, jeigu kas nors neai\u0161ku.',
                                u'D\u0117l Darbo partijos frakcijos seni\u016bno pavaduotoj\u0173. Informuojame, kad \u0161i\u0173 met\u0173 gegu\u017e\u0117s 20\xa0d. frakcijos pos\u0117dyje Darbo partijos frakcija nutar\u0117 atstatydinti Darbo partijos frakcijos seni\u016bno pavaduoj\u0105 V.\xa0Fiodorov\u0105. Tokia \u017einia. Papra\u0161ysime Darbo partijos frakcijos pateikti pakeitimus d\u0117l Seimo nutarimo d\u0117l Seni\u016bn\u0173 sueigos, man atrodo, jis ten buvo.']
                  }
             ]},
            {
              'time': datetime.time(10, 4),
              'title': u'Seni\u016bn\u0173 sueigos patikslintos 2015\xa0m. gegu\u017e\u0117s 21\xa0d. (ketvirtadienio) pos\u0117d\u017ei\u0173 darbotvark\u0117s tikslinimas ir tvirtinimas',
              'statements': [
                  {'fraction': None,
                   'speaker': u'L.\xa0GRAU\u017dINIEN\u0116',
                   'statement': [u'Gerbiamieji kolegos, ar j\u016bs mane dar girdite? Pra\u0161y\u010diau s\u0117sti \u012f savo darbo vietas. Prad\u0117sime \u0161ios dienos darbotvarke. D\u0117l darbotvark\u0117s niekas nenorite? R.\xa0Juknevi\u010dien\u0117. Pra\u0161om.']},
                  {'fraction': u'TS-LKDF',
                   'speaker': u'R.\xa0JUKNEVI\u010cIEN\u0116',
                   'statement': [u'(TS-LKDF*). Ponia Pirmininke, a\u0161 nesu Seni\u016bn\u0173 sueigos nar\u0117, bet buvau informuota, kad Seni\u016bn\u0173 sueigoje buvo kalbama d\u0117l \u012f opozicin\u0119 darbotvark\u0119 \u012fra\u0161yto 1 klausimo. Buvo siekiama tokio bendro sutarimo d\u0117l to, kad pagal partij\u0173 susitarim\u0105, kuris buvo pasira\u0161ytas pra\u0117jusiais metais, buvo sutarta, kad Seimo plenariniame pos\u0117dyje turi vykti diskusija nacionalinio saugumo klausimais. Mes t\u0105 klausim\u0105 i\u0161k\u0117l\u0117me ir tikrai labai nor\u0117tume, kad b\u016bt\u0173 geranori\u0161kas vis\u0173 frakcij\u0173, Seimo vadovyb\u0117s bendradarbiavimas, tod\u0117l mes sutinkame \u0161iandien i\u0161braukti \u0161\u012f klausim\u0105 i\u0161 darbotvark\u0117s, ta\u010diau labai nor\u0117\u010diau, kad mes dabar geranori\u0161kai bendru sutarimu tiesiog \u012f protokol\u0105 \u012fra\u0161ytume, kad b\u016btent bir\u017eelio 11\xa0d., kada jau bus tokia ramesn\u0117 aplinka (beje, ir pasiruo\u0161imui laiko reikia), mes gal\u0117tume toki\u0105 diskusij\u0105 surengti. Jeigu b\u016bt\u0173 geranori\u0161kas sutarimas, mes tuomet sutinkame i\u0161braukti \u0161i\u0105 rezoliucij\u0105 i\u0161 darbotvark\u0117s. Labai jums a\u010di\u016b.']},
                  {'fraction': None,
                   'speaker': u'L.\xa0GRAU\u017dINIEN\u0116',
                   'statement': [u'Gerai, a\u010di\u016b. Gal i\u0161 karto galime apsispr\u0119sti? Gal galime bendrai sutarti, kad vis tiek diskusija \u012fvyks. Kadangi visos partijos pasira\u0161\u0117, tai mes manome, kad tikrai visos partijos kartu turi ir priimti. Yra si\u016bloma bir\u017eelio 11\xa0d., reikia suderinti su institucij\u0173 vadovais ir kitais, kad gal\u0117t\u0173 dalyvauti. Ar galime pritarti bendru sutarimu? (Balsai sal\u0117je) Geria. Labai a\u010di\u016b. D\u0117koju u\u017e supratim\u0105.',
                                 u'Gerbiamasis A.\xa0Matulas.']},
                  {'fraction': u'TS-LKDF',
                   'speaker': u'A.\xa0MATULAS',
                   'statement': [u'Gerbiamoji Pirmininke, gerbiamieji kolegos, kadangi prie\u0161 tai labai gra\u017eiai sutar\u0117me, i\u0161brauk\u0117me i\u0161 darbotvark\u0117s vien\u0105 rezoliucij\u0105, kuri tur\u0117jo b\u016bti pateikta turb\u016bt viso Seimo vardu, a\u0161 labai pra\u0161au frakcijos vardu, kad nepasikartot\u0173 praeitos opozicin\u0117s darbotvark\u0117s situacija. Gal b\u016bt\u0173 galima pritarti, kad vienu metu yra pateikiami si\u016blymai (perskaitant visus si\u016blymus) \u012ftraukti \u012f pavasario sesijos darbotvark\u0119 visus klausimus ir balsuoti, kad neb\u016bt\u0173 taip, kad atmetame, o mums neleid\u017eiama net pristatyti. Tikrai \u0161iandien yra pateikti dalykiniai, ne politizuoti klausimai, tai labai pra\u0161au viso Seimo sutikti, kad balsuotume u\u017e \u012ftraukim\u0105 \u012f darbotvark\u0119 vienu metu u\u017e visus. Sutaupytume laiko ir pagal pavasario sesijos darb\u0173 program\u0105 mums atsirast\u0173 galimyb\u0117. Kaip jau ten balsuosite, taip, bet bent jau leiskite pristatyti. Labai a\u010di\u016b.']},
                  {'fraction': None,
                   'speaker': u'L.\xa0GRAU\u017dINIEN\u0116',
                   'statement': [u'Labai a\u010di\u016b. Bet negaliu dabar teikti balsuoti j\u016bs\u0173 pra\u0161ymo. Tikiuosi, kad Seimo nariai i\u0161girdo ir, svarstydami opozicin\u0119 darbotvark\u0119, tikrai pa\u017ei\u016br\u0117s \u012f teikiamo \u012fstatymo turin\u012f.',
                                 u'Gerbiamasis S.\xa0Jovai\u0161a. Pra\u0161om.']},
                  {'fraction': u'TS-LKDF',
                   'speaker': u'S.\xa0JOVAI\u0160A',
                   'statement': [u'A\u0161 d\u0117l to paties techninio klausimo. Yra opozicijos darbotvark\u0117s 2-12 klausimas, \u012fstatymo projektas Nr.\xa0XIIP-3100, bet n\u0117ra \u012fra\u0161yto nutarimo d\u0117l \u0161ios sesijos darb\u0173 programos papildymo. A\u0161 \u010dia pra\u017ei\u016br\u0117ta?']}],
            },
        ]

    def test_parse_paragraphs(self):
        sel = Selector(self.partial_response)
        paragraphs = sel.xpath('/html/body/div[@class="WordSection2"]/p')
        parsed = list(self.spider._parse_paragraphs(paragraphs))
        self.assertEqual(self.parsed_paras, parsed)

    def test_group_topics(self):
        topics = self.spider._group_topics(self.parsed_paras)
        self.assertEqual(self.grouped_topics, topics)

    def test_parse_stenogram(self):
        items = list(self.spider.parse_stenogram(self.response))
        self.assertEqual(20, len(items))
