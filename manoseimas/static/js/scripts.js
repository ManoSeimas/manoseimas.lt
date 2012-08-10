function ensureSidebarFits() {
  var sidebarInner = $('#middle .sidebar-inner');
  var height = sidebarInner.height() + 20;
  $('#middle .content').css('min-height', height + 'px');
  if (height >= $('#middle').height()) {
    sidebarInner.css('position', 'static');
  }
}

$(ensureSidebarFits);

function activateMenuItem(id) {
  $('.sidebar li').removeClass('active');
  $('.sidebar a[href="#' + id + '"]').parent().addClass('active');
}

function chooseMenuAnchor() {
  var viewportHeight = $(window).height();
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
