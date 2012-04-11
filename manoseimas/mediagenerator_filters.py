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

"""django-mediagenerator filters."""

import posixpath

from django.conf import settings

from mediagenerator.filters import cssurl
from mediagenerator.generators.bundles.base import Filter


class URLRewriter(cssurl.URLRewriter):
    def fixurls(self, match):
        url = match.group(1)
        if '://' not in url and not url.startswith('/'):
            url = posixpath.join(self.base_path, url)
            url = posixpath.normpath(url)
        return 'url(%s)' % url


class CSSURL(cssurl.CSSURL):
    """Rewrites all url()'s in css file to point to settings.STATIC_URL.

    This filter helps, if you only want to use django-mediagenerator for css
    and javascript files but not for images and other similar media files.
    """

    def get_dev_output(self, name, variation):
        basepath = self._get_basepath(name)
        rewriter = URLRewriter(basepath)
        content = Filter.get_dev_output(self, name, variation)
        return rewriter.rewrite_urls(content)

    def _get_input_path(self, name, input):
        index, child = name.split('/', 1)
        index = int(index)
        _input = input[index]
        if isinstance(_input, dict):
            return self._get_input_path(child, _input['input'])
        else:
            return _input

    def _get_abspath(self, name):
        path = posixpath.dirname(name)
        path = posixpath.join(settings.STATIC_URL, path)
        return posixpath.normpath(path)

    def _get_basepath(self, name):
        name = self._get_input_path(name, self.input)
        return self._get_abspath(name)
