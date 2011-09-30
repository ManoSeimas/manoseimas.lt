function (doc) {
    if (doc.doc_type == 'voting') {
        emit(doc._id, null);
    }
}
