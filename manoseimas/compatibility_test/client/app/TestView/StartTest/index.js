import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import StartTest from './StartTest'
import { setActiveTopic } from '../../../store/modules/test_state'

class StartTestContainer extends React.Component {

  constructor (props, context) {
    super(props)
    this._openTopic = this._openTopic.bind(this)
  }

  static propTypes = {
    next_topic_id: PropTypes.number.isRequired,
    topics_amount: PropTypes.number.isRequired,
    setActiveTopic: PropTypes.func.isRequired,
    title: PropTypes.string.isRequired
  }

  static contextTypes = {
    router: React.PropTypes.object
  }

  _openTopic() {
    const topicId = this.props.next_topic_id
    this.props.setActiveTopic(topicId)
    this.context.router.push('/topic/' + topicId)
  }

  render () {
    return <StartTest onClickHandler={this._openTopic}
                      amount={this.props.topics_amount}
                      title={this.props.title} />
  }
}

const mapStateToProps = (state) => ({
    next_topic_id: state.test_state.next_topic_id,
    topics_amount: state.test_state.topics.length,
    title: state.test_state.title
})

export default connect((mapStateToProps), {
    setActiveTopic
})(StartTestContainer)