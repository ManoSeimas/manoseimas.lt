# coding: utf-8
from __future__ import unicode_literals

from urllib import urlencode
from urlparse import urlparse, parse_qs, urlunparse

from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector
from scrapy.utils.url import canonicalize_url

from manoseimas.scrapy.spiders import ManoSeimasSpider


def process_mp_page_url(url):
    """
    >>> process_mp_page_url('http://www3.lrs.lt/pls/inter/'
    ...                     'w5_smn_akt_new.seim_nar_proj'
    ...                     '?p_start=2012-11-16&p_end=&p_kad_ses='
    ...                     '&p_asm_id=7198&p_grup_id=8&p_forma=')
    'http://www3.lrs.lt/pls/inter/w5_smn_akt_new.seim_nar_proj?p_asm_id=7198&p_end=&p_forma=&p_grup_id=8&p_kad_ses=&p_no=1&p_start=2012-11-16'
    >>> process_mp_page_url('http://www3.lrs.lt/pls/inter/'
    ...                     'w5_smn_akt_new.seim_nar_proj'
    ...                     '?p_start=2012-11-16&p_end=&p_kad_ses='
    ...                     '&p_asm_id=7198&p_grup_id=8&p_forma=&p_no=2')
    'http://www3.lrs.lt/pls/inter/w5_smn_akt_new.seim_nar_proj?p_asm_id=7198&p_end=&p_forma=&p_grup_id=8&p_kad_ses=&p_no=2&p_start=2012-11-16'
    """  # noqa
    parts = urlparse(url)
    qs = parse_qs(parts.query, keep_blank_values=True)
    if 'p_no' not in qs:
        qs['p_no'] = 1
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
        allow=[(r'http://www3.lrs.lt/pls/inter/w5_smn_akt_new.seim_nar_proj'
                '\?p_asm_id=\d+'
                '&p_end='
                '&p_forma='
                '&p_grup_id=8'
                '&p_kad_ses='
                '&p_start=2012-11-16'),
               (r'http://www3.lrs.lt/pls/inter/w5_smn_akt_new.seim_nar_proj'
                '\?p_asm_id=\d+'
                '&p_end=[^&]*'
                '&p_forma=[^&]*'
                '&p_grup_id=[^&]*'
                '&p_kad_ses=[^&]*'
                '&p_no=\d+'
                '&p_start=2012-11-16'),
               ],
        process_value=canonicalize_url,
    )

    mp_project_page_link_extractor = LxmlLinkExtractor(
        allow=[(r'http://www3.lrs.lt/pls/inter/w5_smn_akt_new.seim_nar_proj'
                '\?p_asm_id=\d+'
                '&p_end=[^&]*'
                '&p_forma=[^&]*'
                '&p_grup_id=[^&]*'
                '&p_kad_ses=[^&]*'
                '&p_no=\d+'
                '&p_start=2012-11-16')],
        process_value=canonicalize_url,
    )

    rules = [
        Rule(mp_projects_link_extractor, 'parse_mp_project_index'),
    ]

    def parse_mp_project_index(self, response, spider):
        pass
