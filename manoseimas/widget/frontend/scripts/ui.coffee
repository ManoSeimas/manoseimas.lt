# UI Handlers, effects, and related magic

# This is called any time the widget's UI is reloaded.
ui_refresh = () ->
    $("#MSWidget-mps-content").onscroll = (e) ->
        #check_mp_visibility()
        detect_mps_section()

element_visible = (el) ->
    rect = el.getBoundingCientRect()
    return rect.top >= 0 && rect.left >= 0 && rect.top <= (window.innerHeight || document.documentElement.clientHeight)

load_image = (el, callback) ->
    img = new Image()
    img.alt = ''
    img.onload = () ->
        el.parent.replaceChild img, el
        callback()

    img.src = el.getAttribute 'data-src'

check_mp_visibility = () ->
    for el in $(".lazy")
        if element_visible el
            load_image el

# Automatically select section buttons based on context
detect_mps_section = () ->
    # Note: the order here is important, as we intentionally give 
    # priority to sections positioned closer to the cutoff line (1/3 mark)
    current = null
    for sp in ['abstain', 'no', 'aye']
        section = $("#MSWidget-mps-#{sp}")
        parent = section.offsetParent
        offset = section.offsetTop - parent.scrollTop
        if offset < parent.offsetHeight/3
            current = sp
            break
        
    for sp in ['aye', 'no', 'abstain']
        if current is sp
            $("#MSWidget-mps-#{sp}_button").style.backgroundColor = '#ccc'
        else 
            $("#MSWidget-mps-#{sp}_button").style.backgroundColor = '#fff'
        


#addEventListener('scroll',processScroll);
#EX: https://gist.github.com/aliem/2171438
