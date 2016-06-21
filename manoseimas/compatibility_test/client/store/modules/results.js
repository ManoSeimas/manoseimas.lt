import fetch from 'isomorphic-fetch'
import { finishTest } from './test_state'

// ------------------------------------
// Constants
// ------------------------------------
export const SAVE_ANSWER = 'SAVE_ANSWER'
export const LOAD_RESULTS = 'LOAD_RESULTS'

// ------------------------------------
// Actions
// ------------------------------------
export function saveAnswer (topic_id, answer) {
  return {
    type: SAVE_ANSWER,
    topic_id: topic_id,
    answer: answer
  }
}

export function saveAllAnswers () {
  return (dispatch, getState) => {
    dispatch(finishTest())
    return fetch('/test/json/answers', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(getState().results.answers)
    }).then(response => response.json())
      .then(json => console.log('JSON ', json))
      .catch(err => console.error('Request error: ', err))
  }
}
// export function saveAllAnswers () {
//   return (dispatch, getState) => {
//     dispatch(finishTest())
//     let answers = getState().results.answers
//     return new Promise(resolve => {
//       const request = new XMLHttpRequest()
//       request.open('POST', '/test/json/answers', true)
//       request.onlaod = function () {
//         if (request.status >= 200 && request.status < 400) {
//           console.log(JSON.parse(request.responseText))
//         } else {
//           console.error('Request error!')
//         }
//       }
//       request.send(JSON.stringify(answers))
//     })
//   }
// }

export function loadResults (user_id, test_id) {
  return {
    type: LOAD_RESULTS,
    user_id: user_id,
    test_id: test_id
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
  LOAD_RESULTS: (state, action) => {
    // TODO: write code which will call some API and will load answers.
    return Object.assign({}, state)
  }
}

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  // key - topic_id, value - answer
  // answers can be '1' - positive, '-1' - negative, '0' or undefined - skip
  answers: {},
}
export default (state = initialState, action) => {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}