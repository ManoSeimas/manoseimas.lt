function (doc) {
    var key = [];
    if (doc.parents) {
        for (var i=0; i<doc.parents.length; i++) {
            key.push(doc.parents[i]);
        }
    }
    key.push(doc._id);
    emit(key, null);
}
