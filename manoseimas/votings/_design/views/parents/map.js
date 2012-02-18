function (doc) {
    if (doc.doc_type == 'Voting') {
        if (doc.legal_acts) {
            for (var i=0; i<doc.legal_acts.length; i++) {
                emit([doc.legal_acts[i], doc.created], null);
            }
        }
        if (doc.parent_legal_acts) {
            for (var i=0; i<doc.parent_legal_acts.length; i++) {
                emit([doc.parent_legal_acts[i], doc.created], null);
            }
        }
    }
}
