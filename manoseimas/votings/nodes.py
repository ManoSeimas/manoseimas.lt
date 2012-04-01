# coding: utf-8

from  unidecode import unidecode

from zope.component import adapts
from zope.component import provideAdapter

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render


from sboard.categories.interfaces import ICategory
from sboard.factory import getNodeFactory
from sboard.interfaces import INode
from sboard.models import couch
from sboard.nodes import CreateView
from sboard.nodes import DetailsView
from sboard.nodes import ListView
from sboard.nodes import NodeView
from sboard.nodes import TagListView

from .forms import LinkIssueForm
from .forms import PolicyIssueForm
from .interfaces import IPolicyIssue
from .interfaces import IVoting


class VotingView(DetailsView):
    adapts(IVoting)

    form = LinkIssueForm

    templates = {
        'details': 'votings/voting_details.html',
    }

    def render(self, overrides=None):
        return super(VotingView, self).render({
            'link_issue_form': LinkIssueForm(),
        })

provideAdapter(VotingView)


class CreatePolicyIssueView(CreateView):
    adapts(object, IPolicyIssue)

    form = PolicyIssueForm

provideAdapter(CreatePolicyIssueView, name="create")

provideAdapter(TagListView, (IPolicyIssue,))


class CreatePolicyIssueLinkView(VotingView):
    adapts(IVoting)

    def render(self):
        if self.request.method == 'POST':
            factory = getNodeFactory('policyissuelink')
            if not self.can('create', factory):
                return render(self.request, '403.html', status=403)

            form = self.get_form(self.request.POST)
            if form.is_valid():
                form.cleaned_data['parent'] = self.node
                child = self.form_save(form, create=True)
                if self.node:
                    return redirect(self.node.permalink())
                else:
                    return redirect(child.permalink())
        else:
            form = self.get_form()

        return super(CreatePolicyIssueLinkView, self).render({
            'link_issue_form': form,
        })

provideAdapter(CreatePolicyIssueLinkView, name="link-policy-issue")


class QuestionGroupView(ListView):
    adapts(ICategory)

    templates = {
        'list': 'votings/question_group.html',
    }

provideAdapter(QuestionGroupView)


def get_vote_value(vote, link):
    return ({
        'aye': link['aye'],
        'abstain': link['abstain'],
        'no-vote': link['no'],
        'no': link['no'],
    })[vote]


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

def mps_vote_for_issue(policy_issue_id):
    mps = {}
    links = {}
    view = couch.view('votings/by_policy_issue', key=policy_issue_id)
    for link in view:
        links[link.parent] = {
            'aye': link.vote_aye,
            'abstain': link.vote_abstain,
            'no': link.vote_no,
        }

    view = couch.view('votings/policy_issue_votes',
                      startkey=[policy_issue_id], endkey=[policy_issue_id, {}])
    # Loop for all votings
    for voting in view:
        link = links[voting._id]
        # Loop for MPs
        # [{name: Jonas Petraitis, vote: aye}, ...]
        for vote in voting.votes:
            if vote['name'] not in mps:
                mps[vote['name']] = {'times': 0, 'sum': 0}

            mps[vote['name']]['times'] += 1
            mp_vote = get_vote_value(vote['vote'], link)
            mps[vote['name']]['sum'] += mp_vote

    return dict([(name, mp['sum'] / mp['times']) for name, mp in mps.items()])


def match_mps_with_user(results, mps, user_vote):
    for name, mp_issue_vote in mps.items():
        if name not in results:
            results[name] = {'times': 0, 'sum': 0}
        results[name]['times'] += 1
        # If issues will be weighted then then multiply with issue weight
        results[name]['sum'] += user_vote * mp_issue_vote

def sort_results(mps):
    return sorted(list([{
        'name': k,
        'times': v['times'],
        'score': (1.0 * v['sum'] / v['times']) / 4 * 100,
    } for k, v in mps.items()]), key=lambda a: a['score'], reverse=True)

class QuickResultsView(NodeView):
    adapts(INode)

    def render(self):
        if self.request.GET.get('clean'):
            self.request.session['questions'] = []
            self.request.session['mps_matches'] = {}

        # XXX: implement
        user_vote = 1
        questions = self.request.session.get('questions', [])
        mps_matches = self.request.session.get('mps_matches', {})

        if self.node._id not in questions:
            # Save questions
            questions.append(self.node._id)
            self.request.session['questions'] = questions

            # Save mps
            mps_votes = mps_vote_for_issue(self.node._id)
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
            return HttpResponse(json.dumps({'mps': [{
                'name': a['name'],
                'score': a['score'],
                'url': get_img_url(a['name']),
                } for a in results[:8]]
            }))

provideAdapter(QuickResultsView, name='quick-results')


class QuickResultsView(DetailsView):
    adapts(INode)

    templates = {
        'details': 'votings/results.html',
    }

    def render(self):
        return super(QuickResultsView, self).render({
            'results': [
                {'name': u'Eligijus Masiulis',
                 'score': 86,
                 'url': 'http://www3.lrs.lt/home/seimo_nariu_nuotraukos/2008/eligijus_masiulis.jpg',
                },
                {'name': u'Irena Degutienė',
                 'score': 85,
                 'url': 'http://www3.lrs.lt/home/seimo_nariu_nuotraukos/2008/irena_degutiene.jpg',
                },
                {'name': u'Vytautas Gapšys',
                 'score': 79,
                 'url': 'http://www3.lrs.lt/home/seimo_nariu_nuotraukos/2008/vytautas_gapsys.jpg',
                },
                {'name': u'Algirdas Sysas',
                 'score': 76,
                 'url': 'http://www3.lrs.lt/home/seimo_nariu_nuotraukos/2008/algirdas_sysas.jpg',
                },
                {'name': u'Remigijus Žemaitaitis',
                 'score': 69,
                 'url': 'http://www3.lrs.lt/home/seimo_nariu_nuotraukos/2008/remigijus_zemaitaitis.jpg',
                }
            ],
            'party_results': [
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
            ],
        })

provideAdapter(QuickResultsView, name='results')
