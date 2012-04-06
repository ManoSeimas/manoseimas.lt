function(doc) {
    if (doc.parent && doc.solution) {
        emit(doc.parent, {_id: doc.solution});
    }
}
