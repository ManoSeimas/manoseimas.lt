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
      var newShadow = '0px 1px 2px 0px rgba(0, 0, 0, ' + calculations.percentagePassed / 7 + '), 0px 0px 0px 1px rgba(0, 0, 0, ' + calculations.percentagePassed / 20 + '0)';
      $('header .pointing.menu').css('background-color', newColor);
      $('header .pointing.menu').css('box-shadow', newShadow);
    }
  });

$('.photo-box.parliamentarian')
  .visibility({
    once       : false,
    continuous : true,
    onPassing  : function(calculations) {
      var newColor = 'rgba(255, 255, 255, ' + calculations.percentagePassed +')';
      var newShadow = '0px 1px 2px 0px rgba(0, 0, 0, ' + calculations.percentagePassed / 7 + '), 0px 0px 0px 1px rgba(0, 0, 0, ' + calculations.percentagePassed / 20 + '0)';
      $('header .pointing.menu').css('background-color', newColor);
      $('header .pointing.menu').css('box-shadow', newShadow);
    },
    onBottomPassed: function(element) {
      $('header.ui.page.grid').css('display', 'none');
      $('header.ui.grid.scrooled').css('display', 'inline-block');
      $('header .pointing.menu').css('background-color', 'whote');
      // $('header .pointing.menu').css('box-shadow', newShadow);
    },
    onTopVisible: function(element) {
      $('header.ui.page.grid').css('display', 'inline-block');
      $('header.ui.grid.scrooled').css('display', 'none');
    }
  });

});
