import { combineReducers } from 'redux'
import { routerReducer as router } from 'react-router-redux'
import test_state from './modules/test_state'
import results from './modules/results'
import mps_state from './modules/mps_state'

export const makeRootReducer = (asyncReducers) => {
  return combineReducers({
    // Add sync reducers here
    test_state,
    results,
    mps_state,
    router,
    ...asyncReducers
  })
}

export default makeRootReducer