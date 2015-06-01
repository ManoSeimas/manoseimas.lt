function(doc) {
    if (doc.doc_type == "Voting") {
        emit(doc.created.split("T")[0], null);
    }
}
