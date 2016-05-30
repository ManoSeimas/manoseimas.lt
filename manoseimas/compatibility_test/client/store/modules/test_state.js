// ------------------------------------
// Constants
// ------------------------------------
export const SET_ACTIVE_QUESTION = 'SET_ACTIVE_QUESTION'

// ------------------------------------
// Actions
// ------------------------------------
export function setActiveQuestion (question_id) {
  return {
    type: SET_ACTIVE_QUESTION,
    question_id: question_id
  }
}

export const actions = {
  setActiveQuestion
}

// ------------------------------------
// Action Handlers
// ------------------------------------
function getQuestionById (question_id, questions) {
    for (let question of questions) {
        if (question.id === question_id)
            return question
    }
    return undefined
}

const ACTION_HANDLERS = {
  SET_ACTIVE_QUESTION: (state, action) => {
    return Object.assign({}, state, {
      active_question: state.questions[action.question_id],
      previous_question_id: (state.active_question) ? state.active_question.id : undefined,
      next_question_id: (state.active_question) ? state.active_question.id + 1 : 1
    })
  }
}

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  active_question: undefined,
  next_question_id: 1,
  previous_question_id: undefined,
  questions: [{
    id: 1,
    title: 'One'
  }, {
    id: 2,
    title: 'Two'
  }, {
    id:3,
    title: 'Three'
  }]
}
export default (state = initialState, action) => {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}