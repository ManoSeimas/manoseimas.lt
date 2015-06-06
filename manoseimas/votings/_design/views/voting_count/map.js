function (doc) {
    if (doc.source.voting.id) {
        emit(doc.created, 1);
    }
}
