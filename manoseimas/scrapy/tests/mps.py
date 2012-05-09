# coding: utf-8

import unittest

from scrapy.http import HtmlResponse

from ..spiders.mps import MpsSpider

from .utils import fixture


class TestMpsSpider(unittest.TestCase):
    def test_nedzinskas(self):
        spider = MpsSpider()
        url = ('http://www3.lrs.lt/pls/inter/w5_show?'
               'p_r=6113&p_k=1&p_a=5&p_asm_id=53911&p_kade_id=6')
        response = HtmlResponse(url, body=fixture('mp_53911.html'))
        items = list(spider.parse_person(response))
        item = items[0]
        self.assertEqual(item['_id'], '53911p')
        self.assertEqual(item['first_name'], 'Antanas')
        self.assertEqual(item['last_name'], 'Nedzinskas')
        self.assertEqual(item['dob'], '1981-03-15')
        self.assertEqual(item['email'], ['Antanas.Nedzinskas@lrs.lt'])
        self.assertEqual(item['phone'], ['2396694'])
        self.assertEqual(item['raised_by'], u'Tautos prisikėlimo partija')
        self.assertEqual(item['candidate_page'],
                ('http://www.vrk.lt/rinkimai/400_lt/Kandidatai/'
                 'Kandidatas22997/Kandidato22997Anketa.html'))
        self.assertEqual(item['photo'],
                ('http://www3.lrs.lt/home'
                 '/seimo_nariu_nuotraukos/2008/antanas_nedzinskas.jpg'))
        self.assertEqual(len(item['groups']), 13)

    def test_adomenas(self):
        spider = MpsSpider()
        url = ('http://www3.lrs.lt/pls/inter/w5_show?'
               'p_r=6113&p_k=1&p_a=5&p_asm_id=48690&p_kade_id=6')
        response = HtmlResponse(url, body=fixture('mp_48690.html'))

        items = list(spider.parse_person(response))
        item = items[0]
        self.assertEqual(item['_id'], '48690p')
        self.assertEqual(item['parliament'], ['2008-2012'])
        self.assertEqual(item['first_name'], 'Mantas')
        self.assertEqual(item['last_name'], u'Adomėnas')
        self.assertEqual(item['dob'], '1972-10-01')
        self.assertEqual(item['email'], ['Mantas.Adomenas@lrs.lt'])
        self.assertEqual(item['phone'], ['2396631'])
        self.assertEqual(item['office_address'],
                         u'Odminių g. 3, 01122 Vilniaus m')
        self.assertEqual(item['constituency'],
                         u'Senamiesčio  (Nr. 2) apygardoje')
        self.assertEqual(item['raised_by'], (u'Tėvynės sąjunga - Lietuvos '
                                             u'krikščionys demokratai'))
        self.assertEqual(item['home_page'], 'http://www.adomenas.lt')
        self.assertEqual(item['candidate_page'],
                ('http://www.vrk.lt/rinkimai/400_lt/Kandidatai/'
                 'Kandidatas19624/Kandidato19624Anketa.html'))
        self.assertEqual(item['photo'],
                ('http://www3.lrs.lt/home'
                 '/seimo_nariu_nuotraukos/2008/mantas_adomenas.jpg'))
        self.assertEqual(len(item['groups']), 32)


    def test_jukneviciene(self):
        spider = MpsSpider()
        url = ('http://www3.lrs.lt/pls/inter/w5_show?'
               'p_r=6113&p_k=1&p_a=5&p_asm_id=178&p_kade_id=6')
        response = HtmlResponse(url, body=fixture('mp_178.html'))

        items = list(spider.parse_person(response))
        item = items[0]

        self.assertEqual(item['dob'], '1958-01-26')
        self.assertEqual(item['parliament'], ['2008-2012', '2004-2008',
                                              '2000-2004', '1996-2000',
                                              '1990-1992'])
        self.assertEqual(len(item['groups']), 10)

    def test_abramikiene(self):
        spider = MpsSpider()
        url = ('http://www3.lrs.lt/pls/inter/w5_show?'
               'p_a=5&p_asm_id=7229&p_k=1&p_kade_id=6&p_r=6113')
        response = HtmlResponse(url, body=fixture('mp_7229.html'))

        items = list(spider.parse_person(response))
        item = items[0]

        self.assertEqual(item['first_name'], u'Vilija')
        self.assertEqual(item['last_name'], u'Aleknaitė Abramikienė')
        self.assertEqual(item['dob'], '1957-05-04')
        self.assertEqual(len(item['groups']), 21)

    def test_rutkelyte(self):
        spider = MpsSpider()
        url = ('http://www3.lrs.lt/pls/inter/w5_show?'
               'p_a=5&p_asm_id=7259&p_k=1&p_kade_id=6&p_r=6113')
        response = HtmlResponse(url, body=fixture('mp_7259.html'))

        items = list(spider.parse_person(response))
        item = items[0]

        self.assertEqual(item['first_name'], u'Rūta')
        self.assertEqual(item['last_name'], u'Rutkelytė')
        self.assertEqual(item['constituency'], u'pagal sąrašą')
        self.assertEqual(item['office_address'], u'')


    def test_alekna(self):
        spider = MpsSpider()
        url = ('http://www3.lrs.lt/pls/inter/w5_show?'
               'p_a=5&p_asm_id=7404&p_k=1&p_kade_id=6&p_r=6113')
        response = HtmlResponse(url, body=fixture('mp_7404.html'))

        items = list(spider.parse_person(response))
        item = items[0]

        self.assertEqual(item['first_name'], u'Raimundas')
        self.assertEqual(item['last_name'], u'Alekna')
        self.assertEqual(item['constituency'], u'pagal sąrašą')
        self.assertEqual(item['candidate_page'],
                ('http://www.vrk.lt/rinkimai/400_lt/Kandidatai/'
                 'Kandidatas19638/Kandidato19638Anketa.html'))
        self.assertEqual(item['parliament'], ['2008-2012', '1996-2000'])


    def test_baltraitiene(self):
        spider = MpsSpider()
        url = ('http://www3.lrs.lt/pls/inter/w5_show?'
               'p_a=5&p_asm_id=48114&p_k=1&p_kade_id=6&p_r=6113')
        response = HtmlResponse(url, body=fixture('mp_48114.html'))

        items = list(spider.parse_person(response))
        item = items[0]

        self.assertEqual(item['first_name'], u'Virginija')
        self.assertEqual(item['last_name'], u'Baltraitienė')


    def test_jursenas(self):
        spider = MpsSpider()
        url = ('http://www3.lrs.lt/pls/inter/w5_show?'
               'p_r=6113&p_k=1&p_a=5&p_asm_id=110&p_kade_id=6')
        response = HtmlResponse(url, body=fixture('mp_110.html'))

        items = list(spider.parse_person(response))
        item = items[0]

        self.assertEqual(item['first_name'], u'Česlovas')
        self.assertEqual(item['last_name'], u'Juršėnas')
        self.assertEqual(item['email'], [u'Ceslovas.Jursenas@lrs.lt',
                                         u'cejurs@lrs.lt'])
        self.assertEqual(item['home_page'],
                'http://www3.lrs.lt/pls/inter/w5_show?p_r=4487&p_k=1')
        self.assertEqual(item['phone'], ['2396025', '2396626'])
