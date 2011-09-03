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
