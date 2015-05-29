# coding: utf-8

import unittest
from scrapy.http import HtmlResponse
from scrapy.link import Link
from scrapy.selector import Selector

from manoseimas.scrapy.tests.utils import fixture


from manoseimas.scrapy.textutils import strip_tags, extract_text
from manoseimas.scrapy.spiders.stenograms import StenogramSpider


source_text = u"""<p class="Roman"><b>
<span style="font-size:9.0pt">PIRMININKĖ.</span></b> Ačiū.
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


class StenogramCrawlerTestCase(unittest.TestCase):

    def setUp(self):
        super(StenogramCrawlerTestCase, self).setUp()
        url = 'http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=1034324'
        self.response = HtmlResponse(url,
                                     body=fixture('stenogram_1034324.html'))
        self.spider = StenogramSpider()

    def test_parse_stenogram(self):
        self.spider.parse_stenogram(self.response)
