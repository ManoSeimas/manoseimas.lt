(head, req) ->
    if req.query.include_docs != 'true'
        start { code: 400, headers: { 'Content-Type': 'application/json' } }
        return send JSON.stringify { error: 'include_docs=true is required.' }

    mps = {}
    fractions = {}
    voting = null

    # We remap our Fractions and MPs to include the minimal content necessary
    filter = (o, keys) -> new class then constructor: -> @[k] = o[k] for k in keys
    filter_mp = (o) -> filter o, ['_id','fraction','first_name','last_name','image','slug','source','title']
    filter_fraction = (o) -> filter o, ['_id','abbreviation','image','slug','source','title']
 
    while row = getRow()
        [voteid, doctype, vote] = row.key
        switch doctype
            when 'Voting' then voting = row.doc
            when 'Fraction' then fractions[ row.doc._id ] ?= filter_fraction row.doc
            when 'MPProfile' then mps[ row.doc._id ] ?= filter_mp row.doc

    if !voting?
        start { code: 404, headers: { 'Content-Type': 'application/json' } }
        return send JSON.stringify { error: 'Voting not found.' }


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
            votes: voting.votes,
        }
        mps: mps,
        fractions: fractions
    }

    start { headers: { 'Content-Type': 'application/json' } }
    send JSON.stringify result
