import Cookies from 'js-cookie'
import { finishTest } from './test_state'

function api_call(method, url, req_body) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest()
    request.open(method, url, true)
    request.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
    request.addEventListener('load', () => resolve(request.responseText))
    request.addEventListener('error', () => reject('Request Error: ', request.response))
    request.send(req_body)
  })
}

// ------------------------------------
// Constants
// ------------------------------------
export const SAVE_ANSWER = 'SAVE_ANSWER'
export const LOAD_RESULTS = 'LOAD_RESULTS'
export const SET_ACTIVE_TAB = 'SET_ACTIVE_TAB'

// ------------------------------------
// Actions
// ------------------------------------

export function loadResults (results) {
  return {
    type: LOAD_RESULTS,
    results: results
  }
}

export function setActiveTab (tab_id) {
  return {
    type: SET_ACTIVE_TAB,
    tab_id: tab_id
  }
}

export function saveAnswer (topic_id, answer) {
  return {
    type: SAVE_ANSWER,
    topic_id: topic_id,
    answer: answer
  }
}

export function saveAllAnswers () {
  return (dispatch, getState) => {
    dispatch(finishTest())  // Go to results page.
    return new Promise(resolve => {
      // Save answers
      const answers = getState().results.answers
      api_call('POST', '/test/json/answers', JSON.stringify(answers))
        .then(response => {
          // Get and load user's results
          const user_id = JSON.parse(response).user
          api_call('POST', '/test/results/', `user_id=${user_id}&test_id=1`)
            .then(response => {
              const results = JSON.parse(response)
              dispatch(loadResults(results))
            })
            .catch(error => console.error(error))
        })
        .catch(error => console.error(error))
    })
  }
}

export const actions = {
  saveAnswer,
  saveAllAnswers,
  loadResults
}

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
  SAVE_ANSWER: (state, action) => {
    let answers = state.answers
    answers[action.topic_id] = action.answer
    return Object.assign({}, state, { answers: answers })
  },
  SET_ACTIVE_TAB: (state, action) => {
    return Object.assign({}, state, { active_tab: action.tab_id })
  },
  LOAD_RESULTS: (state, action) => {
    return Object.assign({}, state, {
      fractions: action.results.fractions,
      mps: action.results.mps
    })
  }
}

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  // key - topic_id, value - answer
  // answers can be '1' - positive, '-1' - negative, '0' or undefined - skip
  answers: {},
  fractions: [],
  mps: [],
  active_tab: 'fractions'
}
export default (state = initialState, action) => {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}