loadStatments = (data, slug) ->
  $('.statements-component').html(data)
  loadStatementEvents(slug)
  $('.ui.sticky').sticky({context: '.transcriptions', offset: 70});
  console.log  "Load was performed."

$(document).ready ->
  ## Initial Load
  slug = $('.statements-component').attr("data-slug")
  $.get "/mp/statements/#{slug}", (data) ->
    loadStatments(data, slug)
    console.log  "Load was performed."


## EVENTS
loadStatementEvents = (slug) ->
  $('.show-all').click ->
    content = []
    url = '/mp/discussion_json/'+$(this).attr("data-id")
    $.getJSON url, (data) ->
      for statement in data.statements
        content.push('<div class="statement">');
        if statement.selected
          content.push '<p class="highlighted">'
        else
          content.push '<p>'

        if statement.as_chairperson
          content.push '<i class="spy icon" title="Pirmininkas"></i>'

        content.push '<b>'+statement.speaker_name+' </b>'
        content.push statement.text
        content.push '</p>'
        content.push '</div>'

      $('.ui.modal .header').text data.topic.title
      $('.ui.modal .description').html content.join("")
      $('.ui.modal').modal 'show', 'show dimmer'

  $('.ui.pagination.menu .next').click  (e) ->
    e.preventDefault()
    next_page = $(this).attr("data-next-page")
    console.log "Loading"
    $.get "/mp/statements/#{slug}?page=#{next_page}", (data) ->
      # Scroll to top of statments.
      $.scrollTo('.transcripts', 10, {offset: -40})
      loadStatments(data, slug)

  $('.ui.pagination.menu .prev').click  (e) ->
    prev_page = $(this).attr("data-prev-page")
    $.get "/mp/statements/#{slug}?page=#{prev_page}", (data) ->
      $.scrollTo('.transcripts', 100, {offset: -40})
      loadStatments(data, slug)



