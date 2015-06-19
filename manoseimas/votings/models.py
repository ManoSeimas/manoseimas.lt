# Copyright (C) 2012  Mantas Zimnickas <sirexas@gmail.com>
#
# This file is part of manoseimas.lt project.
#
# manoseimas.lt is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# manoseimas.lt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with manoseimas.lt.  If not, see <http://www.gnu.org/licenses/>.

import contextlib
import datetime
import re
import urllib2
import urlparse

from zope.interface import implements

from couchdbkit.ext.django import schema
from scrapy.http import HtmlResponse

from sboard.factory import provideNode
from sboard.models import Node
from sboard.models import couch

from manoseimas.scrapy.pipelines import ManoseimasPipeline
from manoseimas.scrapy.db import get_db
from manoseimas.scrapy.db import set_db_from_settings
from manoseimas.scrapy.spiders.sittings import SittingsSpider

from .interfaces import IVoting


class Source(schema.DocumentSchema):
    id = schema.IntegerProperty()
    url = schema.StringProperty()


class Voting(Node):
    implements(IVoting)

    # Number of people, that has voting right
    has_voting_right = schema.IntegerProperty()

    # Number of people, that registered for this voting session.
    registered_for_voting = schema.IntegerProperty()

    # Total votes received.
    total_votes = schema.IntegerProperty()

    # Voting results.
    vote_abstain = schema.IntegerProperty()
    vote_aye = schema.IntegerProperty()
    vote_no = schema.IntegerProperty()

    # Voting type (regular, urgent, ...)
    voting_type = schema.StringProperty()

    # List of votes by person and fraction.
    votes = schema.DictProperty()

    # List of legal acts that was directly voted for with this voting.
    legal_acts = schema.ListProperty()

    # List of legal acts that was directly voted for with this voting.
    solutions = schema.DictProperty()

    # List of legal acts that are parents of all legal acts voted for.
    parent_legal_acts = schema.ListProperty()

    # Source of information.
    # FIXME: https://github.com/benoitc/couchdbkit/issues/119
    #source = schema.SchemaDictProperty(Source())
    source = schema.DictProperty()

    def did_not_vote(self):
        """Number of people that registered for voting session, but did not
        vote."""
        return self.registered_for_voting - self.total_votes

    def get_vote_value(self, vote):
        return ({
            'aye': 2,
            'abstain': -1,
            'no-vote': -1,
            'no': -2,
        })[vote]

provideNode(Voting, "voting")

def get_full_voting(source_id, include_metrics=True):
    """ 
    Fetches a voting and all of its referenced Fractions and MPs, using an 
    optimized query. Also calculates metrics for the voting.
    """

    fractions = {}
    mps = {}
    voting = None
    nodes = couch.view("widget/voting-objects",  startkey=[source_id], endkey=[source_id, u'\ufff0'])
    for n in nodes:
        if n.doc_type == 'Fraction':
            n.votes = {'aye':0, 'no':0, 'abstain': 0}
            n.voting_score = 0
            n.total_votes = 0
            fractions[n._id] = n
        elif n.doc_type == "MPProfile":
            mps[n._id] = n
        elif n.doc_type == "Voting":
            voting = n

    for vote_type,vote_list in voting.votes.iteritems():
        for i,v in enumerate(vote_list):
            mp = mps[ v[0] ]
            if v[1] != None:
                fraction = fractions[ v[1] ]
            else:
                # Some votings contain votes that occurred during an MPs transition between fractions.
                # This produces NULL fraction data for the MP's vote at that time. We assign a blank Fraction
                # for these votings.
                fraction = None
            vote_list[i] = mp

            mp.fraction = fraction
            mp.vote = vote_type

            if include_metrics and fraction != None:
                fraction.votes[vote_type] += 1
                fraction.voting_score += voting.get_vote_value(vote_type)
                fraction.total_votes += 1
    
    if (include_metrics):
        for fraction in fractions.values():
            fraction.viso = int( 100 * fraction.voting_score / (2*fraction.total_votes) )
            fraction.supports = fraction.viso >= 0
            # FIXME: Acquire no-vote values to calculate participation!
            #fraction['participation'] = int( 100 * fraction['registered_for_voting'] / fraction['total_votes'] )
            fraction.participation = 100;

    voting.fractions = fractions.values()
    voting.mps = mps.values()

    return voting

def get_voting_source_id_from_lrstl_url(url):
    url = urlparse.urlparse(url)
    qry = urlparse.parse_qs(url.query)
    if url.netloc.endswith('.lrs.lt') and 'p_bals_id' in qry:
        try:
            return int(qry['p_bals_id'][0])
        except ValueError:
            return None
    return None

def get_recent_votings(limit=5):
    return couch.view('votings/by_source_id', limit=limit)


def get_voting_by_source_id(source_id):
    return couch.view('votings/by_source_id', key=source_id).first()


def get_voting_by_lrslt_url(url):
    source_id = get_voting_source_id_from_lrstl_url(url)
    if source_id:
        return get_voting_by_source_id(source_id)
    else:
        return None


def fetch_lrslt_url(url):
    with contextlib.closing(urllib2.urlopen(url)) as f:
        return f.read()


def fetch_voting_by_lrslt_url(url):
    # Avoiding circular imports
    from manoseimas.scrapy.settings import COUCHDB_DATABASES
    import manoseimas.legislation.management. \
           commands.syncsittings as syncsittings

    # Parse voting
    body = fetch_lrslt_url(url)
    if not body:
        return None
    response = HtmlResponse(url, body=body)
    spider = SittingsSpider()
    items = list(spider.parse_person_votes(response))

    # Parse question
    question_url = spider.get_question_url(response)[0]
    body = fetch_lrslt_url(question_url)
    if not body:
        return None
    response = HtmlResponse(question_url, body=body)
    items.extend(list(spider.parse_question(response)))

    # Store
    set_db_from_settings(COUCHDB_DATABASES, 'voting')
    keys = []
    pipeline = ManoseimasPipeline()
    for item in items:
        pipeline.process_item(item, spider)
        keys.append(item['_id'])

    # Process
    syncsittings.RawVoting.set_db(get_db('voting'))
    processor = syncsittings.SyncProcessor()
    params = {
        'keys': keys,
        'include_docs': True,
        'classes': {'voting': syncsittings.RawVoting},
    }
    rows = syncsittings.RawVoting.view('scrapy/votes_with_documents', **params)
    processor.sync(rows)

    # Return
    return get_voting_by_lrslt_url(url)


def get_mp_votes_by_internal_id(mp_node_id, start_date, end_date):
    return couch.view('votings/votes_by_mp', startkey=[mp_node_id, start_date],
                      endkey=[mp_node_id, end_date],
                      reduce=True, group=False,
                      include_docs=False).first()


# 2012-11-16 - start of 2012-2016 parliament term
def get_mp_votes(source_id, start_date='2012-11-16', end_date=None):
    if end_date is None:
        end_date = datetime.date.today().isoformat()
    source_id = re.match(r'^\d+', source_id).group(0)
    node = couch.view('mps/by_source_id', key=source_id).first()
    node_id = node._id
    votes_node = get_mp_votes_by_internal_id(node_id, start_date, end_date)
    if votes_node:
        return votes_node['value']


def get_total_votes(start_date='2012-11-16', end_date=None):
    if end_date is None:
        end_date = datetime.date.today().isoformat()
    result = couch.view('votings/voting_count', reduce=True, group=False,
                        include_docs=False, startkey=start_date,
                        endkey=end_date).one()

    return result['value'] if result else 0
