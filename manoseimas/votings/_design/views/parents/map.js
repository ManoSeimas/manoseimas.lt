function (doc) {
    if (doc.doc_type == 'voting' && doc.parents) {
        for (var i=0; i<doc.parents.length; i++) {
            emit([doc.parents[i], doc.datetime], null);
        }
    }
}
