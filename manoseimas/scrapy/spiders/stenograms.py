# coding: utf-8
import re
from datetime import time

from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector

from manoseimas.scrapy.linkextractors import QualifiedRangeSgmlLinkExtractor
from manoseimas.scrapy.spiders import ManoSeimasSpider
from manoseimas.scrapy.textutils import extract_text


MINIMUM_SESSION = 95


def as_statement(paragraph):
    text = extract_text(
        paragraph.xpath('self::p'),
        kill_tags=['b'],
    )
    return re.sub(r'^\([A-Z-]+\)', '', text).lstrip('.').strip()


class StenogramSpider(ManoSeimasSpider):

    name = 'stenograms'
    allowed_domains = ['lrs.lt']
    session_range = [(MINIMUM_SESSION, None), (None, None)]

    start_urls = ['http://www3.lrs.lt/pls/inter/w5_sale.kad_ses']

    stenogram_link_extractor = LxmlLinkExtractor(
        allow=[r'/pls/inter/dokpaieska.showdoc_l\?p_id=\d+'],
        restrict_xpaths=[('//a[text()="Stenograma"]')]
    )

    rules = (
        Rule(QualifiedRangeSgmlLinkExtractor(
            allow=[
                # List of Seimas sittings
                r'/pls/inter/w5_sale\.ses_pos\?p_ses_id=(\d+)',
                # List of days with early and late sessions
                r'/pls/inter/w5_sale\.fakt_pos\?p_fakt_pos_id=(-?\d+)'
            ], allow_range=session_range)
        ),
        Rule(stenogram_link_extractor, 'parse_stenogram'),
    )

    def _extract_title(self, paragraph):
        return {'type': 'title',
                'title': extract_text(
                    paragraph.xpath('self::p//text()[normalize-space()]')
                )}

    def _extract_time(self, paragraph):
        time_parts = map(int, paragraph.re(r'(\d{1,2})\.(\d{2})'))
        return {'type': 'time',
                'time': time(time_parts[0], time_parts[1])}

    def _extract_statement_start(self, paragraph):
        return {'type': 'statement_start',
                'speaker': extract_text(
                    paragraph.xpath('b/span/text()')
                ).strip('.'),
                'fraction': extract_text(
                    paragraph.xpath('b/following-sibling::i/span/text()')
                ) or None,
                'statement': as_statement(paragraph)}

    def _extract_statement_fragment(self, paragraph):
        return {'type': 'statement_fragment',
                'statement': as_statement(paragraph)}

    def _parse_paragraphs(self, paragraph_xs):
        for paragraph in paragraph_xs:
            if paragraph.xpath('self::p[@class="Roman12"]'):
                yield self._extract_title(paragraph)
            elif paragraph.xpath('self::p[@class="Laikas"]'):
                yield self._extract_time(paragraph)
            elif extract_text(paragraph.xpath('self::p/b')):
                yield self._extract_statement_start(paragraph)
            elif extract_text(paragraph.xpath('self::p/text()')):
                yield self._extract_statement_fragment(paragraph)

    def _group_topics(self, parsed_paragraphs):
        """Structure:
        [
            {
                topic: title
                time: time
                statements: [
                    {
                        speaker: speaker (abbriavated)
                        fraction: fraction or None
                        statement: assembled statement
                    }
                ]
            }
        ]

        """
        topics = []
        topic = None
        speaker = None
        for p in parsed_paragraphs:
            if p['type'] == 'time':
                if topic:
                    topics.append(topic)
                topic = {
                    'time': p['time'],
                    'statements': [],
                }
            elif p['type'] == 'title':
                topic['title'] = p['title']
            elif p['type'] == 'statement_start':
                speaker = {'speaker': p['speaker'],
                           'fraction': p['fraction']}

                # XXX Drop initial speech for now
                if topic:
                    topic['statements'].append(
                        {'speaker': speaker['speaker'],
                         'fraction': speaker['fraction'],
                         'statement': [p['statement']]}
                    )
            elif p['type'] == 'statement_fragment':
                # Sometimes spekaer is omitted in stenograms
                # when starting a new topic. Assume it's the last speaker of
                # previous topic (likely the chair of meeting)
                if not topic['statements']:
                    topic['statements'].append(
                        {'speaker': speaker['speaker'],
                         'fraction': speaker['fraction'],
                         'statement': [p['statement']]}
                    )
                else:
                    topic['statements'][-1]['statement'].append(p['statement'])
        if topic:
            topics.append(topic)
        return topics

    def parse_stenogram(self, response):
        sel = Selector(response)
        paragraphs = sel.xpath('/html/body/div[@class="WordSection2"]/p')
        topics = self._group_topics(self._parse_paragraphs(paragraphs))
        return topics
