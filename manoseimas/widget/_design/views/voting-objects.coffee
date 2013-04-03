(doc) ->
  return unless doc.doc_type == "Voting" 
  
  emit [doc._id, doc.doc_type], { _id: doc._id }
  
  for vote,voters of doc.votes
    for v in voters
      emit [doc._id, "MPProfile", vote], { _id: v[0] }
      emit [doc._id, "Fraction", vote], { _id: v[1] }
