function(doc) {
    if (doc.language == 'lt' && doc.type == 'įstatymo projektas') {
        emit(doc.number, null);
    }
}
