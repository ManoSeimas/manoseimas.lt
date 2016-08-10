# coding: utf-8

import re


from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector
from scrapy.contrib.pipeline.images import ImagesPipeline

from manoseimas.scrapy.items import Group
from manoseimas.scrapy.items import Person
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.spiders import ManoSeimasSpider
from manoseimas.scrapy.textutils import mapwords
from manoseimas.scrapy.textutils import split_by_comma
from manoseimas.scrapy.textutils import str2dict
from manoseimas.scrapy import textutils

from manoseimas.scrapy import pipelines
from manoseimas.scrapy.helpers.dates import month_names_map

group_meta_re = re.compile(r'.*, ([^(]+)(?:\(([^)]+)\))?')
date_re = re.compile(r'\d{4}-\d\d-\d\d')
dob_re = re.compile(u'Gim\u0117 (\d{4}) m\. (\w+) (\d+) d\.', re.UNICODE)


# This maps URL components to different Seimas versions
seimas_version_map = {
    786: 0,   # not sure where these numbers come from so adding 0
    6113: 10,
    8801: 11
}


class MpsSpider(ManoSeimasSpider):
    name = 'mps'
    allowed_domains = ['lrs.lt']

    start_urls = [
        'http://www3.lrs.lt/pls/inter/w5_show?p_r=8801&p_k=1',
        # 'http://www3.lrs.lt/pls/inter/w5_show?p_r=6113&p_k=1',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=['p_asm_id=\d+']), 'parse_person'),
    )

    pipelines = (
        ImagesPipeline,
        pipelines.ManoseimasPipeline,
        pipelines.ManoSeimasModelPersistPipeline,
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

            meta = ''.join(group_hxs.xpath('text() | */text()').extract())
            position, membership = group_meta_re.match(meta).groups()
            group.add_value('position', position)

            membership = date_re.findall(membership or '')
            if len(membership) == 1:
                membership.append(None)
            group.add_value('membership', membership)

            person.add_value('groups', [dict(group.load_item())])

    def _parse_biography(self, response, person, hxs):
        try:
            biography = hxs.extract()[0]
        except IndexError:
            pass
        else:
            person.add_value('biography', textutils.clean_html(biography))

    def _parse_groups(self, response, hxs, person):
        group_type_map = {
            u'Seimo komitetuose': 'committee',
            u'Seimo komisijose': 'commission',
            u'Seimo frakcijose': 'fraction',
        }
        group_type = None
        for item in hxs.xpath('tr[5]/td/*'):
            tag = item.xpath('name()').extract()[0]
            tag = tag.lower()
            if tag == 'b':
                name = item.xpath('text()').extract()[0]
                group_type = group_type_map[name]
            elif group_type and tag == 'ul':
                items = item.xpath('li')
                self._parse_group_items(response, person, items, group_type)

        items = hxs.xpath(u'tr[contains(td/b/text(), '
                          u'"Parlamentinėse grupėse")]'
                          u'/following-sibling::tr/td/ul/li')
        self._parse_group_items(response, person, items, 'group')

    def _parse_person_details(self, response):
        xpath = '//table[@summary="Seimo narys"]'
        hxs = Selector(response).xpath(xpath)[0]

        source = self._get_source(response.url, 'p_asm_id')

        seimas_code = self._get_query_attr(response.url, 'p_r')
        if seimas_code:
            source['version'] = seimas_version_map[int(seimas_code)]

        _id = source['id']

        person_hxs = hxs.xpath('tr/td/table/tr/td[2]/table/tr[2]/td[2]')
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
        details = ' '.join(person_hxs.xpath('descendant::text()').extract())
        details = str2dict(split, details, normalize=mapwords({
            u'išrinkta': u'išrinktas',
            u'seimo narė': u'seimo narys',
            u'el p': u'asmeninis elektroninis paštas',
            u'asmeninė svetainė': u'asmeniniai puslapiai',
        }))
        details = dict(details)

        email = details.get(u'asmeninis elektroninis paštas', '')
        phone = details.get(u'darbo telefonas', '')

        person.add_value('constituency', [details.get(u'išrinktas', '')])
        person.add_value('raised_by', [details.get(u'iškėlė', '')])
        person.add_value('email', split_by_comma(email))
        person.add_value('phone', split_by_comma(phone))
        person.add_value('office_address', [details.get(u'biuro adresas', '')])

        person.add_xpath(
            'home_page',
            u'a[contains(font/text(), "Asmeniniai puslapiai") or contains(font/text(), "Asmeninė svetainė")]/@href'
        )
        person.add_xpath('candidate_page',
                         'a[contains(text(), "Kandidato puslapis")]/@href')

        person.add_value('source', source)

        # photo
        photo = hxs.xpath('tr/td/table/tr/td/div/img/@src').extract()[0]
        person.add_value('photo', photo)
        person.add_value('image_urls', photo)

        header_hxs = hxs.xpath('tr/td/table/tr/td[2]/table/tr/td[2]')

        # parliament
        parliament = header_hxs.xpath('div/b/font/text()')
        parliament = parliament.re(r'(\d{4}[-\x97]\d{4})')
        parliament = ''.join(parliament).replace(u'\x97', u'-')
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
        name = header_hxs.xpath('div/b/font[2]/text()').extract()[0]
        self._parse_name(person, name)

        # groups
        party_name = person.get_output_value('raised_by')
        if party_name:
            person.add_value('groups', [{'type': 'party',
                                         'name': party_name,
                                         'position': 'narys'}])

        self._parse_groups(response, hxs, person)

        # date of birth
        xpath = (u'tr/td/table/'
                 u'tr[contains(descendant::text(), "Biografija")]/'
                 u'following-sibling::tr/td/'
                 u'descendant::*[contains(text(), "Gimė")]/text()')
        dob_hxs = hxs.xpath(u'translate(%s, "\xa0", " ")' % xpath)
        dob_match = dob_hxs.re(dob_re)
        if dob_match:
            year, month, day = dob_match
            month = month_names_map[month]
            dob = u'%s-%02d-%s' % (year, month, day.zfill(2))
            person.add_value('dob', dob)

        # biography
        xpath = (u'tr/td/table/'
                 u'tr[contains(descendant::text(), "Biografija")]/'
                 u'following-sibling::tr/td/div')
        bio_hxs = hxs.xpath(xpath)
        self._parse_biography(response, person, bio_hxs)

        # parliamentary history
        xpath = (u'//table[@summary="Istorija"]/'
                 u'tr/td/a[starts-with(b/text(), "Buvo išrinkta")]/'
                 u'following-sibling::text()')
        history_hxs = hxs.xpath(xpath)
        if history_hxs:
            for item in history_hxs:
                parliament = ''.join(item.re(r'(\d{4}) (-) (\d{4})'))
                person.add_value('parliament', [parliament])

        return person.load_item()

    def parse_person(self, response):
        yield self._parse_person_details(response)
