loadStatments = (data, url) ->
  $('.statements-component').html(data)
  loadStatementEvents(url)

  # Set selected sidebar item + make sidebar sticky
  selected_session = $('.sidebar').attr("data-selected-session")
  $("[data-session='#{selected_session}']").addClass("selected")
  $('.ui.sticky').sticky({context: '.transcriptions', offset: 70});

  console.log  "Load was performed."


## EVENTS
search_params = $(location).attr('search')
loadStatementEvents = (url) ->
  $('.show-all').click ->
    content = []
    discussion_url = '/mp/discussion_json/'+$(this).attr("data-id")

    $.getJSON discussion_url, (data) ->
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
    $.get "#{url}/#{next_page}#{search_params}", (data) ->
      # Scroll to top of statments.
      $.scrollTo('.transcripts', 10, {offset: -40})
      loadStatments(data, url)

  $('.ui.pagination.menu .prev').click (e) ->
    prev_page = $(this).attr("data-prev-page")
    $.get "#{url}/#{prev_page}#{search_params}", (data) ->
      $.scrollTo('.transcripts', 100, {offset: -40})
      loadStatments(data, url)

  $('.sidebar .item').click (e) ->
    e.preventDefault()
    session = $(this).attr("data-session")
    if session and session isnt 'None'
      search_params = "?session=#{session}"
    else
      search_params = ""
    $.get "#{url}#{search_params}", (data) ->
      loadStatments(data, url)
      $.scrollTo('.transcripts', 100, {offset: -40})


$(document).ready ->
  ## Initial Load
  slug = $('.statements-component').attr("data-slug")
  url = "/mp/statements/#{slug}"
  # $(location).attr 'pathname'
  $.get url, (data) ->
    loadStatments(data, url)