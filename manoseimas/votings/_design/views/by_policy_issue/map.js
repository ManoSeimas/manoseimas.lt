function(doc) {
    if (doc.policy_issue) {
        emit(doc.policy_issue, null);
    }
}
