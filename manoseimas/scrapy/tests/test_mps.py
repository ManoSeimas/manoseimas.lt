# coding: utf-8

import unittest
from scrapy.http import HtmlResponse

from manoseimas.scrapy.spiders.mps import MpsSpider
from manoseimas.scrapy.tests.utils import fixture


def parse_mp():
    spider = MpsSpider()
    url = ('http://www.lrs.lt/sip/portal.show?p_r=8801&p_k'
        '=1&p_a=seimo_narys&p_asm_id=7190')
    response = HtmlResponse(url, body=fixture('mp_7190.html'))
    items = list(spider.parse_person(response))
    return items[0]


class TestMpsSpider(unittest.TestCase):
    def test_karbauskis(self):
        spider = MpsSpider()
        url = ('http://www.lrs.lt/sip/portal.show?p_r='
            '8801&p_k=1&p_a=seimo_narys&p_asm_id=7190')
        response = HtmlResponse(url, body=fixture('mp_7190.html'))
        items = list(spider.parse_person(response))
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item['_id'], '7190p')
        self.assertEqual(item['parliament'], ['2016-2020', '2000-2004', '1996-2000'])
        self.assertEqual(item['first_name'], u'Ramūnas')
        self.assertEqual(item['last_name'], u'Karbauskis')
        self.assertEqual(item['email'], ['Ramunas.Karbauskis@lrs.lt'])
        self.assertEqual(item['phone'], ['852396102'])
        self.assertEqual(item['constituency'], u'Šilainių (Nr. 14) apygardoje')
        self.assertEqual(item['raised_by'], u'Lietuvos valstiečių ir žaliųjų sąjunga')
        self.assertEqual(
            item['photo'],
            ('http://www.lrs.lt/SIPIS/sn_foto/2016/ramunas_karbauskis.jpg'))

        self.assertEqual(len(item['groups']), 16)
        # self.assertTrue(len(item['biography']) > 0)
        # self.assertEqual(item['dob'], '1969-12-05')

    def test_adomenas(self):
        spider = MpsSpider()
        url = ('http://www.lrs.lt/sip/portal.show?p_r='
                 '8801&p_k=1&p_a=seimo_narys&p_asm_id=48690')
        response = HtmlResponse(url, body=fixture('mp_48690.html'))

        items = list(spider.parse_person(response))
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item['_id'], '48690p')
        self.assertEqual(item['parliament'], ['2016-2020', '2012-2016', '2008-2012'])
        self.assertEqual(item['first_name'], 'Mantas')
        self.assertEqual(item['last_name'], u'Adomėnas')
        self.assertEqual(item['email'], ['Mantas.Adomenas@lrs.lt'])
        self.assertEqual(item['phone'], ['852396631'])
        self.assertEqual(item['constituency'], u'Pagal sąrašą')
        self.assertEqual(item['raised_by'], (u'Tėvynės sąjunga - Lietuvos '
                                              u'krikščionys demokratai'))
        self.assertEqual(item['home_page'], 'http://www.adomenas.lt')
        self.assertEqual(
            item['photo'],
            'http://www.lrs.lt/SIPIS/sn_foto/2016/mantas_adomenas.jpg'
        )
        self.assertEqual(len(item['groups']), 22)
        #self.assertTrue(len(item['biography']) > 0)
        #self.assertEqual(item['dob'], '1972-10-01')


    def test_jukneviciene(self):
        spider = MpsSpider()
        url = ('http://www.lrs.lt/sip/portal.show?p_r=8801&'
                 'p_k=1&p_a=seimo_narys&p_asm_id=178')
        response = HtmlResponse(url, body=fixture('mp_178.html'))

        items = list(spider.parse_person(response))
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item['_id'], '178p')
        self.assertEqual(item['parliament'], ['2016-2020', '2012-2016', '2008-2012',
                                                '2004-2008', '2000-2004',
                                                '1996-2000','1990-1992'])
        self.assertEqual(item['first_name'], 'Rasa')
        self.assertEqual(item['last_name'], u'Juknevičienė')
        self.assertEqual(item['email'], ['Rasa.Jukneviciene@lrs.lt', 'rajukn@lrs.lt'])
        self.assertEqual(item['phone'], ['852396711'])
        self.assertEqual(item['constituency'], u'Pagal sąrašą')
        self.assertEqual(item['raised_by'], (u'Tėvynės sąjunga - Lietuvos '
                                              u'krikščionys demokratai'))
        self.assertEqual(item['home_page'], 'http://www.lrs.lt/sip/portal.show?p_r=3034&p_k=1')
        self.assertEqual(
            item['photo'],
            'http://www.lrs.lt/SIPIS/sn_foto/2016/rasa_jukneviciene.jpg'
        )
        self.assertEqual(len(item['groups']), 14)

        #self.assertTrue(len(item['biography']) > 0)
        #self.assertEqual(item['dob'], '1958-01-26')

    def test_sysas(self):
        spider = MpsSpider()
        url = ('http://www.lrs.lt/sip/portal.show?p_r=8801&p_k=1&'
            'p_a=seimo_narys&p_asm_id=7252')
        response = HtmlResponse(url, body=fixture('mp_7252.html'))

        items = list(spider.parse_person(response))
        self.assertEqual(len(items), 1)
        item = items[0]

        self.assertEqual(item['first_name'], u'Algirdas')
        self.assertEqual(item['last_name'], u'Sysas')
        self.assertEqual(item['email'], [u'alsysa@lrs.lt', u'Algirdas.Sysas@lrs.lt'])
        self.assertEqual(item['home_page'], 'http://www.sysas.eu')
        self.assertEqual(item['phone'], ['852396702'])
        self.assertEqual(item['parliament'], [
                                            '2016-2020', '2012-2016',
                                            '2008-2012', '2004-2008',
                                            '2000-2004', '1996-2000'
                                            ])

