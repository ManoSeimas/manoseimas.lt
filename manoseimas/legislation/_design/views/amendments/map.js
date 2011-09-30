function(doc) {
    if (doc.relations.amends && doc.date) {
        for (var i=0; i<doc.relations.amends.length; i++) {
            emit([doc.relations.amends[i], doc.date], null);
        }
    }
}
