function(doc) {
    if (doc.doc_type !== "Voting") {
        return;
    }
    emit([doc._id, doc.doc_type], {  _id: doc._id });

    for (vote in doc.votes) {
        var voters = doc.votes[vote];
        for (var i=0; i<voters.length; i++) {
            var v = voters[i];
            emit([doc._id, "MPProfile", vote], { _id: v[0] });
            emit([doc._id, "Fraction", vote], { _id: v[1] });
        }
    }
}
