#_require config.coffee

# Simple DOM selector
$ = (selector, context = document) ->
    [c, name] = selector.match(/^(\.|\#)?(.*)/)[1..2]
    if c is "#"
        context.getElementById name
    else if c is "."
        context.getElementsByClassName name
    else if name?
        context.getElementsByTagName name

# Template Renderer
render = (template, data) ->
    Handlebars.templates[template](data)

# Basic display helpers
show = (elements...) ->
    e.style.display = '' for e in elements

hide = (elements...) ->
    e.style.display = 'none' for e in elements


# Convenience function for rendering partials. We're 
# avoiding the built-in partials because they require a
# separate build route (seemingly without reason).
Handlebars.registerHelper "render", (template) ->
    new Handlebars.SafeString(render template, this)

# For iterating over objects in Handlebars templates
Handlebars.registerHelper "key_value", (obj, options) ->
    (options.fn(key: k, value: v) for own k, v of obj).join('')

# For iterating over hash values in Handlebars templates
Handlebars.registerHelper "each_value", (obj, options) ->
    (options.fn(v) for own k,v of obj).join('')

# Constructs a URL to webpage identified by the slug
Handlebars.registerHelper "page_url", (slug) ->
    SERVER_URL + "/" + slug


# Inject CSS into DOM from template
inject_css = (target) -> 
    return if $("#MSWidget-style")

    style = document.createElement 'style'
    style.type = 'text/css'
    style.id = 'MSWidget-style'
    
    if style.styleSheet
        # IE
        style.styleSheet.cssText = render("widget.css")
    else 
        # Other browsers
        style.innerHTML = render("widget.css")

    target.appendChild style

update_position = (slug, position, callback) ->
    post VOTING_URL, { position: position, node: "+"+slug }, callback

fetch_profile = (profile_id, callback) ->
    fetch_data SERVER_URL + "/" + profile_id + ".json", (data) ->
        callback data if callback?

fetch_voting = (slug, callback) ->
    fetch_data DATA_URL+"/voting/"+slug, (data) ->
        if data.error
            console.log "Error encountered fetching voting #{slug}"
            return callback data

        # Rebuilding object links, and additional data massage for template convenience
        for own type,vote_list of data.voting.votes
            for v,i in vote_list
                mp = data.mps[ v[0] ]
                fraction = data.fractions[ v[1] ]
                vote_list[i] = mp

                mp.vote = type
                mp.fraction = fraction
                fraction.votes ?= { aye: 0, no: 0, abstain: 0 }
                fraction.votes[type]++

        callback data if callback?

# Fetch a document from our couchdb instance
fetch_data = (url, callback) ->
    get url, (xhr) ->
        if xhr.status is 200 or xhr.status is 304  
            data = eval '(' + xhr.responseText + ')'
            callback data
        else
            console.log 'Error loading data...'


get = (url, callback) ->
    ajax_request url, 'GET', null, callback

post = (url, params, callback) ->
    ajax_request url, 'POST', params, callback

ajax_request = (url, method, params, callback) ->
    if XMLHttpRequest?
        xhr = new XMLHttpRequest()
    else
        # Older MSIE
        for v in ["MSXML2.XmlHttp.6.0", "MSXML2.XmlHttp.3.0", "Msxml2.XMLHTTP"]
            try xhr = new ActiveXObject v; break catch e

    xhr.withCredentials = true
    xhr.onreadystatechange = ->
        if xhr.readyState is 4 # COMPLETE
            callback xhr if callback

    if method is "GET"
        xhr.open 'GET', encodeURI(url), true
        xhr.send()
    else
        xhr.open 'POST', encodeURI(url), true
        xhr.setRequestHeader "Content-type", "application/x-www-form-urlencoded"

        matches = document.cookie.match /csrftoken=([^;]+)/i        
        xhr.setRequestHeader "X-CSRFToken", decodeURIComponent(matches[1]) if matches?[1]?

        postdata = (k+"="+encodeURIComponent(v) for k,v of params).join '&'
        xhr.send postdata



