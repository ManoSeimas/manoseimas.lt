// ------------------------------------
// Constants
// ------------------------------------
export const EXPAND_TOPICS = 'EXPAND_TOPICS'
export const SELECT_FRACTION = 'SELECT_FRACTION'
export const SET_SELECTED_FRACTIONS = 'SET_SELECTED_FRACTIONS'

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

export function setSelectedFractions (fraction_ids) {
    return {
        type: SET_SELECTED_FRACTIONS,
        fraction_ids: fraction_ids
    }
}

export const actions = {
    expandTopics,
    selectFraction,
    setSelectedFractions
}

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
    EXPAND_TOPICS: (state, action) => {
        // Close expanded mp on second click.
        if (state.expanded_mp === action.mp_id)
            return Object.assign({}, state, { expanded_mp: undefined })

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
    },
    SET_SELECTED_FRACTIONS: (state, action) => {
        return Object.assign({}, state, { selected_fractions: action.fraction_ids})
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