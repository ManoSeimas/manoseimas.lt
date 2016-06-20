import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router'

function getAnswer (answer) {
    answer = (answer) ? answer.toString() : '0'
    switch (answer) {
        case '1':
            return 'taip'
        case '-1':
            return 'ne'
        default:
            return 'praleista'
    }
}

const Results = (props) =>
    <div>
        <h1>Results page for {props.title}</h1>
        <ul>
            {props.topics.map(topic => {
                return <li key={topic.id}>{topic.name} - {getAnswer(props.answers[topic.id])}</li>
            })}
        </ul>
        <Link to='/'>Restart test</Link>
    </div>

Results.propTypes = {
  title: React.PropTypes.string,
  topics: React.PropTypes.array,
  answers: React.PropTypes.object
}

const mapStateToProps = (state) => ({
    title: state.test_state.title,
    topics: state.test_state.topics,
    answers: state.results.answers
})

export default connect((mapStateToProps), {})(Results)