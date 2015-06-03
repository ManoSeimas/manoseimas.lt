# coding: utf-8
import re
from datetime import time, date, datetime

from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector

from manoseimas.scrapy.linkextractors import QualifiedRangeSgmlLinkExtractor
from manoseimas.scrapy.spiders import ManoSeimasSpider
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.items import StenogramTopic
from manoseimas.scrapy.textutils import clean_text
from manoseimas.scrapy.textutils import extract_text
from manoseimas.scrapy.textutils import strip_tags


MINIMUM_SESSION = 95

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

date_re = re.compile(r'(\d{4})\s+m\.\s+(\w+)\s+(\d{1,2})\s+d\.',
                     re.UNICODE)
sitting_no_re = re.compile(r'.*NR.\s(\d+)', re.UNICODE)


def as_statement(paragraph):
    text = extract_text(
        paragraph.xpath('self::p'),
        kill_tags=['b'],
    )
    return re.sub(r'^\([A-Z-]+\)', '', text).lstrip('.').strip()


mp_name_regexps = (
    # PIRMININKĖ (N. SURNAME, FRACT)
    # PIRMININKAS (N. SURNAME, FRACT)
    re.compile(
        ur'((?:PIRMININKĖ|PIRMININKAS)\s\(\w\.\s[\w-]+,\s*[\w-]+[\W]*\))',
        re.UNICODE
    ),
    # PIRMININKĖ (N. SURNAME)
    # PIRMININKAS (N. SURNAME)
    re.compile(ur'((?:PIRMININKĖ|PIRMININKAS)\s\(\w\.\s[\w-]+\))',
               re.UNICODE),
    # PIRMININKĖ
    # PIRMININKAS
    re.compile(ur'(PIRMININKĖ|PIRMININKAS)\s*\.?', re.UNICODE),

    # N. N. SURNAME (FRACT)
    re.compile(ur'^(\w\.\s\w\.\s[\w-]+)\s*\([\w-]+[\W]*\)', re.UNICODE),
    # N. SURNAME (FRACT)
    re.compile(ur'^(\w\.\s[\w-]+)\s*\([\w-]+[\W]*\)', re.UNICODE),

    # N. N. SURNAME.
    re.compile(ur'^(\w\.\s\w\.\s[\w-]+)\s*\.', re.UNICODE),
    # N. SURNAME.
    re.compile(ur'^(\w\.\s[\w-]+)\s*\.', re.UNICODE),

    # N. SURNAME (TEXT TEXT). - some title or explanation
    re.compile(ur'^(\w\.\s[\w-]+)\s*\([^)]+\)', re.UNICODE),
)


def extract_mp_name(paragraph):
    """MP name formats:
    """
    text = clean_text(strip_tags(paragraph)).strip()
    for rule in mp_name_regexps:
        match = rule.match(text)
        if match:
            return match.group(1)
    else:
        return None


