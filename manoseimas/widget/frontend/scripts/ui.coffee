# UI Handlers, effects, and related magic

mps_scroll_tracked = fractions_scroll_tracked = false

# This is called any time the widget's UI is reloaded.
ui_refresh = () ->
    $("#MSWidget-fractions").onscroll = (e) ->
        unless fractions_scroll_tracked
            track_event "Scroll", "Fractions"
            fractions_scroll_tracked = true
    
    $("#MSWidget-mps-content").onscroll = (e) ->
        unless mps_scroll_tracked
            track_event "Scroll", "MPs"
            mps_scroll_tracked = true

        detect_mps_section()

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
