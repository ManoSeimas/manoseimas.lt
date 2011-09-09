function(doc) {
     if (doc.doc_type == "document") {
          emit(doc._id, null);
     }
}
