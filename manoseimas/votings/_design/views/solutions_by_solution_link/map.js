function(doc) {
    if (doc.solution) {
        emit(doc.solution, null);
    }
}
