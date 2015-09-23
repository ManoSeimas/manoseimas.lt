function (doc) {
  if (doc.doc_type == 'voting') {
    emit(parseInt(doc._id), null);
  }
}
