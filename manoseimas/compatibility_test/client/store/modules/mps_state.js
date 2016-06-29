// ------------------------------------
// Constants
// ------------------------------------
export const EXPAND_TOPICS = 'EXPAND_TOPICS'
export const SELECT_FRACTION = 'SELECT_FRACTION'

// ------------------------------------
// Actions
// ------------------------------------
export function expandTopics (mp_id) {
    return {
        type: EXPAND_TOPICS,
        mp_id: mp_id
    }
}

export function selectFraction (fraction_id) {
    return {
        type: SELECT_FRACTION,
        fraction_id: fraction_id
    }
}

export const actions = {
    expandTopics,
    selectFraction
}

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
    EXPAND_TOPICS: (state, action) => {
        return Object.assign({}, state, { expanded_mp: action.mp_id })
    },
    SELECT_FRACTION: (state, action) => {
        let selected_fractions = state.selected_fractions
        if (selected_fractions.indexOf(action.fraction_id) < 0) {
            // In tersm of avoing state Array mutation we're not able to use .push here.
            selected_fractions = [...selected_fractions, action.fraction_id]
        } else {
            // Removing fraction from list on second click (if it's already on the list).
            let position = selected_fractions.indexOf(action.fraction_id)
            selected_fractions = [
                ...selected_fractions.splice(0, position),
                ...selected_fractions.splice(position+1)
            ]
        }
        return Object.assign({}, state, { selected_fractions: selected_fractions })
    }
}

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
    expanded_mp: undefined,
    selected_fractions: []
}
export default (state = initialState, action) => {
    const handler = ACTION_HANDLERS[action.type]
    return handler ? handler(state, action) : state
}