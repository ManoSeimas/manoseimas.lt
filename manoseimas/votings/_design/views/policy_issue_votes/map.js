function(doc) {
    if (doc.policy_issue && doc.parent) {
        emit([doc.policy_issue, doc.parent], {_id: doc.parent});
    }
}
