import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import Question from './Question'
import { setActiveQuestion } from '../../../store/modules/test_state'

class QuestionContainer extends React.Component {

  constructor (props, context) {
    super(props)
    this._openQuestion = this._openQuestion.bind(this)
  }

  static propTypes = {
    next_question_id: PropTypes.number.isRequired,
    setActiveQuestion: PropTypes.func.isRequired,
    active_question: PropTypes.object.isRequired,
    params: React.PropTypes.object
  }

  static contextTypes = {
    router: React.PropTypes.object
  }

  _openQuestion() {
    const questionId = this.props.next_question_id
    this.props.setActiveQuestion(questionId)
    console.log('XXX: ', '/question/' + questionId)
    this.context.router.push('/question/' + questionId)
  }

  render () {
    return <Question onClickHandler={this._openQuestion}
                     question={this.props.active_question} />
  }

}

const mapStateToProps = (state) => ({
    next_question_id: state.test_state.next_question_id,
    active_question: state.test_state.active_question
})

export default connect((mapStateToProps), {
    setActiveQuestion
})(QuestionContainer)