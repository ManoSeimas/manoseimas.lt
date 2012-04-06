function(doc) {
    if (doc.doc_type == 'Voting' && doc.solutions) {
        for (var solution in doc.solutions) {
            emit(doc._id, {_id: solution});
        }
    }
}
