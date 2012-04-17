# coding: utf-8

import re
import urllib
from collections import defaultdict

from lxml.html.clean import clean_html

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from manoseimas.scrapy.items import LegalAct, DocumentInvolved
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.spiders import ManoSeimasSpider
from manoseimas.scrapy.utils import get_absolute_url
from manoseimas.scrapy.utils import get_all
from manoseimas.scrapy.utils import get_first
from manoseimas.scrapy.utils import split_by_words

DOCUMENT_INVOLVED_PARTS = re.compile(ur'(\d+-\d+-\d+) ([^-]+)- (.+)')
REQUIRED_FIELDS = ('_id', 'name', 'kind', 'number', 'date', 'source',)


class LegalActsSpider(ManoSeimasSpider):
    name = 'legal-acts'
    allowed_domains = ['lrs.lt']

    # p_drus - document type
    # p_kalb_id - language
    # p_rus - order by
    # p_gal - document status
    start_urls = [
        # # Current versions
        # ('http://www3.lrs.lt/pls/inter3/dokpaieska.rezult_l?'
        #  'p_drus=102&p_kalb_id=1&p_rus=1&p_gal=33'),
        # Legislation
        ('http://www3.lrs.lt/pls/inter3/dokpaieska.rezult_l?'
         'p_drus=1&p_kalb_id=1&p_rus=1&p_gal='),
        # # Law drafts
        # ('http://www3.lrs.lt/pls/inter3/dokpaieska.rezult_l?'
        #  'p_drus=2&p_kalb_id=1&p_rus=1&p_gal='),
        # Constitution
        ('http://www3.lrs.lt/pls/inter3/dokpaieska.rezult_l?'
         'p_drus=8&p_kalb_id=1&p_rus=1&p_gal='),

        #'http://www3.lrs.lt/pls/inter3/dokpaieska.rezult_l?p_nr=&p_nuo=2010%2006%2001&p_iki=&p_org=&p_drus=2&p_kalb_id=1&p_title=&p_text=&p_pub=&p_met=&p_lnr=&p_denr=&p_es=0&p_rus=1&p_tid=&p_tkid=&p_t=0&p_tr1=2&p_tr2=2&p_gal=',

    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=r'dokpaieska.rezult_l\?')),
        Rule(SgmlLinkExtractor(allow=r'dokpaieska.susije_l\?p_id=-?\d+$'),
             'parse_related_documents'),
        Rule(SgmlLinkExtractor(allow=r'dokpaieska.showdoc_l\?p_id=-?\d+.*',
                               deny=r'p_daug=[1-9]'),
             'parse_document'),
    )

    def _fix_name_case(self, act):
        name = act.get_output_value('name')
        for idx, words in (
                    (-2, (u'ĮSTATYMO PROJEKTAS')),
                    (-1, (u'ĮSTATYMAS')),
                ):
            a, b = split_by_words(name, idx)
            if b in words:
                act.replace_value('name', '%s %s' % (a, b.lower()))
                return

    def _parse_law_act(self, response, hxs, base=False):
        """
        Extracts basic document information and returns law act loader.

        Parameters:

        base
            Return only base information about document. This is used, when
            filling some information bits to a law act from several law act
            documents.

        """
        lang = hxs.select('tr[1]/td[4]/b/text()').extract()[0].strip().lower()

        if lang not in (u'lietuvių', u'rusų', u'anglų', u'ispanų'):
            self.error(response, 'Unknown language: %s' % lang)

        if lang != u'lietuvių':
            return None

        act = Loader(self, response, LegalAct(), hxs,
                          required=REQUIRED_FIELDS)

        act.add_xpath('_id', 'tr[1]/td[2]/b/text()')

        source = self._get_source(response.url, 'p_id')

        if not act.get_output_value('_id'):
            act.replace_value('_id', u'NONUMBER-%s' % source['id'])

        if base:
            return act

        act.add_xpath('name', 'caption/text()')
        act.add_xpath('kind', 'tr[1]/td[1]/b/text()')
        act.add_xpath('number', 'tr[1]/td[2]/b/text()')
        act.add_xpath('date', 'tr[1]/td[3]/b/text()')

        act.add_value('source', source)

        self._fix_name_case(act)

        return act

    def _involved_parts(self, response, hxs, act):
        involved_string = hxs.select('tr[3]/td[1]/b/text()').extract()
        involved_string = ' '.join(involved_string)
        if not involved_string:
            return None

        m = DOCUMENT_INVOLVED_PARTS.match(involved_string)
        if not m:
            return None

        involved = Loader(self, response, DocumentInvolved(), hxs,
                          required=('date', 'how', 'institution',))
        involved.add_value('date', m.group(1))
        involved.add_value('how', m.group(2).lower())
        institution = m.group(3)
        if ',' in institution:
            # TODO: move this to utility function, same code is also used
            # in manoseimas/scrapy/spiders/mps.py:171
            spl = institution.replace(
                    u'Švietimo, mokslo', u'Švietimo%2c mokslo')
            spl = map(lambda x: urllib.unquote(x.strip()),
                                  spl.split(','))
            spl = filter(None, spl)
            if len(spl) == 2:
                person, institution = spl
            else:
                person, group, institution = spl
                spl = group.strip().split()
                group_types = (u'komitetas', u'grupė', u'frakcija',
                               u'komisija')
                if spl[-1].lower() in group_types:
                    group_type = spl[-1].lower()
                elif spl[0].lower() in group_types:
                    group_type = spl[0].lower()
                else:
                    group_type = None

                if group_type:
                    involved.add_value('group', group)
                    involved.add_value('group_type', group_type)
                else:
                    self.error(response, 'Not committee: %s' % group)
            involved.add_value('person', person)
        involved.add_value('institution', institution)
        act.add_value('involved', dict(involved.load_item()))

    def _extract_html_as_attachment(self, response, loader, xpath, name):
        text = HtmlXPathSelector(response).select(xpath).extract()
        text = clean_html('\n'.join(text))
        loader.add_value('_attachments', [(name, text.encode('utf-8'))])

    def _get_legislation_links(self, response, hxs):
        for link in hxs.select('tr[4]/td/a'):
            text = get_first(link, 'text()')
            if text == u'Susiję dokumentai':
                url = get_absolute_url(response, get_first(link, '@href'))
                yield Request(url, callback=self.parse_related_documents)

    def _legislation(self, response, hxs):
        act = self._parse_law_act(response, hxs)
        if not act:
            raise StopIteration

        self._involved_parts(response, hxs, act)

        self._extract_html_as_attachment(response, act,
                "/html/body/*[name()='div' or name()='pre']",
                'original_version.html')

        act.reset_required(*(REQUIRED_FIELDS + ('_attachments',)))
        yield act.load_item()

        for request in self._get_legislation_links(response, hxs):
            yield request

    def _current_edition(self, response, hxs):
        # Do not collect documents, if they are not currently valid.
        valid_edition = hxs.select('tr[4]/td[1]/a[2]/font/b/text()')
        if (valid_edition and
            valid_edition.extract()[0] == u'Galiojanti aktuali redakcija'):
            raise StopIteration

        act = self._parse_law_act(response, hxs, base=True)

        if act:
            self._extract_html_as_attachment(response, act,
                    "/html/body/*[name()='div' or name()='pre']",
                    'updated_version.html')
            act.reset_required('_id', '_attachments')
            yield act.load_item()

    def parse_document(self, response):
        # Some thimes lrs.lt returns empty page...
        if not response.body:
            return

        xpath = '/html/body/table[2]'
        hxs = HtmlXPathSelector(response).select(xpath)[0]

        # Get document kind
        kind = hxs.select('tr[1]/td[1]/b/text()').extract()[0].strip().lower()

        if kind in (u'konstitucija', u'įstatymas', u'įstatymo projektas',
                  u'kodeksas'):
            items = self._legislation(response, hxs)
        elif kind == u'aktuali redakcija':
            items = self._current_edition(response, hxs)
        else:
            items = []

        for item in items:
            yield item

    def parse_related_documents(self, response):
        xpath = '/html/body/div/table/tr[3]/td/table/tr/td/table/tr'
        hxs = HtmlXPathSelector(response).select(xpath)
        act = Loader(self, response, LegalAct(), hxs, required=('_id',))
        act.add_xpath('_id', 'td[2]/b/text()')

        if not act.get_output_value('_id'):
            p_id = unicode(self._get_query_attr(response.url, 'p_id'))
            act.replace_value('_id', u'NONUMBER-%s' % p_id)

        relations = defaultdict(list)
        xpath = '/html/body/div/table/tr[3]/td/table/tr/td/align/table/tr'
        for row in HtmlXPathSelector(response).select(xpath):
            docid = get_all(row, 'td[4]/span//text()')
            rel_type = row.select('td[6]/span/text()')
            if rel_type:
                rel_type = rel_type.extract()[0].strip().lower()

            if rel_type in (u'pakeistas dokumentas',
                            u'ankstesnė dokumento redakcija'):
                relations['amends'].append(docid)

            elif rel_type == u'priimtas dokumentas':
                relations['adopts'].append(docid)

            elif rel_type == u'ryšys su taikymą nusakančiu dokumentu':
                relations['defines_applicability'].append(docid)

            elif rel_type == u'ryšys su galiojimą nusakančiu dokumentu':
                relations['defines_validity'].append(docid)

            elif rel_type == u'negalioja de jure':
                relations['defines_as_no_longer_valid'].append(docid)

            elif rel_type == u'kitas projekto variantas':
                relations['new_draft_version'].append(docid)

            elif rel_type == u'kitas projekto variantas':
                relations['new_draft_version'].append(docid)

            elif rel_type == u'ryšys su ratifikavimo dokumentu':
                relations['ratification'].append(docid)

        if relations:
            act.add_value('relations', dict(relations))
            yield act.load_item()

    def _find_related_law(self, db, doc):
        keyword = u' įstatymo '
        if 'name' not in doc or keyword not in doc['name']:
            return False

        name = doc['name'].split(keyword, 2)[0] + u' įstatymas'
        rs = db.view('scrapy/by_name', key=name, include_docs=True)
        if len(rs) > 0:
            doc.setdefault('relations', {})['law'] = [rs.rows[0]['id']]
            return True

    def _set_type(self, db, doc):
        if 'kind' not in doc:
            return False

        if (doc['kind'] in (u'įstatymas', u'konstitucija') and
            not doc.get('relations')):
            doc['type'] = u'įstatymas'
            return True

        elif doc['kind'] == u'įstatymas':
            doc['type'] = u'įstatymo pataisa'
            return True

    def post_process(self, db, started):
        #for row in db['legalact'].view('scrapy/by_update_time',
        #                               startkey=started, include_docs=True):
        for row in db['legalact'].view('_all_docs', include_docs=True):
            doc = row.doc

            changed = False
            for fn in (self._set_type, self._find_related_law):
                changed = fn(db['legalact'], doc) or changed

            if changed:
                db['legalact'][doc['_id']] = doc
