function ensureSidebarFits() {
  var sidebarInner = $('#middle .sidebar-inner');
  var height = sidebarInner.height() + 20;
  $('#middle .content').css('min-height', height + 'px');
  if (height >= $('#middle').height()) {
    sidebarInner.css('position', 'static');
  }
}

$(ensureSidebarFits);
