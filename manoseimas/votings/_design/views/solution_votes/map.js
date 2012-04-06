function(doc) {
    if (doc.solution && doc.parent) {
        emit([doc.solution, doc.parent], {_id: doc.parent});
    }
}
