$(document).ready ->

  onPassingVisibility = (calculations) ->
    newColor = "rgba(255, 255, 255, #{calculations.percentagePassed})"
    $('header .pointing.menu').css 'background-color', newColor

  $('.photo-box').visibility
    once       : false,
    continuous : true,
    onPassing  : onPassingVisibility

  $('.photo-box.parliamentarian').visibility
    once       : false,
    continuous : true,
    onPassing  : onPassingVisibility
    onBottomPassed: (element) ->
      $('header.ui.page.grid').css('display', 'none')
      $('header.ui.grid.scrooled').css('display', 'inline-block')
      $('header .pointing.menu').css('background-color', 'whote')
    onTopVisible: (element) ->
      $('header.ui.page.grid').css('display', 'inline-block')
      $('header.ui.grid.scrooled').css('display', 'none')

