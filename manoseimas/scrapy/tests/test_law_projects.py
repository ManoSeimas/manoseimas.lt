from __future__ import unicode_literals

from unittest import TestCase

from scrapy.http import HtmlResponse

from manoseimas.scrapy.tests.utils import fixture

from manoseimas.scrapy.spiders.law_projects import LawProjectSpider


class LawProjectUtilsTestCase(TestCase):

    def test_mp_law_project_link_extractor(self):
        url = ('http://www3.lrs.lt/pls/inter/w5_smn_akt_new.seim_nar_proj'
               '?p_kad_ses=k7&p_start=2012-11-16')

        response = HtmlResponse(url=url,
                                body=fixture('law_project_summary.html'))
        links = LawProjectSpider.mp_projects_link_extractor.extract_links(
            response
        )
        self.assertEqual(147, len(links))

    def test_mp_project_page_link_extractor(self):
        url = ('http://www3.lrs.lt/pls/inter/w5_smn_akt_new.seim_nar_proj'
               '?p_start=2012-11-16&p_end=&p_kad_ses=&p_asm_id=7198'
               '&p_grup_id=8&p_forma=')
        response = HtmlResponse(url=url, body=fixture('mp_project_index.html'))
        links = LawProjectSpider.mp_projects_link_extractor.extract_links(
            response
        )
        self.assertEqual(1, len(links))
