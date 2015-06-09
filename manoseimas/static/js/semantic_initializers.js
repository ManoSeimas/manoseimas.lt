$(document).ready(function() {
  $('.ui.checkbox').checkbox('toggle');
  $('.ui.dropdown').dropdown();
  $('.ui.indicating.progress').progress({showActivity: false});
  $('.ui.sticky').sticky({context: '.parliamentarians'});
  $('.tabular.menu .item').tab();
  $('.rating').popup();
;

  $('.photo-box').visibility({
    once       : false,
    continuous : true,
    onPassing  : function(calculations) {
      var newColor = 'rgba(255, 255, 255, ' + calculations.percentagePassed +')';
      $('header .pointing.menu').css('background-color', newColor);
    }
  });
});
