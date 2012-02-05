function(doc) {
    if (doc.is_legal_act && doc.cleaned_name) {
        emit(doc.cleaned_name, null);
    }
}
