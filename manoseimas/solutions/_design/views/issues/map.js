function(doc) {
    if (doc.doc_type == 'SolutionIssue' && doc.solution && doc.issue) {
        // Solution issue
        emit([doc.solution, doc.solves, doc.likes, doc._id, 2], null);
        // Issue
        emit([doc.solution, doc.solves, doc.likes, doc._id, 1], {_id: doc.issue});
    }
}
