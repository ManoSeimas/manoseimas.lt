import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import StartTest from './StartTest'
import { setActiveTopic } from '../../store/modules/test_state'

class StartTestContainer extends React.Component {

  constructor (props, context) {
    super(props)
    this._openTopic = this._openTopic.bind(this)
  }

  static propTypes = {
    next_topic: PropTypes.object.isRequired,
    topics_amount: PropTypes.number.isRequired,
    setActiveTopic: PropTypes.func.isRequired,
    title: PropTypes.string.isRequired,
    image: PropTypes.string
  }

  static contextTypes = {
    router: React.PropTypes.object
  }

  _openTopic() {
    const topicSlug = this.props.next_topic.slug
    this.props.setActiveTopic(topicSlug)
    this.context.router.push('/topic/' + topicSlug)
  }

  render () {
    return <StartTest onClickHandler={this._openTopic}
                      amount={this.props.topics_amount}
                      img_url={this.props.img_url}
                      title={this.props.title} />
  }
}

const mapStateToProps = (state) => ({
    next_topic: state.test_state.next_topic,
    topics_amount: state.test_state.topics.length,
    title: state.test_state.title,
    img_url: state.test_state.test_img
})

export default connect((mapStateToProps), {
    setActiveTopic
})(StartTestContainer)