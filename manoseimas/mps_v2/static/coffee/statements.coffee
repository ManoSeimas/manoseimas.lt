loadStatments = (data, url) ->
  $('.statements-component').html(data)
  loadStatementEvents(url)

  # Set selected sidebar item + make sidebar sticky
  selected_session = $('.sidebar').attr("data-selected-session")
  $("[data-session='#{selected_session}']").addClass("selected")
  $('.ui.sticky').sticky({context: '.transcriptions', offset: 70})


## EVENTS
search_params = $(location).attr('search')
global_session = null

buildSearchParams = ->
  only_as_presenter = $('#only_as_presenter').checkbox('is checked')
  params = []
  if global_session and global_session isnt 'None'
    params.push "session=#{global_session}"
  if only_as_presenter
    params.push "only_as_presenter=1"
  return "?#{params.join('&')}"

loadStatementEvents = (url) ->
  $('.show-all').click ->
    content = []
    discussion_url = '/json/discussion/'+$(this).attr("data-id")

    $.getJSON discussion_url, (data) ->
      for statement in data.statements
        content.push('<div class="statement">')
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
    global_session = $(this).attr('data-session')
    search_params = buildSearchParams()
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

  $('#only_as_presenter input').change (e) ->
    e.preventDefault()
    search_params = buildSearchParams()
    $.get "#{url}#{search_params}", (data) ->
      loadStatments(data, url)
