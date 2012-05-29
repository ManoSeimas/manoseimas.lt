function(doc) {
    if (doc.doc_type == 'SolutionIssue' && doc.solution && doc.issue) {
        // Solution issue
        emit([doc.issue, doc.solves, doc.likes, doc._id, 2], null);
        // Solution
        emit([doc.issue, doc.solves, doc.likes, doc._id, 1], {_id: doc.solution});
    }
}
