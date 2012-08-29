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

    $('.fraction .description .percent').click(function() {
      $('#result-tabs a[href=#seimo-nariai]').tab('show');
      var slug = $(this).data('slug');
      $('#filter-fraction').val(slug).change();
    });
  }

  manoSeimas.activateFractionFilter = activateFractionFilter;
})(window);
