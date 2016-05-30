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
    setActiveTopic: PropTypes.func.isRequired
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
    return <StartTest onClickHandler={this._openTopic} />
  }
}

const mapStateToProps = (state) => ({
    next_topic_id: state.test_state.next_topic_id
})

export default connect((mapStateToProps), {
    setActiveTopic
})(StartTestContainer)