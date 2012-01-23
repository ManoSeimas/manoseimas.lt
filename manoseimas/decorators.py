from functools import wraps

from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt


class JsonResponse(HttpResponse):
    def __init__(self, data):
        super(JsonResponse, self).__init__(content=simplejson.dumps(data),
                                           mimetype='application/json')


def ajax_request(*allowed_methods):
    allowed_methods = allowed_methods or ('POST',)
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method not in allowed_methods or not request.is_ajax():
                return HttpResponseBadRequest()
            response = view_func(request, *args, **kwargs)
            if isinstance(response, HttpResponse):
                return response
            else:
                return JsonResponse(response)
        return wrapper
    return csrf_exempt(decorator)
