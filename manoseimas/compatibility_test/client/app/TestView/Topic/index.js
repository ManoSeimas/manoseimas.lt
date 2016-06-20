import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import Topic from './Topic'
import { setActiveTopic,
         finishTest,
         toggleArgumentsModal,
         toggleMoreModal } from '../../../store/modules/test_state'

class TopicContainer extends React.Component {

    constructor (props, context) {
        super(props)
        this._openTopic = this._openTopic.bind(this)
    }

    static propTypes = {
        next_topic_id: PropTypes.number.isRequired,
        setActiveTopic: PropTypes.func.isRequired,
        finishTest: PropTypes.func.isRequired,
        toggleArgumentsModal: PropTypes.func.isRequired,
        toggleMoreModal: PropTypes.func.isRequired,
        active_topic: PropTypes.object.isRequired,
        topics_amount: PropTypes.number.isRequired,
        params: React.PropTypes.object
    }

    static contextTypes = {
        router: React.PropTypes.object
    }

    _openTopic () {
        const topicId = this.props.next_topic_id
        if (topicId < this.props.topics_amount) {
            this.props.setActiveTopic(topicId)
            this.context.router.push('/topic/' + topicId)
        } else {
            this.props.finishTest()
            this.context.router.push('/results')
        }
    }

    render () {
        return <Topic onClickHandler={this._openTopic}
                      toggleArguments={this.props.toggleArgumentsModal}
                      toggleDetails={this.props.toggleMoreModal}
                      topic={this.props.active_topic}
                      doneTopics={this.props.next_topic_id}
                      topicsAmount={this.props.topics_amount} />
    }

}

const mapStateToProps = (state) => ({
    next_topic_id: state.test_state.next_topic_id,
    active_topic: state.test_state.active_topic,
    topics_amount: state.test_state.topics.length
})

export default connect((mapStateToProps), {
    setActiveTopic,
    finishTest,
    toggleArgumentsModal,
    toggleMoreModal
})(TopicContainer)