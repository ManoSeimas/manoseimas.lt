import { saveAllAnswers } from './results'

// ------------------------------------
// Constants
// ------------------------------------
export const SET_ACTIVE_TOPIC = 'SET_ACTIVE_TOPIC'
export const FINISH_TEST = 'FINISH_TEST'
export const TOGGLE_ARGUMENTS_MODAL = 'TOGGLE_ARGUMENTS_MODAL'
export const TOGGLE_MORE_MODAL = 'TOGGLE_MORE_MODAL'

// ------------------------------------
// Actions
// ------------------------------------
export function setActiveTopic (topic_id) {
  return {
    type: SET_ACTIVE_TOPIC,
    topic_id: topic_id
  }
}

export function finishTest () {
  return function (dispatch) {
    dispatch({type: FINISH_TEST})  // Go to results page.
    dispatch(saveAllAnswers())
  }
}

export function toggleArgumentsModal () {
  return {
    type: TOGGLE_ARGUMENTS_MODAL
  }
}

export function toggleMoreModal () {
  return {
    type: TOGGLE_MORE_MODAL
  }
}

export const actions = {
  setActiveTopic,
  finishTest,
  toggleArgumentsModal,
  toggleMoreModal
}

// ------------------------------------
// Action Handlers
// ------------------------------------
function getTopicById (topic_id, topics) {
  for (let topic of topics) {
    if (topic.id === topic_id)
      return topic
  }
  return undefined
}

const ACTION_HANDLERS = {
  SET_ACTIVE_TOPIC: (state, action) => {
    return Object.assign({}, state, {
      active_topic: state.topics[action.topic_id],
      previous_topic_id: (state.active_topic) ? action.topic_id - 1 : undefined,
      next_topic_id: (state.active_topic) ? action.topic_id + 1 : 1
    })
  },
  FINISH_TEST: (state, action) => {
    return Object.assign({}, state, {
      active_topic: undefined,
      next_topic_id: 0,
      previous_topic_id: undefined,
    })
  },
  TOGGLE_ARGUMENTS_MODAL: (state, action) => {
    return Object.assign({}, state, {
      active_topic: Object.assign({}, state.active_topic, {
        arguments_modal: !state.active_topic.arguments_modal,
        more_modal: false
      })
    })
  },
  TOGGLE_MORE_MODAL: (state, action) => {
    return Object.assign({}, state, {
      active_topic: Object.assign({}, state.active_topic, {
        arguments_modal: false,
        more_modal: !state.active_topic.more_modal
      })
    })
  }
}

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  active_topic: undefined,
  next_topic_id: 0,
  previous_topic_id: undefined,
  topics: [],
  title: 'Test name'
}
export default (state = initialState, action) => {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}