function(doc) {
    if (doc.is_legal_act && doc.number) {
        emit(doc.number, null);
    }
}
