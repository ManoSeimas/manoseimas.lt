import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import Topic from './Topic'
import { setActiveTopic,
         toggleArgumentsModal,
         toggleMoreModal,
         finishTest } from '../../store/modules/test_state'
import { saveAnswer } from '../../store/modules/results'


class TopicContainer extends React.Component {

    constructor (props, context) {
        super(props)
        this._setAnswer = this._setAnswer.bind(this)
        this._nextTopic = this._nextTopic.bind(this)
    }

    static propTypes = {
        next_topic: PropTypes.object.isRequired,
        setActiveTopic: PropTypes.func.isRequired,
        finishTest: PropTypes.func.isRequired,
        toggleArgumentsModal: PropTypes.func.isRequired,
        toggleMoreModal: PropTypes.func.isRequired,
        saveAnswer: PropTypes.func.isRequired,
        active_topic: PropTypes.object.isRequired,
        topics_amount: PropTypes.number.isRequired,
        params: React.PropTypes.object
    }

    static contextTypes = {
        router: React.PropTypes.object
    }

    componentWillReceiveProps(nextProps) {
        const topicSlug = nextProps.params.topicSlug
        if (Object.keys(nextProps.params).length === 0) {
            this.props.setActiveTopic()
        } else {
            if (!nextProps.active_topic || this.props.active_topic.slug !== topicSlug) {
                this.props.setActiveTopic(topicSlug)
            }
        }
    }

    _nextTopic () {
        const topicPosition = this.props.next_topic.position
        const topicSlug = this.props.next_topic.slug
        if (topicPosition <= this.props.topics_amount) {
            this.props.setActiveTopic(topicSlug)
            this.context.router.push('/topic/' + topicSlug)
        } else {
            this.props.finishTest()
            this.context.router.push('/results')
        }
    }

    _setAnswer (topic_id, answer) {
        if (topic_id && answer) {
            this.props.saveAnswer(topic_id, answer)
            this._nextTopic()
        } else {
            this._nextTopic()
        }
    }

    render () {
        const done_topics = (this.props.next_topic.position > 2) ? this.props.next_topic.position - 1 : 1
        if (this.props.active_topic) {
            return <Topic saveAnswer={this._setAnswer}
                          nextTopic={this._nextTopic}
                          toggleArguments={this.props.toggleArgumentsModal}
                          toggleDetails={this.props.toggleMoreModal}
                          topic={this.props.active_topic}
                          doneTopics={done_topics}
                          topicsAmount={this.props.topics_amount} />
        } else {
            return <div>Loading...</div>
        }
    }

}

const mapStateToProps = (state) => ({
    next_topic: state.test_state.next_topic,
    active_topic: state.test_state.active_topic,
    topics_amount: state.test_state.topics.length
})

export default connect((mapStateToProps), {
    setActiveTopic,
    finishTest,
    toggleArgumentsModal,
    toggleMoreModal,
    saveAnswer
})(TopicContainer)