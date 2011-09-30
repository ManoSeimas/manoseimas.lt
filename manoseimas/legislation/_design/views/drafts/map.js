function(doc) {
    if (doc.date) {
        if (doc.relations.adopts) {
            for (var i=0; i<doc.relations.adopts.length; i++) {
                emit([doc.relations.adopts[i], doc.date], null);
            }
        }
        if (doc.relations.law) {
            for (var i=0; i<doc.relations.law.length; i++) {
                emit([doc.relations.law[i], doc.date], null);
            }
        }
    }
}
