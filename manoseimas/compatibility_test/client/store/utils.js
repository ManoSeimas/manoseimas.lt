import Cookies from 'js-cookie'

export function fetch(method, url, req_body) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest()
    request.open(method, url, true)
    request.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
    request.addEventListener('load', () => resolve(request.responseText))
    request.addEventListener('error', () => reject('Request Error: ', request.response))
    request.send(req_body)
  })
}