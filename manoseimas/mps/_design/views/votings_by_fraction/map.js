function (doc) {
    if (doc.doc_type == "Voting" && doc.votes) {
        var fractions = [];
        var vote_types = ["abstain", "aye", "no"];
        for (var i=0; i<vote_types.length; i++) {
            if (vote_types[i] in doc.votes) {
                var votes = doc.votes[vote_types[i]];
                for (var j=0; j<votes.length; j++) {
                    var fraction = votes[j][1];
                    if (fractions.indexOf(fraction) == -1) {
                        fractions.push(fraction);
                        emit(fraction, null);
                    }
                }
            }
        }
    }
}
