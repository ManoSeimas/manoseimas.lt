function(doc) {
    if (doc.doc_type == 'CounterArgument' && doc.parents && doc.parents.length > 0) {
        emit(doc.parents[doc.parents.length-1], null);
    }
}
