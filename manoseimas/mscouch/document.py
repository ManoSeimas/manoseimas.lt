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
