function(doc) {
    if (doc.adopted_documents && doc.date) {
        for (var i=0; i<doc.adopted_documents.length; i++) {
            emit([doc.adopted_documents[i], doc.date], null);
        }
    }
}
