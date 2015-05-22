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

import json
from functools import wraps

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


class JsonResponse(HttpResponse):
    def __init__(self, data):
        super(JsonResponse, self).__init__(content=json.dumps(data), mimetype='application/json')


def ajax_request(*allowed_methods):
    allowed_methods = allowed_methods or ('POST',)

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method not in allowed_methods:
                return HttpResponseBadRequest()
            response = view_func(request, *args, **kwargs)
            if isinstance(response, HttpResponse):
                return response
            else:
                return JsonResponse(response)
        return wrapper
    return csrf_exempt(decorator)
