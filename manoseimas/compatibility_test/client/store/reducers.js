import { combineReducers } from 'redux'
import { routerReducer as router } from 'react-router-redux'
import questions from './modules/questions'
import test_state from './modules/test_state'

export const makeRootReducer = (asyncReducers) => {
  return combineReducers({
    // Add sync reducers here
    test_state,
    // questions,
    router,
    ...asyncReducers
  })
}

export default makeRootReducer