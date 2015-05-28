# coding: utf-8
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector

from manoseimas.scrapy.linkextractors import QualifiedRangeSgmlLinkExtractor
from manoseimas.scrapy.spiders import ManoSeimasSpider
from manoseimas.scrapy.textutils import extract_text


MINIMUM_SESSION = 95


def as_statement(paragraph):
    return extract_text(
        paragraph.xpath('self::p/text()[normalize-space()]')
    )


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
                ),
                'para': paragraph}

    def _extract_time(self, paragraph):
        return {'type': 'time',
                'para': paragraph}

    def _extract_statement_start(self, paragraph):
        return {'type': 'statement_start',
                'speaker': extract_text(
                    paragraph.xpath('b/span/text()')
                ).strip('.'),
                'fraction': extract_text(
                    paragraph.xpath('i/text()')
                ) or None,
                'statement': as_statement(paragraph),
                'para': paragraph}

    def _extract_statement_fragment(self, paragraph):
        return {'type': 'statement_fragment',
                'statement': as_statement(paragraph),
                'para': paragraph}

    def _parse_paragraphs(self, paragraph_xs):
        for paragraph in paragraph_xs:
            if paragraph.xpath('self::p[@class="Roman12"]'):
                yield self._extract_title(paragraph)
            elif paragraph.xpath('self::p[@class="Laikas"]'):
                yield self._extract_time(paragraph)
            elif paragraph.xpath('self::p/b'):
                yield self._extract_statement_start(paragraph)
            elif extract_text(paragraph.xpath('self::p/text()')):
                yield self._extract_statement_fragment(paragraph)

    def _group_topics(self, response, paragraph_xs):
        """Structure:
        {
            topics: [
                {
                    topic: title
                    time: time
                    sitting: sitting
                    date: date
                    statements: [
                        {
                            speaker: speaker (abbriavated)
                            fraction: fraction or None
                            statement: assembled statement
                        }
                    ]
                }
            ]
        }

        """
        for p in self._parse_paragraphs(paragraph_xs):
            if p['type'] == 'statement_start':
                print(p['speaker'])
                print(p['statement'])
            elif p['type'] == 'statement_fragment':
                print(p['statement'])

    def parse_stenogram(self, response):
        sel = Selector(response)
        paragraphs = sel.xpath('/html/body/div[@class="WordSection2"]/p')
        return self._group_topics(response, paragraphs)
