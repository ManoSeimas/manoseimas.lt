# coding: utf-8

import re

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import HtmlXPathSelector

from manoseimas.scrapy.items import Group
from manoseimas.scrapy.items import Person
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.spiders import ManoSeimasSpider
from manoseimas.scrapy.textutils import mapwords
from manoseimas.scrapy.textutils import str2dict

group_meta_re = re.compile(r', ([^(]+)(\([^)]+)?')
date_re = re.compile(r'\d{4}-\d\d-\d\d')
bio_re = re.compile(ur'Gim\u0117 (\d{4}) m\. (\w+) (\d+) d\.', re.UNICODE)

month_names_map = {
    u'sausio':     1,
    u'vasario':    2,
    u'kovo':       3,
    u'balandžio':  4,
    u'gegužės':    5,
    u'birželio':   6,
    u'liepos':     7,
    u'rugpjūčio':  8,
    u'rugsėjo':    9,
    u'spalio':    10,
    u'lapkričio': 11,
    u'gruodžio':  12,
}

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

    def _parse_group_items(self, response, person, items, group_type):
        for group_hxs in items:
            group = Loader(self, response, Group(), group_hxs,
                           required=('name', 'position'))

            group.add_value('type', group_type)
            group.add_xpath('name', 'a/text()')
            group.add_xpath('source', 'a/@href')

            meta = ''.join(group_hxs.select('text()').extract())
            position, membership = group_meta_re.match(meta).groups()
            group.add_value('position', position)

            membership = date_re.findall(membership or '')
            if len(membership) == 1:
                membership.append(None)
            group.add_value('membership', membership)

            person.add_value('groups', [dict(group.load_item())])

    def _parse_groups(self, response, hxs, person):
        group_type_map = {
            u'Seimo komitetuose': 'committee',
            u'Seimo komisijose': 'commission',
            u'Seimo frakcijose': 'fraction',
        }
        group_type = None
        for item in hxs.select('tr[5]/td/*'):
            tag = item.select('name()').extract()[0]
            tag = tag.lower()
            if tag == 'b':
                name = item.select('text()').extract()[0]
                group_type = group_type_map[name]
            elif group_type and tag == 'ul':
                items = item.select('li')
                self._parse_group_items(response, person, items, group_type)

        items = hxs.select(u'tr[contains(td/b/text(), '
                           u'"Parlamentinėse grupėse")]'
                           u'/following-sibling::tr/td/ul/li')
        self._parse_group_items(response, person, items, 'group')

    def _parse_person_details(self, response):
        xpath = '//table[@summary="Seimo narys"]'
        hxs = HtmlXPathSelector(response).select(xpath)[0]

        source = self._get_source(response.url, 'p_asm_id')
        _id = source['id']

        person_hxs = hxs.select('tr/td/table/tr/td[2]/table/tr[2]/td[2]')
        person = Loader(self, response, Person(), person_hxs,
                        required=('first_name', 'last_name'))
        person.add_value('_id', '%sp' % _id)


        # Details

        split = [
            u'asmeniniai puslapiai',
            u'asmeninis elektroninis paštas',
            u'biuro adresas',
            u'darbo telefonas',
            u'iškėlė',
            u'išrinktas',
            u'kabinetas',
            u'kandidato puslapis',
            u'padėjėja sekretorė',
            u'seimo narys',
        ]
        details = ' '.join(person_hxs.select('descendant::text()').extract())
        details = str2dict(split, details, normalize=mapwords({
            u'išrinkta': u'išrinktas',
            u'seimo narė': u'seimo narys',
        }))
        details = dict(details)

        person.add_value('constituency', [details.get(u'išrinktas', '')])
        person.add_value('raised_by', [details.get(u'iškėlė', '')])
        person.add_value('email',
                [details.get(u'asmeninis elektroninis paštas', '')])
        person.add_value('phone', [details.get(u'darbo telefonas', '')])
        person.add_value('office_address', [details.get(u'biuro adresas', '')])

        person.add_xpath('home_page',
                'a[contains(font/text(), "Asmeniniai puslapiai")]/@href')
        person.add_xpath('candidate_page',
                'a[contains(text(), "Kandidato puslapis")]/@href')

        person.add_value('source', source)

        # photo
        photo = hxs.select('tr/td/table/tr/td/div/img/@src').extract()[0]
        person.add_value('photo', photo)

        header_hxs = hxs.select('tr/td/table/tr/td[2]/table/tr/td[2]')

        # parliament
        parliament = header_hxs.select('div/b/font/text()')
        parliament = parliament.re(r'(\d{4}-\d{4})')
        person.add_value('parliament', parliament)
        if u'seimo narys' in details:
            keys = ['nuo', 'iki']
            membership = dict(str2dict(keys, details[u'seimo narys']))
            parliament_group = {
                'type': 'parliament',
                'name': parliament,
                'position': u'seimo narys',
                'membership': [membership['nuo'], membership.get('iki')],
            }
            person.add_value('groups', [parliament_group])

        # name (first name, last name)
        name = header_hxs.select('div/b/font[2]/text()').extract()[0]
        self._parse_name(person, name)

        # groups
        party_name = person.get_output_value('raised_by')
        person.add_value('groups', [{'type': 'party', 'name': party_name}])
        self._parse_groups(response, hxs, person)

        # biography
        xpath = (u'tr/td/table/'
                 u'tr[contains(descendant::text(), "Biografija")]/'
                 u'following-sibling::tr/td/'
                 u'descendant::*[contains(text(), "Gimė")]/text()')
        bio_hxs = hxs.select(u'translate(%s, "\xa0", " ")' % xpath)
        bio = bio_hxs.re(bio_re)
        if bio:
            year, month, day = bio
            month = month_names_map[month]
            dob = u'%s-%02d-%s' % (year, month, day.zfill(2))
            person.add_value('dob', dob)

        # parliamentary history
        xpath = (u'//table[@summary="Istorija"]/'
                 u'tr/td/a[starts-with(b/text(), "Buvo išrinkta")]/'
                 u'following-sibling::text()')
        history_hxs = hxs.select(xpath)
        if history_hxs:
            for item in history_hxs:
                parliament = ''.join(item.re(r'(\d{4}) (-) (\d{4})'))
                person.add_value('parliament', [parliament])

        return person.load_item()

    def parse_person(self, response):
        yield self._parse_person_details(response)
