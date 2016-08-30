import React from 'react'
import ReactDOM from 'react-dom'
import { Router, useRouterHistory } from 'react-router'
import { createHashHistory } from 'history'
import { Provider } from 'react-redux'
import { syncHistoryWithStore } from 'react-router-redux'
import configureStore from './store/configureStore'
import routes from './app/routes'

const initialState = window.___INITIAL_STATE__
const browserHistory = useRouterHistory(createHashHistory)({ queryKey: false })
const store = configureStore(initialState, browserHistory)
const history = syncHistoryWithStore(browserHistory, store, {
  selectLocationState: (state) => state.router
})
history.listen(function (location) {
    window.ga('send', 'pageview', location.pathname);
})

ReactDOM.render(
    <Provider store={store}>
        <Router history={history} children={routes(store)} />
    </Provider>,
    document.getElementById('compat-app')
)
