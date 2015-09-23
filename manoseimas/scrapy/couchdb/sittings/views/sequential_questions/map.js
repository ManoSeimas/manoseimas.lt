function (doc) {
  if (doc.doc_type == 'question') {
    emit(parseInt(doc._id), null);
  }
}
