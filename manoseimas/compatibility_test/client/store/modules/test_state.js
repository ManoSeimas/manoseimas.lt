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
export function setActiveTopic (slug) {
  return {
    type: SET_ACTIVE_TOPIC,
    slug
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
    // If there are no slug given, it's first topic
    let position = 0
    let found = false // Set to true when find at least one topic
    const topic = (action.slug)
      ? state.topics.filter(t => {
        if (!found)
          position += 1

        if (t.slug === action.slug) {
          found = true
          return true
        }
        return false
      })[0]
      : state.topics[0]

    let next_topic =  {
      position: position+1,
      slug: ((position) < state.topics.length) ? state.topics[position].slug : 'undefinedx'
    }

    return Object.assign({}, state, {
      active_topic: topic,
      active_topic_position: position,
      previous_position: (state.active_topic && position > 0) ? position - 1 : undefined,
      next_topic: next_topic
    })
  },
  FINISH_TEST: (state, action) => {
    return Object.assign({}, state, {
      active_topic: undefined,
      next_topic: {},
      previous_position: undefined,
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
  },
}

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  active_topic: {},
  active_topic_slug: '',
  next_topic: {
    position: 0,
    slug: ''
  },
  previous_position: undefined,
  topics: [],
  topics_amount: 0,
  title: 'Test name'
}
export default (state = initialState, action) => {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}