function (doc) {
    if (doc.doc_type == "Fraction" && doc.abbreviation) {
        emit(doc.abbreviation, null);
    }
}
