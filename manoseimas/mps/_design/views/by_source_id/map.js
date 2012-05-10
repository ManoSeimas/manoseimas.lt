function (doc) {
    if (doc.source.id) {
        emit(doc.source.id, null);
    }
}
