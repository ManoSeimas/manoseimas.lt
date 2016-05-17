import { createStore } from 'redux'
// import thunk from 'redux-thunk'
import makeRootReducer from './reducers'

export default (initialState = {}) => {
  // ======================================================
  // Store Instantiation and HMR Setup
  // ======================================================
  const store = createStore(
    makeRootReducer(),
    initialState,
  )
  store.asyncReducers = {}

  if (module.hot) {
    module.hot.accept('./reducers', () => {
      const reducers = require('./reducers').default
      store.replaceReducer(reducers)
    })
  }

  return store
}