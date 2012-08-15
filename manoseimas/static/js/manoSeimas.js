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

  function activateMenuItem(id) {
    $('.sidebar li').removeClass('active');
    $('.sidebar a[href="#' + id + '"]').parent().addClass('active');
  }

  function chooseMenuAnchor() {
    var viewportHeight = Math.min($(window).height(), 600);
    var viewportCenter = $(window).scrollTop() + viewportHeight / 2;

    function centerDistance(elem) {
      var elemCenter = $(elem).offset().top + Math.min($(elem).height(), viewportHeight) / 2;
      return Math.abs(viewportCenter - elemCenter);
    }

    var minDistance = Infinity;
    var minId;

    $('h1').each(function(index, item) {
      var d = centerDistance($(item).parent());
      if (d < minDistance) {
        minDistance = d;
        minId = item.id;
      }
    });

    if (minDistance < Infinity) {
      activateMenuItem(minId);
    }
  }

  manoSeimas.chooseMenuAnchor = chooseMenuAnchor;

  function throttle(delay, fn) {
    var timer = null;
    var lastVal = null;
    var postFire = false;
    return function (args) {
      if (timer) {
        postFire = true;
        return lastVal;
      } else {
        lastVal = fn.apply(args);
        timer = setTimeout(function() {
          if (postFire) {
            fn.apply(args);
          }
          postFire = false;
          timer = null;
        }, delay);
        return lastVal;
      }
    }
  }

  manoSeimas.throttle = throttle;


  function submitPosition(url, node_id, position, callback) {
    var postData = {
      node: "+" + node_id,
      position: position
    };
    $.post(url, postData, callback, 'html');
  };

  manoSeimas.submitPosition = submitPosition;

  function showFractionMPs(fraction) {
    var mps = $('.doc-type-mpprofile');
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

    $('.doc-type-fraction .description p:first-child').click(function() {
      $('#result-tabs a[href=#seimo-nariai]').tab('show');
      var slug = $(this).parent().parent().data('slug');
      $('#filter-fraction').val(slug).change();
    });
  }

  manoSeimas.activateFractionFilter = activateFractionFilter;
})(window);
