function(doc) {
    if (doc.parent_legal_acts) {
        for (var i=0; i<doc.parent_legal_acts.length; i++) {
            emit(doc._id, {_id: doc.parent_legal_acts[i]});
        }
    }
}
