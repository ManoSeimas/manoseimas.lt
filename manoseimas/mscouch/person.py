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

from couchdb import mapping


class Person(mapping.Document):
    name = mapping.TextField()
    email = mapping.TextField()
    phone = mapping.TextField()
    home_page = mapping.TextField()
    constituency = mapping.TextField()
    party_candidate = mapping.TextField()
    source = mapping.DictField(mapping.Mapping.build(
        id = mapping.TextField(),
        url = mapping.TextField(),
        name = mapping.TextField()
    ))

    by_name = mapping.ViewField('person', '''
        function(doc) {
            if (doc.doc_type == 'person') {
                emit(doc.name, null);
            }
        }''', include_docs=True)
