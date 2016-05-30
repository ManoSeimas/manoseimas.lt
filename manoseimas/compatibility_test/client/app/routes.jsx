import React from 'react'
import { IndexRoute, Route } from 'react-router'
import Layout from './layout'
import { StartTest, Question } from './TestView'

export default (store) => {
    /**
     * Please keep routes in alphabetical order
     */

    let compo = <div>Hello J</div>
    return (
        <Route path="/" component={Layout}>
            <IndexRoute component={StartTest} />

            <Route path="/question" component={Question} />
            <Route path="/question/:questionId" component={Question} />
        </Route>
    )
}
