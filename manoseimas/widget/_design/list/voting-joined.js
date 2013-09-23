function(head, req) {
    if (req.query.include_docs !== 'true') {
        start({ code: 400,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return send(JSON.stringify({ error: 'include_docs=true is required.' }));
    }

    var mps = {};
    var fractions = {};
    var voting = null;
    var filter = function(o, keys) {
        return new ((function() {
            return function () {
                for (var i=0; i<keys.length; i++) {
                    var k = keys[i];
                    this[k] = o[k];
                }
            }
        })());
    };

    var filter_mp = function(o) {
        return filter(o, ['_id', 'fraction', 'first_name', 'last_name', 'image', 'slug', 'source', 'title']);
    };
    var filter_fraction = function(o) {
        return filter(o, ['_id', 'abbreviation', 'image', 'slug', 'source', 'title']);
    };
    var row;
    while (row = getRow()) {
        var voteid = row.key[0];
        var doctype = row.key[1];
        var vote = row.key[2];
        switch (doctype) {
            case 'Voting':
                voting = row.doc;
                break;
            case 'Fraction':
                if (fractions[row.doc._id] == null) {
                    fractions[row.doc._id] = filter_fraction(row.doc);
                }
                break;
            case 'MPProfile':
                if (mps[row.doc._id] == null) {
                    mps[row.doc._id] = filter_mp(row.doc);
                }
                break;
        }
    }
    if (voting == null) {
        start({ code: 404, headers: {
            'Content-Type': 'application/json'
        }
        });
        return send(JSON.stringify({
            error: 'Voting not found.'
        }));
    }
    result = {
        voting: {
            _id: voting._id,
            title: voting.title,
            source: voting.source,
            documents: voting.documents,
            registered_for_voting: voting.registered_for_voting,
            total_votes: voting.total_votes,
            vote_aye: voting.vote_aye,
            vote_no: voting.vote_no,
            vote_abstain: voting.vote_abstain,
            votes: voting.votes
        },
        mps: mps,
        fractions: fractions
    };
    start({ headers: {
        'Content-Type': 'application/json'
        }
    });
    return send(JSON.stringify(result));
}
