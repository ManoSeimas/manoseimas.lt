#_require MSWidget.coffee
#_require utils.coffee

# Initialize Widget
do ->
    console.log "MSWidget Init..."
    inject_css document.getElementsByTagName("head")[0]

    handle = $("#MSWidget")
    unless handle?
        handle = document.createElement "div"
        handle.id = "MSWidget"
        show handle

        p = $("body")[0]
        p.insertBefore handle, p.firstChild

    handle.className = "MSWidget"

    window.MSWidgetReady() if window.MSWidgetReady

