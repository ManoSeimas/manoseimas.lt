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

function similarity (user_answers, fraction_answers) {
    let points = 0,
        answers_count = 0

    for (let answer_id in fraction_answers) {
        if (user_answers[answer_id]) {
            answers_count++
            points += Math.abs((user_answers[answer_id] + fraction_answers[answer_id]) / 2)
        }
    }

    return Math.round((points / answers_count)*100)
}

const Results = (props) =>
    <div>
        <h1>Results page for {props.title}</h1>
        <h2>My votes:</h2>
        <ul>
            {props.topics.map(topic => {
                return <li key={topic.id}>{topic.name} - {getAnswer(props.answers[topic.id])}</li>
            })}
        </ul>

        <h2>Results by fractions:</h2>
        <ul>
            {props.fractions.map(fraction => {
                return <li>{fraction.title} - {similarity(props.answers, fraction.answers)}%</li>
            })}
        </ul>
        <Link to='/'>Restart test</Link>
    </div>

Results.propTypes = {
  title: React.PropTypes.string,
  topics: React.PropTypes.array,
  answers: React.PropTypes.object,
  fractions: React.PropTypes.array
}

const mapStateToProps = (state) => ({
    title: state.test_state.title,
    topics: state.test_state.topics,
    answers: state.results.answers,
    fractions: state.results.fractions
})

export default connect((mapStateToProps), {})(Results)