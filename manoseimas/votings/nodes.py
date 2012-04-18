# coding: utf-8

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

import urlparse

from  unidecode import unidecode

from zope.component import adapts
from zope.component import provideAdapter

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from sboard.categories.interfaces import ICategory
from sboard.interfaces import INode
from sboard.models import couch
from sboard.nodes import CreateView
from sboard.nodes import DetailsView
from sboard.nodes import ListView
from sboard.nodes import NodeView
from sboard.nodes import TagListView

from .forms import LinkSolutionForm
from .forms import SolutionForm
from .interfaces import ISolution
from .interfaces import IVoting


class VotingView(DetailsView):
    adapts(IVoting)

    form = LinkSolutionForm

    templates = {
        'details': 'votings/voting_details.html',
    }

    def get_related_legal_acts(self):
        return couch.view('legislation/related_legal_acts', key=self.node._id)

    def get_solutions(self):
        return couch.view('votings/solutions_by_voting', key=self.node._id)

    def render(self, **overrides):
        context = {
            'related_legal_acts': self.get_related_legal_acts(),
            'solutions': self.get_solutions(),
        }
        context.update(overrides or {})

        if 'link_solution_form' not in context:
            context['link_solution_form'] = LinkSolutionForm()

        return super(VotingView, self).render(**context)

provideAdapter(VotingView)


class CreateSolutionView(CreateView):
    adapts(object, ISolution)

    form = SolutionForm

provideAdapter(CreateSolutionView, name="create")

provideAdapter(TagListView, (ISolution,))


class LinkSolutionView(VotingView):
    adapts(IVoting)

    def render(self):
        if self.request.method == 'POST':
            if not self.can('update', None):
                return render(self.request, '403.html', status=403)

            form = self.get_form(self.request.POST)
            if form.is_valid():
                if 'solutions' not in self.node:
                    self.node.solutions = {}
                solution = form.cleaned_data.pop('solution')
                self.node.solutions[solution._id] = form.cleaned_data
                self.node.save()
                return redirect(self.node.permalink())
        else:
            form = self.get_form()

        return super(LinkSolutionView, self).render(link_solution_form=form)

provideAdapter(LinkSolutionView, name="link-solution")


class QuestionGroupView(ListView):
    adapts(ICategory)

    templates = {
        'list': 'votings/question_group.html',
    }

provideAdapter(QuestionGroupView)


def get_vote_value(vote, position):
    value = ({
        'aye': 2,
        'abstain': -1,
        'no-vote': -1,
        'no': -2,
    })[vote]
    if not position:
        value = value * -1
    return value


def get_img_url(name):
    uname = name.strip()
    names = unidecode(uname).split()  
    names.append( names.pop(0) )  #   swap/rotate order of Name and Surname
    name_surname4photo = "_".join( names).lower()
    link = "http://www3.lrs.lt/home/seimo_nariu_nuotraukos/2008/%s.jpg" % name_surname4photo

    if (len(names) == 3):
        names.append( names.pop(0) )  #  once more: rotate order of Name and Surname
        name_surname4photo = "_".join( names).lower()
        link = "http://www3.lrs.lt/home/seimo_nariu_nuotraukos/2008/%s.jpg" % name_surname4photo
    return link

def mps_vote_for_solution(solution_id):
    mps = {}
    view = couch.view('votings/by_solution', key=solution_id)
    # Loop for all votings
    for voting in view:
        link = voting.solutions[solution_id]
        # Loop for MPs
        # [{name: Jonas Petraitis, vote: aye}, ...]
        for vote in voting.votes:
            if vote['name'] not in mps:
                mps[vote['name']] = {'times': 0, 'sum': 0}

            mps[vote['name']]['times'] += link['weight']
            mp_vote = get_vote_value(vote['vote'], link['position'])
            mps[vote['name']]['sum'] += mp_vote * link['weight']

    return dict([(name, 1.0 * mp['sum'] / mp['times']) for name, mp in mps.items()])

