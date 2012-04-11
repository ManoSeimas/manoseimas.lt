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

from django.conf.urls.defaults import *

LEGISLATION_ID = r'(?P<legislation_id>[A-Za-z0-9\(\)-]+)'

urlpatterns = patterns('manoseimas.legislation.views',
    url(r'^$', 'category_list', name='manoseimas-category-list'),
    url(r'^visi-istatymai/$', 'legislation_list',
        name='manoseimas-legislation-list'),
    url(r'^paieska/$', 'document_search',
        name='manoseimas-legislation-document-search'),
    url(r'^%s/$' % LEGISLATION_ID, 'legislation',
        name='manoseimas-legislation'),
    url(r'^%s/pataisos/$' % LEGISLATION_ID, 'legislation_amendments',
        name='manoseimas-legislation-amendments'),
    url(r'^%s/projektai/$' % LEGISLATION_ID, 'legislation_drafts',
        name='manoseimas-legislation-drafts'),
    url(r'^%s/balsavimai/$' % LEGISLATION_ID, 'legislation_votings',
        name='manoseimas-legislation-votings'),
    url(r'^projektai/$', 'legislation_all_drafts',
        name='manoseimas-legislation-all-drafts'),
)
