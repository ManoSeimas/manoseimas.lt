import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import StartTest from './StartTest'
import { setActiveQuestion } from '../../../store/modules/test_state'

class StartTestContainer extends React.Component {

  constructor (props, context) {
    super(props)
    this._openQuestion = this._openQuestion.bind(this)
  }

  static propTypes = {
    next_question_id: PropTypes.number.isRequired,
    setActiveQuestion: PropTypes.func.isRequired
  }

  static contextTypes = {
    router: React.PropTypes.object
  }

  _openQuestion() {
    const questionId = this.props.next_question_id
    this.props.setActiveQuestion(questionId)
    this.context.router.push('/question/' + questionId)
  }

  render () {
    return <StartTest onClickHandler={this._openQuestion} />
  }

}

const mapStateToProps = (state) => ({
    next_question_id: state.test_state.next_question_id
})

export default connect((mapStateToProps), {
    setActiveQuestion
})(StartTestContainer)