function(doc) {
    if (doc.language == 'lt' && !doc.relations && doc.number &&
        (doc.type == 'įstatymas' || doc.type == 'konstitucija')) {
        emit(doc.name, null);
    }
}
