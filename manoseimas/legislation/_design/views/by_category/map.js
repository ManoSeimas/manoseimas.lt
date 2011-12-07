function(doc) {
    if (doc.type == 'įstatymas' && doc.category) {
        emit([doc.category, doc.name], null);
    }
}
