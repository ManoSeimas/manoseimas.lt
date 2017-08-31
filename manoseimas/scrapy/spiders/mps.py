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
from manoseimas.scrapy.textutils import str2dict

from manoseimas.scrapy import pipelines
from manoseimas.scrapy.helpers.dates import month_names_map

group_meta_re = re.compile(r'.*, ([^(]+)(?:\(([^)]+)\))?')
date_re = re.compile(r'\d{4}-\d\d-\d\d')
# dob_re = re.compile(u'Gim\u0117 (\d{4}) m\. (\w+) (\d+) d\.', re.UNICODE)
dob_re = re.compile(u'(\d{4}) m\. (\w+) (\d+) d\.', re.UNICODE)


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
        'http://www.lrs.lt/sip/portal.show?p_r=8801&p_k=1',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=['p_asm_id=\d+']), 'parse_person'),
    )

    pipelines = (
        ImagesPipeline,
        pipelines.ManoseimasPipeline,
        pipelines.ManoSeimasModelPersistPipeline,
    )

    def _parse_group_items(self, response, person, items, group_type):
        for group_hxs in items.xpath('tr'):
            group_data_hxs = group_hxs.xpath('td[2]')
            group = Loader(self, response, Group(), group_data_hxs,
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

    def _parse_biography(self, person, hxs):
        # TODO fix incapsula issue
        # biography info is in other tab (url)
        # using Request(url, callback) po parse related data
        # Incapsula block this request

        # Date of birth
        dob_hxs = hxs.xpath(
            'tr/td[contains(descendant::text(), "Gimimo data")'
            ']/following-sibling::td/text()'
        )
        dob_match = dob_hxs.re(dob_re)
        if dob_match:
            year, month, day = dob_match
            month = month_names_map[month]
            dob = u'%s-%02d-%s' % (year, month, day.zfill(2))
            person.add_value('dob', dob)

        # biography
        xpath = (u'tr/td/text()')
        bio_hxs = hxs.xpath(xpath)
        biography = bio_hxs.extract()
        person.add_value('biography', biography)

    def _parse_groups(self, response, hxs, person):
        group_type_map = {
            u'Seimo komitetuose': 'committee',
            u'Seimo komisijose': 'commission',
            u'Seimo frakcijose': 'fraction',
            u'Parlamentinėse grupėse': 'group',
        }
        group_type = None
        groups = Selector(response).xpath(
                '//*/div[contains(@class, "pl-container")]'
                '/div[contains(@class, "pl-head-container")]'
                '/div[contains(@id, "smn-dabar-dirba")]/*'
        )
        for item in groups:
            tag = item.xpath('name()').extract()[0]
            tag = tag.lower()
            if tag == 'h3':
                name = item.xpath('text()').extract()[0]
                group_type = group_type_map[name]
            elif group_type and tag == 'table':
                self._parse_group_items(response, person, item, group_type)

    def _parse_person_details(self, response):
        xpath = '//div[contains(@id,"page-content")]'
        hxs = Selector(response).xpath(xpath)[0]

        source = self._get_source(response.url, 'p_asm_id')

        seimas_code = self._get_query_attr(response.url, 'p_r')
        if seimas_code:
            source['version'] = seimas_version_map[int(seimas_code)]

        _id = source['id']
        person_hxs = hxs.xpath('div/div[contains(@class, "col1")]')
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
            u'buvo išrinktas',
            u'buvo išrinkta',
            u'kontaktai',
        ]
        details = ' '.join(person_hxs.xpath('descendant::text()').extract())

        details = str2dict(split, details, normalize=mapwords({
            u'išrinkta': u'išrinktas',
            u'seimo narė': u'seimo narys',
        }))

        details = dict(details)

        contacts_hxs = hxs.xpath(
            'div/div[contains(@class, "col3")]'
            '/div[contains(@class, "kontaktai")]'
        )
        contacts = ' '.join(contacts_hxs.xpath('descendant::text()').extract())
        contacts_split = [
            u'el p',
            u'tel',
            u'asmeninė svetainė'
        ]
        contacts = str2dict(contacts_split, contacts)
        contacts = dict(contacts)

        if contacts.get('tel'):
            phone = re.sub("[^0-9]", "", contacts.get(u'tel'))
            person.add_value('phone', phone)

        email_xpath = 'div/div[contains(descendant::text(), "El. p.")]/a/text()'
        email_hxs = contacts_hxs.xpath(email_xpath)

        for email in email_hxs:
            person.add_value('email', email.extract())

        # TODO

        person.add_value('office_address', [''])

        website_hxs = contacts_hxs.xpath(
            'div/div[contains(@class, "site")]/a/@href'
        )
        if website_hxs:
            person.add_value(
                'home_page',
                website_hxs.extract()[0]
            )
        person.add_value('raised_by', [details.get(u'iškėlė', '')])
        person.add_value('constituency', [details.get(u'išrinktas', '')])

        person.add_value('source', source)

        # photo
        # first for P leader
        # second for the rest
        photo_selectors = [
            '//*[@id="page-content"]/div/div[1]/div[1]/img/@src',
            '//*[contains(@class, "seimo-nario-foto")]/img/@src',
        ]
        photo = None
        for photo_selector in photo_selectors:
            photo = Selector(response).xpath(photo_selector).extract()
            if photo:
                break
        if photo:
            person.add_value('photo', photo[0])
            person.add_value('image_urls', photo[0])
        # parliament

        parliament = hxs.xpath(
            'div/div/div[contains(@class, "smn-kadencija")]/span/text()'
        )
        parliament = parliament.re(r'(\d{4}[^-]\d{4})')
        parliament = ''.join(parliament).replace(u'\u2013', u'-')
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

        first_name = Selector(response).xpath('//*/div[contains(@class, "smn-name")]/text()').extract()[0]
        last_name = Selector(response).xpath('//*/span[contains(@class, "smn-pavarde")]/text()').extract()[0]

        person.add_value('first_name', unicode(first_name))
        person.add_value('last_name', unicode(last_name.title()))

        # groups
        party_name = person.get_output_value('raised_by')
        if party_name:
            person.add_value('groups', [{'type': 'party',
                                         'name': party_name,
                                         'position': 'narys'}])
        self._parse_groups(response, hxs, person)

        # biography_xpath = 'div/div[2]/div[3]/div/table[2]/tbody'
        # biography_hxs = hxs.xpath(biography_xpath)
        # self._parse_biography(person, biography_hxs)

        # parliamentary history
        xpath = (
                u'div/div[contains(@class, "col1")]/'
                u'p[contains(@class, "buvo-isrinkta")]/descendant::text()'
                )
        history_hxs = hxs.xpath(xpath)

        if history_hxs:
            for item in history_hxs:
                parliament = ''.join(item.re(r'(\d{4}[^-]\d{4})'))
                parliament = parliament.replace(u'\x97', '-')
                person.add_value('parliament', [parliament])

        return person.load_item()

    def parse_person(self, response):
        yield self._parse_person_details(response)
