import { finishTest } from './test_state'
import { fetch } from '../utils'

// ------------------------------------
// Constants
// ------------------------------------
export const SAVE_ANSWER = 'SAVE_ANSWER'
export const LOAD_ANSWERS = 'LOAD_ANSWERS'
export const GET_ANSWERS = 'GET_ANSWERS'
export const LOAD_RESULTS = 'LOAD_RESULTS'
export const GET_RESULTS = 'GET_RESULTS'
export const SET_ACTIVE_TAB = 'SET_ACTIVE_TAB'
export const TOGGLE_IMPORTANCE = 'TOGGLE_IMPORTANCE'
export const SHOW_HEADER = 'SHOW_HEADER'
export const HIDE_HEADER = 'HIDE_HEADER'

// ------------------------------------
// Actions
// ------------------------------------

export function loadResults (results) {
  return {
    type: LOAD_RESULTS,
    results: results
  }
}

export function getResults () {
  return (dispatch, getState) => {
    return new Promise(resolve => {
      fetch('POST', '/test/results/', 'test_id=1')
        .then(response => {
          const results = JSON.parse(response)
          dispatch(loadResults(results))
        })
        .catch(error => console.error(error))
    })
  }
}

export function loadAnswers (answers) {
  return {
    type: LOAD_ANSWERS,
    answers: answers
  }
}

export function getAnswers () {
  return (dispatch, getState) => {
    return new Promise(resolve => {
      fetch('GET', '/test/json/answers')
        .then(response => {
          const answers = JSON.parse(response).answers
          dispatch(loadAnswers(answers))
        })
        .catch(error => console.error(error))
    })
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

export function toggleImportance (topic_id) {
  return {
    type: TOGGLE_IMPORTANCE,
    topic_id: topic_id
  }
}

export function saveAllAnswers () {
  return (dispatch, getState) => {
    dispatch(finishTest())  // Go to results page.
    return new Promise(resolve => {
      // Save answers
      const answers = getState().results.answers
      fetch('POST', '/test/json/answers', JSON.stringify(answers))
        .then(response => {
          // Get and load user's results
          const test_id = JSON.parse(response).test_id
          fetch('POST', '/test/results/', `test_id=${test_id}`)
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

export function showHeader () {
  return {
    type: SHOW_HEADER
  }
}

export function hideHeader () {
  return {
    type: HIDE_HEADER
  }
}

export const actions = {
  toggleImportance,
  saveAnswer,
  saveAllAnswers,
  setActiveTab,
  loadResults,
  getResults,
  showHeader,
  hideHeader
}

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
  SAVE_ANSWER: (state, action) => {
    let answers = Object.assign({}, state.answers)
    answers[action.topic_id] = Object.assign({}, answers[action.topic_id], {answer: action.answer})
    return Object.assign({}, state, { answers: answers })
  },
  TOGGLE_IMPORTANCE: (state, action) => {
    let answers = Object.assign({}, state.answers)
    let answer = answers[action.topic_id] || {}
    answers[action.topic_id] = Object.assign({}, answer, {important: !answer.important})
    return Object.assign({}, state, { answers: answers })
  },
  SET_ACTIVE_TAB: (state, action) => {
    return Object.assign({}, state, { active_tab: action.tab_id })
  },
  LOAD_RESULTS: (state, action) => {
    return Object.assign({}, state, {
      fractions: action.results.fractions,
      mps: action.results.mps,
      answers: action.results.user_answers
    })
  },
  LOAD_ANSWERS: (state, action) => {
    return Object.assign({}, state, {answers: action.answers})
  },
  SHOW_HEADER: (state, action) => {
    return Object.assign({}, state, { show_header: true })
  },
  HIDE_HEADER: (state, action) => {
    return Object.assign({}, state, { show_header: false })
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
  active_tab: 'fractions',
  show_header: false
}
export default (state = initialState, action) => {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}