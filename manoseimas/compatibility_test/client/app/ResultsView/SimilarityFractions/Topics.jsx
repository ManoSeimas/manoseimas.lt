import React from 'react'
import { Checkbox } from '../../../components'
import styles from '../../../styles/views/results.css'

function getAnswer (user_answers, topic_id) {
    if (user_answers[topic_id])
        return user_answers[topic_id].answer
    return undefined
}

const Topics = ({topics, toggleImportance, saveAnswer, user_answers}) =>
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
                          actionHandler={() => toggleImportance(topic.id)}>šis klausimas man svarbus</Checkbox>

                <div className={styles['similarity-bar']}>
                    <div className={styles.no}>PRIEŠ</div>
                    <div style={{width: '500px'}}>
                        <div className={styles.line}></div>
                        <div className={styles.actions}>
                            <div className={styles.action}>
                                <img src={(getAnswer(user_answers, topic.id) < 0)
                                            ? '/static/img/person-negative.png'
                                            : '/static/img/person.png'}
                                     onClick={() => saveAnswer(topic.id, -1)} />
                            </div>
                            <div className={styles.action}>
                                <img src={(getAnswer(user_answers, topic.id) === undefined)
                                            ? '/static/img/person-active.png'
                                            : '/static/img/person.png'}
                                     onClick={() => saveAnswer(topic.id, undefined)} />
                            </div>
                            <div className={styles.action}>
                                <img src={(getAnswer(user_answers, topic.id) > 0)
                                            ? '/static/img/person-positive.png'
                                            : '/static/img/person.png'}
                                     onClick={() => saveAnswer(topic.id, 1)} />
                            </div>
                        </div>
                    </div>
                    <div className={styles.yes}>UŽ</div>
                </div>
            </li>
        })}
        </ol>
    </div>

Topics.propTypes = {
  user_answers: React.PropTypes.object,
  topics: React.PropTypes.array,
  toggleImportance: React.PropTypes.func,
  saveAnswer: React.PropTypes.func
}

export default Topics