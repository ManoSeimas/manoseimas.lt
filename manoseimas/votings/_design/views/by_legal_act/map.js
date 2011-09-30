function (doc) {
    if (doc.doc_type == 'voting' && doc.documents) {
        for (var i=0; i<doc.documents.length; i++) {
            emit(doc.documents[i], null);
        }
    }
}
