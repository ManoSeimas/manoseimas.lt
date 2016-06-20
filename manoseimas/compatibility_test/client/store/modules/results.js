// ------------------------------------
// Constants
// ------------------------------------
export const SAVE_ANSWER = 'SAVE_ANSWER'
export const LOAD_RESULTS = 'LOAD_RESULTS'

// ------------------------------------
// Actions
// ------------------------------------
export function saveAnswer (topic_id, answers) {
  return {
    type: SAVE_ANSWER,
    topic_id: topic_id,
    answers: answers
  }
}

export function loadResults (user_id, test_id) {
  return {
    type: LOAD_RESULTS,
    user_id: user_id,
    test_id: test_id
  }
}

export const actions = {
  saveAnswer,
  loadResults
}

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
  SAVE_ANSWER: (state, action) => {
    let answers = state.answers
    answers[action.topic_id] = action.answers
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