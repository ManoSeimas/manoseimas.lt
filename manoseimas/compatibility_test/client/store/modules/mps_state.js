// ------------------------------------
// Constants
// ------------------------------------
export const EXPAND_TOPICS = 'EXPAND_TOPICS'

// ------------------------------------
// Actions
// ------------------------------------
export function expandTopics (mp_id) {
    return {
        type: EXPAND_TOPICS,
        mp_id: mp_id
    }
}

export const actions = {
    expandTopics
}

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
    EXPAND_TOPICS: (state, action) => {
        return Object.assign({}, state, { expanded_mp: action.mp_id })
    }
}

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
    expanded_mp: undefined
}
export default (state = initialState, action) => {
    const handler = ACTION_HANDLERS[action.type]
    return handler ? handler(state, action) : state
}