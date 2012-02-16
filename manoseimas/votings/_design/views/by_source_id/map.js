function (doc) {
    if (doc.source.voting.id) {
        emit(doc.source.voting.id, null);
    }
}
