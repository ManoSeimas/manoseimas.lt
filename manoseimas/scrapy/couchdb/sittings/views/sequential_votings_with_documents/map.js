function (doc) {
    if (doc.doc_type == 'voting' && doc.documents) {
        emit(parseInt(doc._id), null);
    }
}
