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



class Document(mapping.Document):
    # TODO:albertas:2011-09-04: Document should also save data: "Projekta
    # pateike" and "Projekto komitetas".
    name = mapping.TextField()
    type = mapping.TextField()
    number = mapping.TextField()
    date = mapping.DateTimeField()
    language = mapping.TextField()
    source = mapping.DictField(mapping.Mapping.build(
        id = mapping.TextField(),
        url = mapping.TextField(),
        name = mapping.TextField()
    ))

    by_number = mapping.ViewField('document', '''
        function(doc) {
            if (doc.doc_type == 'document') {
                emit(doc.number, null);
            }
        }''', include_docs=True)


    proposed_only = mapping.ViewField('document', '''
        function(doc) {
            if (doc.doc_type == 'document' && doc.proposed) {
                emit(doc.number, null);
            }
        }''', include_docs=True)


    votes = mapping.ViewField('votes', '''
        function(doc) {
            if (doc.doc_type == 'voting' && doc.documents) {
                for (var i=0; i<doc.documents.length; i++){
                    emit([doc.documents[i], doc._id], null);
                }
            } else if (doc.doc_type == 'document') {
               emit([doc._id, 0], null);
            }
        }''', include_docs=True)
