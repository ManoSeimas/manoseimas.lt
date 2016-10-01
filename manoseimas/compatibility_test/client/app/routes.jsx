import React from 'react'
import { IndexRoute, Route } from 'react-router'
import Layout from './layout'
import TopicView from './TopicView'
import StartTest from './StartTest'
import { ResultsLayout, SimilarityFractions, SimilarityMps, SimilarityTopics } from './ResultsView'

export default (store) => {
    return (
        <Route path="/" component={Layout}>
            <IndexRoute component={StartTest} />

            <Route path="/topic" component={TopicView} />
            <Route path="/topic/:topicSlug" component={TopicView} />
            <Route path="/results" component={ResultsLayout}>
                <IndexRoute component={SimilarityTopics} />
                <Route path="/results/fractions" component={SimilarityFractions} />
                <Route path="/results/mps" component={SimilarityMps} />
            </Route>
        </Route>
    )
}
