function(doc) {
    if (doc.type == 'įstatymas') {
        emit(doc.name, null);
    }
}
