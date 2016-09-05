import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import Topic from './Topic'
import { setActiveTopic,
         toggleArgumentsModal,
         toggleMoreModal,
         finishTest } from '../../store/modules/test_state'
import { saveAnswer, toggleImportance } from '../../store/modules/results'


class TopicContainer extends React.Component {

    constructor (props, context) {
        super(props)
        this._setAnswer = this._setAnswer.bind(this)
        this._nextTopic = this._nextTopic.bind(this)
        this._toggleDetails = this._toggleDetails.bind(this)
        this._toggleArguments = this._toggleArguments.bind(this)
    }

    static propTypes = {
        next_topic: PropTypes.object.isRequired,
        setActiveTopic: PropTypes.func.isRequired,
        finishTest: PropTypes.func.isRequired,
        toggleArgumentsModal: PropTypes.func.isRequired,
        toggleMoreModal: PropTypes.func.isRequired,
        toggleImportance: PropTypes.func.isRequired,
        saveAnswer: PropTypes.func.isRequired,
        active_topic: PropTypes.object.isRequired,
        topics_amount: PropTypes.number.isRequired,
        answers: PropTypes.object.isRequired,
        params: React.PropTypes.object
    }

    static contextTypes = {
        router: React.PropTypes.object
    }

    componentWillReceiveProps(nextProps) {
        const new_slug = nextProps.params.topicSlug
        if (new_slug !== this.props.params.topicSlug && nextProps.active_topic.slug !== new_slug) {
            this.props.setActiveTopic(new_slug)
        }
    }

    componentWillMount() {
        const topicSlug = this.props.params.topicSlug
        if (Object.keys(this.props.params).length === 0) {
            this.props.setActiveTopic()
        } else {
            if (!this.props.active_topic || this.props.active_topic.slug !== topicSlug) {
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

    _toggleDetails () {
        // Track click in Google Analytics
        window.ga('send', 'event', {
            eventCategory: 'Toggle Details',
            eventAction: 'click',
            eventLabel: this.props.active_topic.slug
        })
        this.props.toggleMoreModal()
    }

    _toggleArguments () {
        // Track click in Google Analytics
        window.ga('send', 'event', {
            eventCategory: 'Toggle Arguments',
            eventAction: 'click',
            eventLabel: this.props.active_topic.slug
        })
        this.props.toggleArgumentsModal()
    }

    render () {
        const done_topics = (this.props.next_topic.position > 2) ? this.props.next_topic.position - 1 : 1
        if (this.props.active_topic && this.props.active_topic.id) {
            return <Topic saveAnswer={this._setAnswer}
                          nextTopic={this._nextTopic}
                          toggleArguments={this._toggleArguments}
                          toggleDetails={this._toggleDetails}
                          toggleImportance={this.props.toggleImportance}
                          topic={this.props.active_topic}
                          doneTopics={done_topics}
                          topicsAmount={this.props.topics_amount}
                          answers={this.props.answers} />
        } else {
            return <div>Loading...</div>
        }
    }

}

const mapStateToProps = (state) => ({
    next_topic: state.test_state.next_topic,
    active_topic: state.test_state.active_topic,
    topics_amount: state.test_state.topics.length,
    answers: state.results.answers
})

export default connect((mapStateToProps), {
    setActiveTopic,
    finishTest,
    toggleArgumentsModal,
    toggleMoreModal,
    toggleImportance,
    saveAnswer
})(TopicContainer)