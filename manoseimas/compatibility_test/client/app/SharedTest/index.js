import React from 'react'
import ReactDOM from 'react-dom'
import StartTest from '../StartTest/StartTest'

let {test_id, topics, title} =  window.___INITIAL_STATE__

ReactDOM.render(
    <StartTest onClickHandler={() => window.open(`/test/${test_id}/#/topic/0`, '_self')}
               amount={topics.length}
               title={title} />,
    document.getElementById('shared-test-start')
)
