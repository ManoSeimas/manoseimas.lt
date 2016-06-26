import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import { SimilarityBar, Checkbox } from '../../../components'
import { saveAnswer, getResults, toggleImportance } from '../../../store/modules/results'

import styles from '../../../styles/views/results.css'

class SimilarityFractions extends React.Component {

    static propTypes = {
      user_answers: PropTypes.object,
      fractions: PropTypes.array,
      topics: PropTypes.array,
      saveAnswer: PropTypes.func,
      getResults: PropTypes.func,
      toggleImportance: PropTypes.func
    }

    componentWillMount () {
        this.props.getResults()
    }

    calculate_similarity (fraction_answers) {
        let points = 0,
            answers_count = 0,
            answers = this.props.user_answers

        for (let answer_id in fraction_answers) {
            if (answers[answer_id] && answers[answer_id].answer) {
                let answer_points = Math.abs((answers[answer_id].answer + fraction_answers[answer_id]) / 2)
                if (answers[answer_id].important) {
                    answers_count += 2
                    answer_points *= 2
                } else {
                    answers_count++
                }
                points += answer_points
            }
        }

        return Math.round((points / answers_count)*100)
    }

    getAnswer (topic_id) {
        if (this.props.user_answers[topic_id])
            return this.props.user_answers[topic_id].answer
        return undefined
    }

    render () {
        let {fractions, user_answers, topics} = this.props
        return (
            <div>
                <div className={styles.note}>
                    Kuo didesnis procentas, tuo labiau frakcija atitinka Jūsų pažiūras.
                </div>
                {fractions.map(fraction => {
                    let similarity = this.calculate_similarity(fraction.answers)
                    return (
                        <div className={styles.item} key={fraction.short_title}>
                            <div className={styles.img}>
                                <img src={fraction.logo} alt={fraction.title + ' logo'} />
                            </div>
                            <main>
                                <div className={styles.title}>{fraction.title}, {similarity}%</div>
                                <SimilarityBar similarity={similarity} />
                                <a href={'#' + fraction.short_title}>
                                    {fraction.members_amount} nariai {' '}
                                    <div className={styles.arrow}></div>
                                </a>
                            </main>
                        </div>
                    )
                })}
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
    topics: state.test_state.topics
})

export default connect((mapStateToProps), {
    saveAnswer,
    toggleImportance,
    getResults
})(SimilarityFractions)
