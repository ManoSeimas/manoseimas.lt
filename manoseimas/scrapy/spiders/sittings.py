# coding: utf-8
import urllib

from manoseimas.scrapy.linkextractors import QualifiedRangeSgmlLinkExtractor

from scrapy.contrib.spiders import Rule
from scrapy.selector import HtmlXPathSelector

from manoseimas.scrapy.items import PersonVote
from manoseimas.scrapy.items import Question
from manoseimas.scrapy.items import QuestionDocument
from manoseimas.scrapy.items import QuestionDocumentSpeaker
from manoseimas.scrapy.items import Registration
from manoseimas.scrapy.items import Session
from manoseimas.scrapy.items import Voting
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.loaders import absolute_url
from manoseimas.scrapy.spiders import ManoSeimasSpider
from manoseimas.scrapy.utils import Increment
from manoseimas.scrapy.db import  get_sequential_votings, get_question


        
class SittingsSpider(ManoSeimasSpider):
    """
    This spider walks through all sittings of Seimas and extracts information
    about questions and documents discussed during sittings. Also it collects
    voting results.
    
    LRS.LT PAGE HIERARCHY:
    All Seimas Sessions
    http://www3.lrs.lt/pls/inter/w5_sale.kad_ses 
     -> List of Seimas sittings, organized by date, broken into morning and afternoon sittings
        Ex: http://www3.lrs.lt/pls/inter/w5_sale.ses_pos?p_ses_id=96
       -> List of events for a particular sitting, including Question discussions
          Ex: http://www3.lrs.lt/pls/inter/w5_sale.fakt_pos?p_fakt_pos_id=-500731
         -> A singular Question discussion
            Ex: http://www3.lrs.lt/pls/inter/w5_sale.klaus_stadija?p_svarst_kl_stad_id=-15596
           -> A singular voting for this Question
              Ex: http://www3.lrs.lt/pls/inter/w5_sale.bals?p_bals_id=-16591

    The rules configured below are designed to resume scraping from where we last 
    left off. We determine where we last left off using the unique, sequential IDs 
    that lrs.lt uses when referencing documents. We take the most recent voting in 
    our database and backtrack to identify the most recent Question, Sitting, and 
    Session and use the QualifiedRangeSgmlLinkExtractor to limit scraping to documents
    published after our most recent Voting.
    """

    name = 'sittings'
    allowed_domains = ['lrs.lt']

    def __init__(self, resume="yes", start_url='http://www3.lrs.lt/pls/inter/w5_sale.kad_ses'):
        #print "Arguments: Start_url: %s ; Resume? %s" % (start_url, resume)

        self.start_urls = [ start_url ]

        # By default, never earlier than Seimas sitting 88, which is Spring 2011. 
        sitting_session_range = [ (88, None), (None, None) ]
        question_range = None
        voting_range = None

        if resume.lower() != "no":
            # Resume spidering from the last stored Voting
            voting = get_sequential_votings(limit=1)[0]
            question = get_question(voting['question'])
            session = question['session']
            #print "VOTING: [_id=%s, question=%s]" % (voting['_id'], voting['question'])
            #print "QUESTION: [_id=%s, session=%s]" % (question['_id'], question['session'])

            # Note: We're incrementing range arguments by 1 because our
            # range comparison expects a standard [a,b) interval, with 2nd-argument
            # exclusivity, and we're dealing with negative numbers. 
            sitting_session_range = [
                    (int(session['id']), None),
                     (None, 1+int(session['fakt_pos_id']))
            ]
            question_range = [ (None, 1+int(question['source']['id'])) ]
            # Note: We increment (see above note) and then decrement in order to 
            # reach the next voting. Net result is 0 offset.
            voting_range = [ (None, int(voting['source']['id'])) ]

        self.rules = (
            Rule(QualifiedRangeSgmlLinkExtractor(
                 allow=[
                        # List of Seimas sittings
                        r'/pls/inter/w5_sale\.ses_pos\?p_ses_id=(\d+)',
                        # List of days with early and late sessions
                        r'/pls/inter/w5_sale\.fakt_pos\?p_fakt_pos_id=(-?\d+)'
                     ],
                 allow_range=sitting_session_range
            )),

            # Discussion on a question
            Rule(QualifiedRangeSgmlLinkExtractor(
                    allow=[r'p_svarst_kl_stad_id=(-?\d+)'], 
                    allow_range=question_range
                 ), 'parse_question', follow=True),

            # Voting results by person
            Rule(QualifiedRangeSgmlLinkExtractor(
                    allow=[r'p_bals_id=(-?\d+)'], 
                    allow_range=voting_range
                ), 'parse_person_votes'),
        )
       
        ManoSeimasSpider.__init__(self)


    def _get_session(self, response, hxs):
        session_id = hxs.select('div[1]/a[1]').re(r'p_ses_id=(\d+)')

        hxs = hxs.select("div[2]/b")

        session = Loader(self, response, Session(), hxs, required=(
            'id', 'fakt_pos_id', 'number', 'date', 'type',))

        session.add_value('id', session_id)
        session.add_value('fakt_pos_id', hxs.select('a[1]').re(r'p_fakt_pos_id=(-\d+)'))
        session.add_value('number', hxs.select('a[1]/text()').re(r'Nr. (\d+)'))
        session.add_xpath('date', 'a[2]/text()')
        session.add_xpath('type', 'a[3]/text()')

        return dict(session.load_item())

    def _parse_question_votes(self, voting, positions):
        """
        Helper method, for adding repeated voting values more easily.
        """
        keys = ('vote_aye', 'vote_no', 'vote_abstain', 'result')
        if positions:
            for pos, key in zip(positions, keys):
                voting.add_xpath(key, 'td[2]/b[%d]/text()' % pos)
        else:
            for pos, key in zip(range(3), keys):
                voting.add_value(key, u'0')

    def _get_question_voting(self, response, item, question):
        date = question['session']['date']
        required = (
            '_id', 'datetime', 'vote_aye', 'vote_no', 'vote_abstain',
            'total_votes', 'question', 'source',
        )

        if item.select(u'td[2][contains(a,"alternatyvus balsavimas:")]'):
            voting_type = u'alternatyvus'
            required += ('formulation_a', 'formulation_b',)
        else:
            voting_type = u'paprastas'

        voting = Loader(self, response, Voting(), item, required=required)

        url = item.select('td[2]/a[1]/@href').extract()[0]
        source = self._get_source(url, 'p_bals_id')
        _id = source['id']

        voting.add_value('_id', '%sv' % _id)
        voting.add_value('type', voting_type)
        voting.add_value('datetime', date)
        voting.add_xpath('datetime', 'td[1]/text()')
        voting.add_value('question', question['_id'])

        if voting_type == u'alternatyvus':
            voting.add_xpath('formulation_a', 'td[2]/text()[3]')
            voting.add_xpath('formulation_b', 'td[2]/text()[5]')
            self._parse_question_votes(voting, (2, 4, 5, 6))
        else:
            formulation = item.select('td[2]/text()[2]').extract()[0].strip()

            # If formulation node is equeal to '(už' it means, that
            # there is no formulation at all.
            if formulation.endswith(u'(už'):
                if not formulation == u'(už':
                    voting.add_value('formulation', formulation[:-3])
                voting_positions = (1, 2, 3)
            else:
                voting.add_value('formulation', formulation)
                voting_positions = (2, 3, 4, 1)

            if item.select('td[2]/b'):
                self._parse_question_votes(voting, voting_positions)
            else:
                self._parse_question_votes(voting, None)

        voting.add_value('source', source)

        return voting

    def _parse_question_agenda(self, response, hxs, question):
        date = question['session']['date']
        registration = None
        for item in hxs:
            # Registration
            if item.select('td[2]/a[1][contains(@href, "p_reg_id=")]'):
                registration = Loader(self, response, Registration(), item,
                                      required=('datetime',))

                url = item.select('td[2]/a[1]/@href').extract()[0]
                _id = unicode(self._get_query_attr(url, 'p_reg_id'))

                registration.add_value('id', _id)
                registration.add_value('datetime', date)
                registration.add_xpath('datetime', 'td[1]/text()')
                registration.add_xpath('joined', 'td[2]/b[1]/text()')

            # Voting
            if item.select('td[2]/a[1][contains(@href, "p_bals_id=")]'):
                voting = self._get_question_voting(response, item, question)
                votes = sum([int(voting.get_output_value('vote_%s' % f))
                             for f in ('aye', 'no', 'abstain')])
                voting.add_value('total_votes', unicode(votes))

                if registration:
                    registration = dict(registration.load_item())
                    joined = int(registration['joined'])
                    voting.add_value('no_vote', unicode(joined - votes))
                    voting.add_value('registration', registration)

                registration = None

                yield voting.load_item()

    def _parse_question_speakers(self, response, hxs, item, position):
        for speaker in hxs.select('b[position()>%d]' % position):
            dspeaker = Loader(self, response, QuestionDocumentSpeaker(),
                              speaker, required=('name',))
            dspeaker.add_xpath('name', 'text()')
            speaker_details = (speaker.select('following::text()').
                                       extract()[0])
            if (speaker_details and speaker_details.startswith(', ') and
                len(speaker_details) > 4):

                # This is a workaround for situations, where some names has
                # comma. This whay commas are replaced with urlquotes, then all
                # string is splitted by commans and resulting list is unquoted
                # back.
                speaker_details = speaker_details.replace(
                        u'Švietimo, mokslo', u'Švietimo%2c mokslo')

                speaker_details = map(lambda x: urllib.unquote(x.strip()),
                                      speaker_details.split(','))
                speaker_details = filter(None, speaker_details)

                dspeaker.reset_required('name', 'position',)

                inc = Increment(-1)
                dspeaker.add_value('position', speaker_details[inc()])
                if len(speaker_details) == 3:
                    dspeaker.add_value('committee', speaker_details[inc()])
                if len(speaker_details) > 1:
                    dspeaker.add_value('institution', speaker_details[inc()])
            item.add_value('speakers', dict(dspeaker.load_item()))

    def _get_question_documents(self, response, hxs):
        qdoc = Loader(self, response, QuestionDocument(), hxs, required=(
            'id', 'name', 'type', 'number',))
        d_id = hxs.select('b[2]/a[1]/@href').re(r'p_id=(-?\d+)')[0]
        qdoc.add_value('id', u'%sd' % d_id)
        qdoc.add_xpath('name', 'b[1]/text()')
        qdoc.add_value('type',
                hxs.select('b[1]/following::text()[1]').re('^; (.+)'))
        number_re = (r'[A-Z]{1,4}'
                     r'-'
                     r'\d+'
                     r'(([a-zA-Z0-9]{1,2})?(\([^)]{1,4}\))?)*')
        qdoc.add_value('number',
                hxs.select('b[1]//text()').re(
                    r'\(Nr. (%s)\)' % number_re)[0])

        self._parse_question_speakers(response, hxs, qdoc, position=2)

        return qdoc.load_item()

    def _parse_question_documents(self, response, hxs, question):
        many_docs = hxs.select('ol/li')
        if many_docs:
            for d in many_docs:
                question.add_value('documents',
                        dict(self._get_question_documents(response, d)))

        else:
            has_docs = hxs.select('b[2]/a[1]/@href').re(r'p_id=(-?\d+)')
            if has_docs:
                question.add_value('documents',
                        dict(self._get_question_documents(response, hxs)))
            else:
                question.reset_required('_id', 'name', 'session',
                                        'source',)
                question.add_xpath('name', 'b[1]//text()')
                self._parse_question_speakers(response, hxs, question,
                                              position=1)

    def parse_question(self, response):
        xpath = '/html/body/div/table/tr[3]/td/table/tr/td'
        hxs = HtmlXPathSelector(response).select(xpath)[0]

        source = self._get_source(response.url, 'p_svarst_kl_stad_id')
        _id = source['id']

        question = Loader(self, response, Question(), hxs, required=(
            '_id', 'session', 'documents', 'source',))
        question.add_value('_id', '%sq' % _id)

        self._parse_question_documents(response, hxs, question)

        question.add_value('session', self._get_session(response, hxs))
        question.add_value('source', source)

        yield question.load_item()

        agenda_hxs = hxs.select('table[@class="basic"]/tr')
        agenda = self._parse_question_agenda(response, agenda_hxs,
                                             question.item) or []
        for item in agenda:
            yield item

    def _get_vote_value(self, hxs):
        if hxs.select('td[3][contains(.,"+")]'):
            return u'aye'
        elif hxs.select('td[4][contains(.,"+")]'):
            return u'no'
        elif hxs.select('td[5][contains(.,"+")]'):
            return u'abstain'
        else:
            return u'no-vote'

    def _add_voting_legal_act_number(self, hxs, voting):
        number_re = (r'[A-Z]{1,4}'
                     r'-'
                     r'\d+'
                     r'(([a-zA-Z0-9]{1,2})?(\([^)]{1,4}\))?)*')
        voting.add_value('documents',
                hxs.select('b[1]//text()').re(
                    r'\(Nr. (%s)\)' % number_re)[0])

    def _parse_voting_legal_acts(self, response, voting):
        xpath = '/html/body/div/table/tr[3]/td/table/tr/td/align'
        hxs = HtmlXPathSelector(response).select(xpath)[0]

        many_docs = hxs.select('ol/li')
        if many_docs:
            for d in many_docs:
                self._add_voting_legal_act_number(d, voting)

        else:
            has_docs = hxs.select('b[2]/a[1]/@href').re(r'p_id=(-?\d+)')
            if has_docs:
                self._add_voting_legal_act_number(hxs, voting)

    def get_question_url(self, response):
        xpath = '/html/body/div/table/tr[3]/td/table/tr/td/align'
        hxs = HtmlXPathSelector(response).select(xpath)[0]
        urls = hxs.select('b/a/@href') or hxs.select('ol/li/b/a/@href')
        absolute_urls = []
        for url in urls:
            url = url.extract()
            url = absolute_url([url], {'response': response})
            absolute_urls.append(url)
        return absolute_urls

    def parse_person_votes(self, response):
        xpath = ('/html/body/div/table/tr[3]/td/table/tr/td/align/'
                 'div[contains(h4,"rezultatai")]/table')
        hxs = HtmlXPathSelector(response).select(xpath)[0]

        source = self._get_source(response.url, 'p_bals_id')
        _id = source['id']

        voting = Loader(self, response, Voting(), hxs, required=(
            '_id', 'votes',))
        voting.add_value('_id', '%sv' % _id)

        self._parse_voting_legal_acts(response, voting)

        for person in hxs.select('tr'):
            if person.select('th'):
                continue # Skip header

            p_vote = Loader(self, response, PersonVote(), person, required=(
                'person', 'fraction', 'vote',))

            p_id = person.select('td[1]/a/@href').re(r'p_asm_id=(-?\d+)')[0]

            p_vote.add_value('person', '%sp' % p_id)
            p_vote.add_xpath('name', 'td[1]/a/text()')
            p_vote.add_xpath('fraction', 'td[2]/text()')
            p_vote.add_value('vote', self._get_vote_value(person))

            voting.add_value('votes', dict(p_vote.load_item()))

        yield voting.load_item()
