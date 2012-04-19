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
        self.assertEqual(item['email'], 'Antanas.Nedzinskas@lrs.lt')
        self.assertEqual(item['phone'], '2396694')
        self.assertEqual(item['raised_by'], u'Tautos prisikėlimo partija')
        self.assertEqual(item['candidate_page'],
                ('http://www.vrk.lt/rinkimai/400_lt/Kandidatai/'
                 'Kandidatas22997/Kandidato22997Anketa.html'))
        self.assertEqual(item['photo'],
                ('http://www3.lrs.lt/home'
                 '/seimo_nariu_nuotraukos/2008/antanas_nedzinskas.jpg'))
        self.assertEqual(len(item['groups']), 9)
