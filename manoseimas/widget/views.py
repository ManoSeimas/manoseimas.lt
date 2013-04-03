from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from sboard.models import Node
from sboard.models import get_node_by_slug
from sboard.models import get_image_node_thumbnail

from manoseimas.votings.models import get_voting_by_source_id, get_voting_by_lrslt_url

from decorators import ajax_request

from social_auth.views import auth

import logging
logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def index(request):

    voting = None
    if 'voting_id' in request.GET:
        voting = get_node_by_slug( request.GET.get('voting_id') )
    elif 'source_id' in request.GET:
        voting = get_voting_by_source_id( request.GET.get('source_id') )
    elif 'source_url' in request.GET:
        voting = get_voting_by_lrslt_url( request.GET.get('source_url') )
    else:
        return HttpResponseBadRequest("One of voting_id, source_id or source_url are required.")
    
    if not voting or voting.doc_type != 'Voting':
        raise Http404("Voting Not Found.") 

    if request.user.is_anonymous():
        profile_id = None
    else:
        profile_id = request.user.get_profile().node._id

    if settings.DEBUG and 'dev' in request.GET:
        template = 'widget/index-dev.html'
    else:
        template = 'widget/index.html'

    return render(request, template, { "profile_id": profile_id, "voting_id": voting._id } )

@ajax_request('GET')
def voting_data(request, slug):
    content = Node.get_db().list("widget/voting-joined", "voting-objects", startkey=[slug], endkey=[slug, u'\ufff0'], include_docs=True)

    if 'error' in content:
        return { 'error': content['error']}
    
    # NOTE: This is still somewhat slow.
    for k in ['fractions','mps']:
        for slug in content[k]:
            image_slug = content[k][slug]['image'] 
            content[k][slug]['image'] = get_image_node_thumbnail(image_slug, geometry='50x50').url
            if not content[k][slug]['image']:
                logger.error("Problem fetching image for slug: "+image_slug)

    return content

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

