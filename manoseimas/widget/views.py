from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from manoseimas.mps_v2.models import Group, ParliamentMember
from manoseimas.scrapy.services import get_voting_by_source_id, get_voting_by_lrslt_url, get_recent_votings
from manoseimas.scrapy.models import Voting

from manoseimas.decorators import ajax_request

from social.apps.django_app.views import auth

import logging
logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def index(request):

    voting = None
    if 'voting_id' in request.GET:
        voting = get_object_or_404(Voting, key=request.GET.get('voting_id'))
    elif 'source_id' in request.GET:
        voting = get_voting_by_source_id(request.GET.get('source_id'))
    elif 'source_url' in request.GET:
        voting = get_voting_by_lrslt_url(request.GET.get('source_url'))
    else:
        return HttpResponseBadRequest("One of voting_id, source_id or source_url are required.")

    if request.user.is_anonymous():
        profile_id = None
    else:
        profile_id = request.user.pk

    if settings.DEBUG and 'dev' in request.GET:
        template = 'widget/index-dev.html'
    else:
        template = 'widget/index.html'

    return render(request, template, {"profile_id": profile_id, "voting_id": voting.key})


@ajax_request('GET')
def voting_data(request, slug):
    voting = get_object_or_404(Voting, key=slug)

    _voting = dict(voting.value)
    _voting['title'] = voting.get_title()
    if 'registered_for_voting' in voting.value:
        _voting['registered_for_voting'] = voting.value['registration']['joined']
    else:
        _voting['registered_for_voting'] = None

    mps = []
    fractions = []
    mpfraction = {}
    _voting['votes'] = {'aye': [], 'abstain': [], 'no': [], 'no-vote': []}
    for v in voting.value.get('votes', []):
        mps.append(v['person'])
        fractions.append(v['fraction'])
        mpfraction[v['person']] = v['fraction']
        _voting['votes'][v['vote']].append([v['person'], v['fraction']])

    if fractions:
        fractions = {fraction.abbr: {
            '_id': fraction.abbr,
            'slug': fraction.slug,
            'title': fraction.name,
            'image': fraction.logo.url if fraction.logo else None,
            'abbreviation': fraction.abbr,
            'source': None,
        } for fraction in Group.objects.filter(type=Group.TYPE_FRACTION, abbr__in=fractions)}
    else:
        fractions = {}

    if mps:
        mps = {mp.source_id: {
            'first_name': mp.first_name,
            'last_name': mp.last_name,
            'title': mp.first_name + ' ' + mp.last_name,
            'image': mp.photo.url if mp.photo else None,
            'source': {
                'id': mp.source_id,
                'url': mp.candidate_page,
                'name': 'lrslt',
            },
            'fraction': mpfraction[mp.source_id],
            'slug': mp.slug,
            '_id': mp.source_id,
        } for mp in ParliamentMember.objects.filter(source_id__in=mps)}
    else:
        mps = {}

    # Remove votings if MP, that voted is not known. This can happen if scraping of mps and votings went out of sync. In
    # this case just remove votings that does not have associated MPs, making widget work, but with less data.
    for vote, votes in _voting['votes'].items():
        _voting['votes'][vote] = [v for v in votes if v[0] in mps]

    return {
        'fractions': fractions,
        'voting': _voting,
        'mps': mps,
    }


@ajax_request('GET')
def profile_data(request):
    # XXX: https://github.com/ManoSeimas/manoseimas.lt/issues/178
    return {}


# Unfortunately, problems with django_social_auth prevent us from passing additional parameters
# to OAuth to specify the view mode. This content hack injects the parameters as they are being
# posted to Google OAuth.
# We need auth in a popup because we're providing login capability directly from the Widget,
# which is embedded in a 3rd party site.
def google_openid_mode_hack(request):
    response = auth(request, 'google')
    response.content = response.content.replace("</form>", "<input type='hidden' name='openid.ui.mode' value='popup'/><input type='hidden' name='openid.ns.ui' value='http://specs.openid.net/extensions/ui/1.0'/></form>")
    return response


def auth_finish(request):
    if request.user.is_anonymous():
        profile_id = None
    else:
        profile_id = request.user.get_profile().node._id

    response = """

    <script>
        window.opener.MSWidget.connected("%s");
        window.close();
    </script>
    """ % profile_id

    return HttpResponse(response)


def builder(request):
    recent = []
    for v in get_recent_votings(25):
        details = "\n".join([d['name'] for d in v.documents])
        title = v.documents[0]['name'] if v.documents else v.title
        if len(title) > 50:
            title = title[:47] + "..."

        recent.append({
            'value': v._id,
            'text': v.created.strftime("%d/%m/%Y %H:%M") + ": " + title,
            'details': details
        })

    params = {
        'recent_votings': recent,
        'dev': settings.DEBUG and 'dev' in request.GET
    }
    return render(request, 'widget/builder.html', params)
