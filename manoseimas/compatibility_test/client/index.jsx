import React from 'react'
import ReactDOM from 'react-dom'
import { Router, useRouterHistory } from 'react-router'
import { createHashHistory } from 'history'
import createStore from './store/createStore'
import AppContainer from './app/main'
import routes from './routes.jsx'

const history = useRouterHistory(createHashHistory)({ queryKey: false })
const initialState = window.___INITIAL_STATE__
const store = createStore(initialState)

ReactDOM.render(
    <AppContainer
        history={history}
        store={store}
        routes={routes(store)}
    />,
    document.getElementById('compat-app')
)
