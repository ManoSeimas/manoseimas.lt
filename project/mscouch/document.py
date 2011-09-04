from couchdb import mapping


class Document(mapping.Document):
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
