import React from 'react'
import { Checkbox, SimilarityWidget } from '../../../components'
import styles from '../../../styles/views/results.css'

const Topics = ({topics, fractions, toggleImportance, saveAnswer, user_answers}) =>
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
                <SimilarityWidget topic={topic}
                                  fractions={fractions}
                                  saveAnswer={saveAnswer}
                                  user_answers={user_answers} />
            </li>
        })}
        </ol>
    </div>

Topics.propTypes = {
  user_answers: React.PropTypes.object,
  fractions: React.PropTypes.array,
  topics: React.PropTypes.array,
  toggleImportance: React.PropTypes.func,
  saveAnswer: React.PropTypes.func
}

export default Topics