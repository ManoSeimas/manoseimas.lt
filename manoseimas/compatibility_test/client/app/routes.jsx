import React from 'react'
import { IndexRoute, Route } from 'react-router'
import Layout from './layout'
import { StartTest, Topic } from './TestView'

export default (store) => {
    return (
        <Route path="/" component={Layout}>
            <IndexRoute component={StartTest} />

            <Route path="/topic" component={Topic} />
            <Route path="/topic/:topicId" component={Topic} />
        </Route>
    )
}
