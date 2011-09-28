function(doc) {
    if (doc.relations.defines_as_no_longer_valid && doc.date) {
        var not_valid = doc.relations.defines_as_no_longer_valid;
        for (var i=0; i<not_valid.length; i++) {
            emit([not_valid[i], doc.date], null);
        }
    }
}
