function(doc) {
    if (doc.type == 'įstatymas') {
        emit(doc._id, null);
    }
}
