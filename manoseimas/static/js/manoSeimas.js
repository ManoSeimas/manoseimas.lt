(function (window) {
  var manoSeimas = {};
  window.manoSeimas = manoSeimas;

  manoSeimas.ensureSidebarFits = function () {
    var sidebarInner = $('#middle .sidebar-inner');
    var height = sidebarInner.height() + 20;
    $('#middle .content').css('min-height', height + 'px');
    if (height >= $('#middle').height()) {
      sidebarInner.css('position', 'static');
    }
  };

  $(manoSeimas.ensureSidebarFits);

  manoSeimas.submitPosition = function (url, node_id, position, callback) {
    var postData = {
      node: "+" + node_id,
      position: position
    };
    $.post(url, postData, callback, 'html');
  };

  manoSeimas.handlePositionChange = function (callback) {
    $(".answers > .position-buttons > button, .answers > .important input").click(function() {
      var sender = $(this);
      var answers = $($(this).parents('.answers'));
      var solutionId = answers.attr('data-solution');
      if (sender.is('input')) {
        var btnPosition = answers.find('.position-buttons > button.active').data('value');
      } else {
        var btnPosition = sender.data('value');
      }
      var important = answers.find('.important input').is(':checked') ? 2 : 1;
      var position = btnPosition * important;
      var url = "/testas/submit-position/";
      manoSeimas.submitPosition(url, solutionId, position, callback && function(result) {
        callback(result, solutionId, position);
      });
    });
  };

  manoSeimas.showFractionMPs = function (fraction) {
    var mps = $('.mpprofile');
    if (fraction === '') {
      mps.show();
    } else {
      var fractionClass = '.fraction-' + fraction;
      mps.not(fractionClass).hide();
      mps.filter(fractionClass).show();
    }
  };

  manoSeimas.activateFractionFilter = function () {
    $('#filter-fraction').change(function() {
      showFractionMPs(this.value);
    });

    $('.fraction .result-description .percent').click(function () {
      $('#result-tabs a[href=#seimo-nariai]').tab('show');
      var slug = $(this).data('slug');
      $('#filter-fraction').val(slug).change();
    });
  };
})(window);
