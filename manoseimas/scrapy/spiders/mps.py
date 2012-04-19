# coding: utf-8

import re

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import HtmlXPathSelector

from manoseimas.scrapy.items import Group
from manoseimas.scrapy.items import Person
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.spiders import ManoSeimasSpider

group_meta_re = re.compile(r', ([^(]+)\(([^)]+)')
date_re = re.compile(r'\d{4}-\d\d-\d\d')


class MpsSpider(ManoSeimasSpider):
    name = 'mps'
    allowed_domains = ['lrs.lt']

    start_urls = [
        'http://www3.lrs.lt/pls/inter/w5_show?p_r=6113&p_k=1',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=['p_asm_id=\d+']), 'parse_person'),
    )

    def _parse_name(self, person, whole_name):
        first, last = [], []
        for name in whole_name.split(' '):
            if name.isupper():
                last.append(name.title())
            else:
                first.append(name)

        person.add_value('first_name', ' '.join(first))
        person.add_value('last_name', ' '.join(last))

    def _parse_groups(self, response, hxs, person):
        group_type_map = {
            u'Seimo komitetuose': 'committee',
            u'Seimo komisijose': 'commission',
            u'Seimo frakcijose': 'fraction',
            u'Parlamentinėse grupėse': 'group',
        }
        for item in hxs.select('tr[5]/td/*'):
            tag = item.select('name()').extract()[0]
            tag = tag.lower()
            if tag == 'b':
                name = item.select('text()').extract()[0]
                group_type = group_type_map[name]
            elif tag == 'ul':
                for group_hxs in item.select('li'):
                    group = Loader(self, response, Group(), group_hxs,
                                   required=('name', 'position'))

                    group.add_value('type', group_type)
                    group.add_xpath('name', 'a/text()')
                    group.add_xpath('source', 'a/@href')

                    meta = ''.join(group_hxs.select('text()').extract())
                    position, membership = group_meta_re.match(meta).groups()
                    group.add_value('position', position)

                    membership = date_re.findall(membership)
                    if len(membership) == 1:
                        membership.append(None)
                    group.add_value('membership', membership)

                    person.add_value('groups', [group.load_item()])

    def _parse_person_details(self, response):
        xpath = '//table[@summary="Seimo narys"]'
        hxs = HtmlXPathSelector(response).select(xpath)[0]

        source = self._get_source(response.url, 'p_asm_id')
        _id = source['id']

        person_hxs = hxs.select('tr/td/table/tr/td[2]/table/tr[2]/td[2]')
        person = Loader(self, response, Person(), person_hxs,
                        required=('first_name', 'last_name'))
        person.add_value('_id', '%sp' % _id)
        person.add_xpath('email', 'b[6]/a/text()')
        person.add_xpath('phone', 'b[4]/text()')
        person.add_xpath('candidate_page', 'a/@href')
        person.add_xpath('raised_by', 'b[10]/text()')
        person.add_value('source', source)

        # photo
        photo = hxs.select('tr/td/table/tr/td/div/img/@src').extract()[0]
        person.add_value('photo', photo)

        # name (first name, last name)
        name_hxs = hxs.select('tr/td/table/tr/td[2]/table/tr/td[2]')
        name = name_hxs.select('div/b/font[2]/text()').extract()[0]
        self._parse_name(person, name)

        # groups
        party_name = person.get_output_value('raised_by')
        person.add_value('groups', [Group(type='party', name=party_name)])
        self._parse_groups(response, hxs, person)

        return person.load_item()

    def parse_person(self, response):
        yield self._parse_person_details(response)
