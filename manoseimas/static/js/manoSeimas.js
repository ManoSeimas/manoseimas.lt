(function(window) {
  manoSeimas = {}
  window.manoSeimas = manoSeimas;

  function ensureSidebarFits() {
    var sidebarInner = $('#middle .sidebar-inner');
    var height = sidebarInner.height() + 20;
    $('#middle .content').css('min-height', height + 'px');
    if (height >= $('#middle').height()) {
      sidebarInner.css('position', 'static');
    }
  }

  $(manoSeimas.ensureSidebarFits);

  function submitPosition(url, node_id, position, callback) {
    var postData = {
      node: "+" + node_id,
      position: position
    };
    $.post(url, postData, callback, 'html');
  };

  manoSeimas.submitPosition = submitPosition;

  function handlePositionChange(callback) {
    $(".answers > .position-buttons > button, .answers > .important input").click(function() {
      var sender = $(this);
      var answers = $($(this).parents('.answers'));
      var solutionId = answers.data('solution');
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
  }

  manoSeimas.handlePositionChange = handlePositionChange;

  function showFractionMPs(fraction) {
    var mps = $('.mpprofile');
    if (fraction === '') {
      mps.show();
    } else {
      var fractionClass = '.fraction-' + fraction;
      mps.not(fractionClass).hide();
      mps.filter(fractionClass).show();
    }
  }

  manoSeimas.showFractionMPs = showFractionMPs;

  function activateFractionFilter(){
    $('#filter-fraction').change(function() {
      showFractionMPs(this.value);
    });

    $('.fraction .result-description .percent').click(function() {
      $('#result-tabs a[href=#seimo-nariai]').tab('show');
      var slug = $(this).data('slug');
      $('#filter-fraction').val(slug).change();
    });
  }

  manoSeimas.activateFractionFilter = activateFractionFilter;
})(window);
