import React from 'react'
import { IndexRoute, Route } from 'react-router'
import Layout from './layout'
import { StartTest, Topic } from './TestView'
import ResultsLayout from './ResultsView'
import SimilarityFractions from './ResultsView/SimilarityFractions'
import SimilarityMps from './ResultsView/SimilarityMps'

export default (store) => {
    return (
        <Route path="/" component={Layout}>
            <IndexRoute component={StartTest} />

            <Route path="/topic" component={Topic} />
            <Route path="/topic/:topicId" component={Topic} />
            <Route path="/results" component={ResultsLayout}>
                <IndexRoute component={SimilarityFractions} />
                <Route path="/results/mps" component={SimilarityMps} />
            </Route>
        </Route>
    )
}
