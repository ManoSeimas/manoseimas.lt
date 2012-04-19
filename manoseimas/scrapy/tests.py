# coding: utf-8

import os.path
import unittest

from scrapy.http import HtmlResponse

from .spiders.mps import MpsSpider


def fixture(name):
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'fixtures', name)) as f:
        return f.read()


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
        self.assertEqual(item['email'], 'Antanas.Nedzinskas@lrs.lt')
        self.assertEqual(item['phone'], '2396694')
        self.assertEqual(item['raised_by'], u'Tautos prisikėlimo partija')
        self.assertEqual(item['candidate_page'],
                ('http://www.vrk.lt/rinkimai/400_lt/Kandidatai/'
                 'Kandidatas22997/Kandidato22997Anketa.html'))
        self.assertEqual(item['photo'],
                ('http://www3.lrs.lt/home'
                 '/seimo_nariu_nuotraukos/2008/antanas_nedzinskas.jpg'))
        self.assertEqual(len(item['groups']), 12)

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
        self.assertEqual(item['birth_place'], 'Vilniuje')
        self.assertEqual(item['email'], 'Mantas.Adomenas@lrs.lt')
        self.assertEqual(item['phone'], '2396631')
        self.assertEqual(item['office_address'], u'Odminių g. 3, 01122 '
                                                 u'Vilniaus m.')
        self.assertEqual(item['constituency'], u'Senamiesčio')
        self.assertEqual(item['raised_by'], (u'Tėvynės sąjunga - Lietuvos '
                                             u'krikščionys demokratai'))
        self.assertEqual(item['home_page'], 'http://www.adomenas.lt')
        self.assertEqual(item['candidate_page'],
                ('http://www.vrk.lt/rinkimai/400_lt/Kandidatai/'
                 'Kandidatas19624/Kandidato19624Anketa.html'))
        self.assertEqual(item['photo'],
                ('http://www3.lrs.lt/home'
                 '/seimo_nariu_nuotraukos/2008/mantas_adomenas.jpg'))
        self.assertEqual(len(item['groups']), 31)


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
        self.assertEqual(len(item['groups']), 9)
