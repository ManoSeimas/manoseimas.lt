function(doc) {
    if (doc.parent && doc.policy_issue) {
        emit(doc.parent, {_id: doc.policy_issue});
    }
}
