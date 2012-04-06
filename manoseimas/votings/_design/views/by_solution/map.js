function(doc) {
    if (doc.solution && doc.parent) {
        emit(doc.solution, {_id: doc.parent});
    }
}
