import { combineReducers } from 'redux'
import { routerReducer as router } from 'react-router-redux'
import test_state from './modules/test_state'
import results from './modules/results'

export const makeRootReducer = (asyncReducers) => {
  return combineReducers({
    // Add sync reducers here
    test_state,
    results,
    router,
    ...asyncReducers
  })
}

export default makeRootReducer