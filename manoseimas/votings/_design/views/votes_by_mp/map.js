function(doc) {
    if (doc.doc_type == 'Voting' && doc.votes) {
        for(var i = 0; i < doc.votes.aye.length; i++) {
            emit(doc.votes.aye[i][0], {'aye': 1});
        }

        for(var i = 0; i < doc.votes.no.length; i++) {
            emit(doc.votes.no[i][0], {'no': 1});
        }

        for(var i = 0; i < doc.votes.abstain.length; i++) {
            emit(doc.votes.abstain[i][0], {'abstain': 1});
        }
    }
}