def match_mps_with_user(results, mps, user_vote):
    for name, mp_solution_vote in mps.items():
        if name not in results:
            results[name] = {'times': 0, 'sum': 0}
        results[name]['times'] += 1
        # If solutions will be weighted then then multiply with issue weight
        results[name]['sum'] += user_vote * mp_solution_vote

def sort_results(mps):
    return sorted(list([{
        'name': k,
        'times': v['times'],
        'score': int((1.0 * v['sum'] / v['times']) / 4 * 100),
        'url': get_img_url(k),
    } for k, v in mps.items()]), key=lambda a: a['score'], reverse=True)


class QuickResultsView(NodeView):
    adapts(INode)

    def render(self):
        if self.request.GET.get('clean'):
            self.request.session['questions'] = []
            self.request.session['mps_matches'] = {}

        user_vote = self.request.GET.get('vote')
        if user_vote not in ('-2', '-1', '0', '1', '2'):
            raise Http404
        user_vote = int(user_vote)

        questions = self.request.session.get('questions', [])
        mps_matches = self.request.session.get('mps_matches', {})

        if self.node._id not in questions:
            # Save questions
            questions.append(self.node._id)
            self.request.session['questions'] = questions

            # Save mps
            mps_votes = mps_vote_for_solution(self.node._id)
            match_mps_with_user(mps_matches, mps_votes, user_vote)
            self.request.session['mps_matches'] = mps_matches

        results = sort_results(mps_matches)
        if self.request.GET.get('raw'):
            return HttpResponse(
                '<table>' + ''.join(['''
                    <tr>
                        <td>%(name)s</td>
                        <td>x%(times)s</td>
                        <td>%(score)s%%</td>
                        <td><img src="%(url)s"> %(url)s</td>
                    </tr>''' % {
                        'name': a['name'],
                        'times': a['times'],
                        'score': a['score'],
                        'url': get_img_url(a['name']),
                    } for a in results]) +
                '</table>')
        else:
            import json
            return HttpResponse(json.dumps({'mps': results[:8]}))

provideAdapter(QuickResultsView, name='quick-results')


class QuickResultsView(DetailsView):
    adapts(INode)

    templates = {
        'details': 'votings/results.html',
    }

    def render(self):
        mps_matches = self.request.session.get('mps_matches', {})
        results = sort_results(mps_matches)
        return super(QuickResultsView, self).render(
            results=results[:8],
            party_results=[
                {'name': u'Tėvynės sąjungos-Lietuvos krikščionių demokratų frakcija',
                 'score':  78,
                 'url':    'http://manobalsas.lt/politikai/logos/part_37.gif',
                },
                {'name': u'Lietuvos socialdemokratų partijos frakcija',
                 'score':  72,
                 'url':    'http://manobalsas.lt/politikai/logos/part_20.gif',
                },
                {'name': u'Liberalų ir centro sąjungos frakcija',
                 'score':  67,
                 'url':    'http://manobalsas.lt/politikai/logos/part_3.gif',
                },
                {'name': u'Liberalų sąjūdžio frakcija',
                 'score':  66,
                 'url':    'http://manobalsas.lt/politikai/logos/part_18.gif',
                },
                {'name': u'Frakcija "Tvarka ir teisingumas"',
                 'score':  56,
                 'url':    'http://manobalsas.lt/politikai/logos/part_30.gif',
                },
            ]
        )

provideAdapter(QuickResultsView, name='results')


class SolutionDetailsView(DetailsView):
    adapts(ISolution)

    templates = {
        'details': 'votings/solution.html',
    }

provideAdapter(SolutionDetailsView)


def search_lrs_url(query):
    url = urlparse.urlparse(query)
    qry = urlparse.parse_qs(url.query)
    if url.netloc.endswith('.lrs.lt') and 'p_bals_id' in qry:
        try:
            source_id = int(qry['p_bals_id'][0])
        except ValueError:
            source_id = None
        if source_id:
            node = couch.view('votings/by_source_id', key=source_id).first()
            return redirect(node.permalink())
