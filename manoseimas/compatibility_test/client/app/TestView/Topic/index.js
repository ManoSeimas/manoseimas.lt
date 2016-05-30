import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import Topic from './Topic'
import { setActiveTopic } from '../../../store/modules/test_state'

class TopicContainer extends React.Component {

  constructor (props, context) {
    super(props)
    this._openTopic = this._openTopic.bind(this)
  }

  static propTypes = {
    next_topic_id: PropTypes.number.isRequired,
    setActiveTopic: PropTypes.func.isRequired,
    active_topic: PropTypes.object.isRequired,
    params: React.PropTypes.object
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
    return <Topic onClickHandler={this._openTopic}
                  topic={this.props.active_topic} />
  }

}

const mapStateToProps = (state) => ({
    next_topic_id: state.test_state.next_topic_id,
    active_topic: state.test_state.active_topic
})

export default connect((mapStateToProps), {
    setActiveTopic
})(TopicContainer)