class SittingChairpersonProcessor(object):
    """Stateful Chair -> MP name converter
    """

    def __init__(self):
        self.name = None
        self.fraction = None

    def process_mp(self, name, fraction):
        if name.lower().startswith((u'pirmininkas', u'pirmininkė')):
            name_match = re.match(r'.*\(([^,]+)(?:,\s([^)]+)|)\)', name)
            if name_match:
                self.name = name_match.group(1).strip()
                self.fraction = name_match.group(2) or None
            if self.name:
                name = self.name
                fraction = self.fraction
        return name, fraction


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

    mp_processor_classes = (SittingChairpersonProcessor,)

    def _extract_title(self, paragraph):
        return {'type': 'title',
                'title': extract_text(
                    paragraph.xpath('self::p//text()[normalize-space()]')
                )}

    def _extract_time(self, paragraph):
        time_parts = map(int, paragraph.re(r'(\d{1,2})\s*\.\s*(\d{2})'))
        return {'type': 'time',
                'time': time(time_parts[0], time_parts[1])}

    def _extract_statement_start(self, paragraph):
        speaker = re.sub(
            u'\xa0', ' ',
            extract_mp_name(paragraph.extract())
        )
        return {'type': 'statement_start',
                'speaker': speaker,
                'fraction': extract_text(
                    paragraph.xpath('b/following-sibling::i/span/text()')
                ) or None,
                'statement': as_statement(paragraph)}

    def _extract_statement_fragment(self, paragraph):
        return {'type': 'statement_fragment',
                'statement': as_statement(paragraph)}

    def _parse_paragraphs(self, paragraph_xs):
        for paragraph in paragraph_xs:
            if (paragraph.xpath('self::p[@class="Roman12"]')
                    or paragraph.xpath('a[starts-with(@class, "klausimas")]')):
                yield self._extract_title(paragraph)
            elif (paragraph.xpath('self::p[@class="Laikas"]')
                  and extract_text(paragraph.xpath('text()'))):
                yield self._extract_time(paragraph)
            elif (extract_text(paragraph.xpath('self::p/b'))
                  and extract_mp_name(paragraph.extract())):
                yield self._extract_statement_start(paragraph)
            elif as_statement(paragraph):
                yield self._extract_statement_fragment(paragraph)

    def _create_mp_processors(self):
        self.mp_processors = [cls() for cls in self.mp_processor_classes]

    def _process_mp(self, name, fraction):
        for mp_processor in self.mp_processors:
            name, fraction = mp_processor.process_mp(name, fraction)
        return name, fraction

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
        self._create_mp_processors()
        topics = []
        topic = None
        speaker = None
        for p in parsed_paragraphs:
            if p['type'] == 'time':
                if topic and topic.get('time'):
                    topics.append(topic)
                if not topic:
                    topic = None
                topic = {
                    'statements': [],
                }
                topic['time'] = p['time']
            elif p['type'] == 'title':
                if not topic:
                    topic = {
                        'statements': [],
                    }
                topic['title'] = p['title']
            elif p['type'] == 'statement_start':
                name, fraction = self._process_mp(p['speaker'], p['fraction'])
                speaker = {'speaker': name,
                           'fraction': fraction}

                if topic:
                    topic['statements'].append(
                        {'speaker': speaker['speaker'],
                         'fraction': speaker['fraction'],
                         'statement': [p['statement']]}
                    )
            elif p['type'] == 'statement_fragment' and topic is not None:
                # Sometimes speaker is omitted in stenograms
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

    def _parse_stenogram_meta(self, response, meta_xs):
        meta = {}
        source = self._get_source(response.url, 'p_id')
        meta['source'] = source
        meta['_id'] = source['id']
        date_match = meta_xs.re(date_re)
        if date_match:
            year = int(date_match[0])
            month = month_names_map[date_match[1]]
            day = int(date_match[2])
            meta['date'] = date(year, month, day)
        sitting_no_match = meta_xs.re(sitting_no_re)
        if sitting_no_match:
            meta['sitting_no'] = sitting_no_match[0]
        return meta

    def parse_stenogram(self, response):
        sel = Selector(response)
        meta_xs = sel.xpath('/html/body/div[@class="WordSection1"]')
        meta = self._parse_stenogram_meta(response, meta_xs)
        paragraphs = sel.xpath('/html/body/div[@class="WordSection2"]/p')
        topics = self._group_topics(self._parse_paragraphs(paragraphs))
        for topic in topics:
            try:
                loader = Loader(self, response, StenogramTopic(),
                                required=('_id', 'title', 'date', 'sitting_no',
                                          'statements'))
                loader.add_value('title', topic['title'])
                loader.add_value('date', datetime.combine(meta['date'],
                                                          topic['time']))
                loader.add_value('sitting_no', meta['sitting_no'])
                loader.add_value('statements', topic['statements'])
                loader.add_value('source', meta['source'])
                loader.add_value('_id', meta['_id'])
            except KeyError:
                pass
            else:
                yield loader.load_item()
