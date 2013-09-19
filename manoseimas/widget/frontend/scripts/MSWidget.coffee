#_require utils.coffee
#_require ui.coffee

window.MSWidget = {
    content: undefined,
    profile: undefined,
    position: undefined,

    load_voting: (voting_id) ->
        $("#MSWidget").innerHTML = render "loading-frame"
        fetch_voting voting_id, (data) ->
            if data.error
                MSWidget.content = undefined
                $("#MSWidget").innerHTML = render "error-pane", { message: "Problem loading voting `#{voting_id}`: #{data.error}" }
            else
                MSWidget.content = data
                $("#MSWidget").innerHTML = render "widget-frame", MSWidget.content
                ui_refresh()
                MSWidget.show_fractions track: false

    load_profile: (profile_id, callback) ->
        fetch_profile profile_id, (profile) ->
            MSWidget.profile = profile
            callback profile if callback?

    vote: (position) ->
        position *= 2 if $("#important").checked
        MSWidget.position = position

        update_position MSWidget.content.voting._id, position

        if position > 0
            addClass $("#yes"), 'pressed'
            removeClass $("#no"), 'pressed'
            track_event "Vote", "Support", position
        else
            addClass $("#no"), 'pressed'
            removeClass $("#yes"), 'pressed'
            track_event "Vote", "Oppose", position

        MSWidget.show_positions()
        $("#MSWidget-fractions").scrollTop = 0
        MSWidget.show_fractions()

        unless MSWidget.profile
            MSWidget.show_thanks()

    connect: (service) ->
        track_event "Click", "Connect", service

        # Different tweaks for different services
        switch service
            when "google"
                [w,h] = [450, 500]
                url = "/widget/auth/google/popup"
            when "facebook"
                [w,h] = [100,100]
                url = "/accounts/login/facebook"
            when "openid"
                [w,h] = [650, 300]
                url = "/accounts/login/"

        x = screen.width/2 - w/2
        y = screen.height/2 - h/2
        window.open url+"?next=/widget/auth/finish", "", "width=#{w},height=#{h},status=1,location=1,resizable=yes,left=#{x},top=#{y}"
    
    connected: (profile_id) ->
        track_event "Connected"
        MSWidget.hide_overlays()
        MSWidget.load_profile profile_id

    show_fractions: ({track} = {track:true}) ->
        if track
            track_event "Click", "Fractions"

        MSWidget.show_panel 'fractions'

    show_fraction: (fraction) ->
        target = $("#MSWidget-fraction-#{fraction}")
        
        track_event "Click", "Fraction", fraction

        # Because fraction rows are part of a table, we must also incorporate the parent table's offset
        $("#MSWidget-fractions").scrollTop = target.offsetTop + target.offsetParent.offsetTop

    show_mps: (subpanel) ->
        if subpanel?
            track_event "Click", "MP", subpanel
        else
            track_event "Click", "MPs"

        # Lazy loading the MPs list panel to delay MP image loading until we really need it.
        if $("#MSWidget-mps-content").innerHTML is ""
            $("#MSWidget-mps-content").innerHTML = render "mp_list", MSWidget.content

            # Ensures a good default scroll offset
            subpanel = 'aye'

        MSWidget.show_panel 'mps'

        if subpanel?
            # Note: We're nudging just below the section header so it's out of sight. Section headers are mainly for scrolling.
            section = $("#MSWidget-mps-#{subpanel}")
            heading = $(".heading", section)[0]
            section.offsetParent.scrollTop = heading.offsetTop + heading.offsetHeight
             
            for sp in ['aye','no','abstain']
                if subpanel is sp
                    addClass $("#MSWidget-mps-#{sp}_button"), 'active'
                else
                    removeClass $("#MSWidget-mps-#{sp}_button"), 'active'


    show_panel: (panel) ->
        for p in ['fractions', 'mps']
            if panel is p
                show $("#MSWidget-#{p}")
                addClass $("#MSWidget-#{p}_button"), 'active'
            else
                hide $("#MSWidget-#{p}")
                removeClass $("#MSWidget-#{p}_button"), 'active'

    show_overlay: (name) ->
        hide o for o in $(".overlay")
        show $(".overlay_backdrop")[0]
        show $("#MSWidget-#{name}")

    hide_overlays: () ->
        hide o for o in $(".overlay")
        hide $(".overlay_backdrop")[0]
    
    show_thanks: (rerender=true) ->
        if rerender? or $("#MSWidget-thanks").innerHTML is ""
            $("#MSWidget-thanks").innerHTML = render "thanks-pane", { profile: MSWidget.profile }

        MSWidget.show_overlay('thanks')

    show_positions: (rerender=true) ->
        if rerender? or $("#MSWidget-positions").innerHTML is ""
            positions = MSWidget.content.fractions
            if MSWidget.position
                positions.user = {
                    user: true,
                    supports: MSWidget.position >=0,
                    viso: MSWidget.position*110,
                    image: "/static/img/anonymous.png"
                }
                
            $("#MSWidget-positions").innerHTML = render "positions_bar", { positions: positions }

        show $("#MSWidget-positions")

    show_history: () ->
        unless MSWidget.profile
            MSWidget.show_overlay('connect')
            return false

        window.open page_url 'accounts/profile'
        MSWidget.clickthrough 'Voting History'

    clickthrough: (type) ->
        track_event "Link", type
    
}

