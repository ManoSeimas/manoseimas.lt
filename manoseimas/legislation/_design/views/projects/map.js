function(doc) {
    if (doc.doc_type == "LawProject" && doc.parents) {
        for (var i=0; i<doc.parents.length; i++) {
            emit([doc.parents[i], doc.created], null);
        }
    }
}
