function (doc) {
    if (doc.doc_type == 'voting' && doc.documents) {
        emit(doc._id, null);
    }
}
