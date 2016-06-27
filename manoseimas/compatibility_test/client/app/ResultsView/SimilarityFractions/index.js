import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import { subscribe } from 'subscribe-ui-event'
import { SimilarityBar, Checkbox } from '../../../components'
import { saveAnswer, getResults, toggleImportance, showHeader, hideHeader } from '../../../store/modules/results'
import SimilarityFractions from './SimilarityFractions'
import styles from '../../../styles/views/results.css'

class SimilarityFractionsContainer extends React.Component {

    static propTypes = {
      user_answers: PropTypes.object,
      fractions: PropTypes.array,
      topics: PropTypes.array,
      saveAnswer: PropTypes.func,
      getResults: PropTypes.func,
      toggleImportance: PropTypes.func,
      show_header: PropTypes.bool,
      showHeader: PropTypes.func,
      hideHeader: PropTypes.func
    }

    componentWillMount () {
        this.props.getResults()
    }

    getAnswer (topic_id) {
        if (this.props.user_answers[topic_id])
            return this.props.user_answers[topic_id].answer
        return undefined
    }

    render () {
        let {fractions, user_answers, topics, show_header} = this.props
        return (
            <div>
                <div className={styles.note}>
                    Kuo didesnis procentas, tuo labiau frakcija atitinka Jūsų pažiūras.
                </div>
                <SimilarityFractions user_answers={user_answers}
                                     fractions={fractions}
                                     show_header={show_header}
                                     showHeader={this.props.showHeader}
                                     hideHeader={this.props.hideHeader} />
                <div className={styles.topics}>
                    <h3>Interaktyvūs frakcijų rezultatai pagal klausimus</h3>
                    <div className={styles.note}>
                        Šioje rezultatų dalyje galite keisti savo atsakymus ir stebėti kaip keičiasi
                        rezultatai.
                    </div>
                    <ol>
                    {topics.map(topic => {
                        return <li key={topic.id}>
                            {topic.name} <br />
                            <Checkbox name={'topic'+topic.id}
                                      value={topic.id.toString()}
                                      actionHandler={() => this.props.toggleImportance(topic.id)}>šis klausimas man svarbus</Checkbox>

                            <div className={styles['similarity-bar']}>
                                <div className={styles.no}>PRIEŠ</div>
                                <div style={{width: '500px'}}>
                                    <div className={styles.line}></div>
                                    <div className={styles.actions}>
                                        <div className={styles.action}>
                                            <img src={(this.getAnswer(topic.id) < 0)
                                                        ? '/static/img/person-negative.png'
                                                        : '/static/img/person.png'}
                                                 onClick={() => this.props.saveAnswer(topic.id, -1)} />
                                        </div>
                                        <div className={styles.action}>
                                            <img src={(this.getAnswer(topic.id) === undefined)
                                                        ? '/static/img/person-active.png'
                                                        : '/static/img/person.png'}
                                                 onClick={() => this.props.saveAnswer(topic.id, undefined)} />
                                        </div>
                                        <div className={styles.action}>
                                            <img src={(this.getAnswer(topic.id) > 0)
                                                        ? '/static/img/person-positive.png'
                                                        : '/static/img/person.png'}
                                                 onClick={() => this.props.saveAnswer(topic.id, 1)} />
                                        </div>
                                    </div>
                                </div>
                                <div className={styles.yes}>UŽ</div>
                            </div>
                        </li>
                    })}
                    </ol>
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    user_answers: state.results.answers,
    fractions: state.results.fractions,
    topics: state.test_state.topics,
    show_header: state.results.show_header
})

export default connect((mapStateToProps), {
    saveAnswer,
    toggleImportance,
    getResults,
    showHeader,
    hideHeader
})(SimilarityFractionsContainer)
