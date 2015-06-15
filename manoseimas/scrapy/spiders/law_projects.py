# coding: utf-8
from __future__ import unicode_literals
import re

import datetime

from urllib import urlencode
from urlparse import urlparse, parse_qs, urlunparse

from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector
from scrapy.utils.url import canonicalize_url

from manoseimas.scrapy import pipelines
from manoseimas.scrapy.items import ProposedLawProjectProposer
from manoseimas.scrapy.items import PassedLawProjectProposer
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.spiders import ManoSeimasSpider


def process_mp_page_url(url):
    """
    >>> process_mp_page_url('http://www3.lrs.lt/pls/inter/'
    ...                     'w5_smn_akt_new.seim_nar_proj'
    ...                     '?p_start=2012-11-16&p_end=&p_kad_ses='
    ...                     '&p_asm_id=7198&p_grup_id=8&p_forma=')
    'http://www3.lrs.lt/pls/inter/w5_smn_akt_new.seim_nar_proj?p_asm_id=7198&p_end=&p_forma=&p_grup_id=8&p_kad_ses=&p_no=1&p_rus=&p_start=2012-11-16'
    >>> process_mp_page_url('http://www3.lrs.lt/pls/inter/'
    ...                     'w5_smn_akt_new.seim_nar_proj'
    ...                     '?p_start=2012-11-16&p_end=&p_kad_ses='
    ...                     '&p_asm_id=7198&p_grup_id=8&p_forma=&p_no=2')
    'http://www3.lrs.lt/pls/inter/w5_smn_akt_new.seim_nar_proj?p_asm_id=7198&p_end=&p_forma=&p_grup_id=8&p_kad_ses=&p_no=2&p_rus=&p_start=2012-11-16'
    """  # noqa
    parts = urlparse(url)
    qs = parse_qs(parts.query, keep_blank_values=True)
    if 'p_no' not in qs:
        qs['p_no'] = 1
    if 'p_rus' not in qs:
        qs['p_rus'] = ''
    new_url = urlunparse([
        parts.scheme,
        parts.netloc,
        parts.path,
        parts.params,
        urlencode(qs, doseq=True),
        parts.fragment,
    ])

    return canonicalize_url(new_url)


class LawProjectSpider(ManoSeimasSpider):
    name = 'law_projects'
    allowed_domains = ['lrs.lt']

    start_urls = [
        ('http://www3.lrs.lt/pls/inter/w5_smn_akt_new.seim_nar_proj'
         '?p_kad_ses=k7&p_start=2012-11-16'),
    ]

    mp_projects_link_extractor = LxmlLinkExtractor(
        allow=[(r'http://www3.lrs.lt/pls/inter/w5_smn_akt_new\.seim_nar_proj'
                '\?p_asm_id=\d+'
                '&p_end='
                '&p_forma='
                '&p_grup_id=8'
                '&p_kad_ses='
                '&p_start=2012-11-16'),
               (r'http://www3.lrs.lt/pls/inter/w5_smn_akt_new\.seim_nar_proj'
                '\?p_asm_id=\d+'
                '&p_end=[^&]*'
                '&p_forma=[^&]*'
                '&p_grup_id=[^&]*'
                '&p_kad_ses=[^&]*'
                '&p_no=\d+'
                '&p_rus=[^&]*'
                '&p_start=[^&]*'),
               ],
        process_value=process_mp_page_url,
    )

    rules = [
        Rule(mp_projects_link_extractor, 'parse_mp_project_index'),
    ]

    pipelines = (
        pipelines.ManoSeimasModelPersistPipeline,
    )

    def _extract_proposal_no(self, xs):
        match = xs.xpath('td[2]/a/text()').re(r'(XI{1,3}P-\d+)')
        if match:
            return match[0]

    def _extract_passed_no(self, xs):
        match = xs.xpath('text()').re(r'.*(XI{1,3}-\d+)')
        if match:
            return match[0]

    def _parse_project_row(self, xs, response):

        loader = Loader(self, item=ProposedLawProjectProposer(), selector=xs,
                        response=response)
        doc_id = self._get_query_attr(xs.xpath('td[3]/a/@href').extract()[0],
                                      'p_id')
        loader.add_value('id', doc_id)
        isodate = xs.xpath('td[2]/text()').extract()[0]
        proposal_date = datetime.date(*map(int, isodate.split('-')))
        loader.add_value('date', proposal_date)
        loader.add_xpath('project_name', 'td[3]/text()')
        loader.add_xpath('project_url', 'td[3]/a/@href')
        loader.add_value('project_number', self._extract_proposal_no(xs))
        loader.add_value('source', self._get_source(response.url, 'p_asm_id'))
        loader.add_value('project_number', self._extract_proposal_no(xs))
        yield loader
        passed_xs = xs.xpath('td[4]/a')
        if passed_xs:
            loader = Loader(self, item=PassedLawProjectProposer(),
                            selector=passed_xs, response=response)
            doc_id = self._get_query_attr(
                passed_xs.xpath('@href').extract()[0], 'p_id'
            )
            loader.add_value('id', doc_id)
            doc_number = self._extract_passed_no(passed_xs)
            loader.add_value('passing_number', doc_number)
            loader.add_xpath('passing_url', '@href')
            loader.add_value('date', proposal_date)
            loader.add_value('source', self._get_source(response.url,
                                                        'p_asm_id'))
            yield loader

    def parse_mp_project_index(self, response):
        sel = Selector(response)
        main_xs = sel.xpath('/html/body/div/table/tr[3]/td/table/tr/td/*')
        mp_name = main_xs.xpath('h4/text()').extract()[0]
        xs = main_xs.xpath('div/table/tr/td/table[@class="basic"]/tr[td]')
        for row_xs in xs:
            for loader in self._parse_project_row(row_xs, response):
                loader.add_value('proposer_name', mp_name)
                yield loader.load_item()
