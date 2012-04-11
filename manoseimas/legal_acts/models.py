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

from couchdbkit.exceptions import ResourceNotFound
from couchdbkit.ext.django import schema


class LegalAct(schema.Document):
    name = schema.StringProperty()

    @classmethod
    def search(cls, params, limit=25, **kw):
        starts = params['query']
        ends = starts + 'Z'
        return cls.view('_all_docs', limit=limit, **kw)[starts:ends]

    def current_version(self):
        try:
            return self.fetch_attachment('current_version.html')
        except ResourceNotFound:
            return self.original_version()

    def original_version(self):
        try:
            return self.fetch_attachment('original_version.html')
        except ResourceNotFound:
            return u''
