function(doc) {
  if (doc.language == 'lt' && !doc.corrects &&
      (doc.type == 'įstatymas' || doc.type == 'konstitucija')) {
    emit(doc.number, null);
  }
}
