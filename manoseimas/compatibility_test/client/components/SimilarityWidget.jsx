import React from 'react'
import styles from '../styles/components/similarity-widget.css'

function getAnswer (user_answers, topic_id) {
    if (user_answers[topic_id])
        return user_answers[topic_id].answer
    return undefined
}

function make_procental_answer (answer) {
    // -1p = 0%     (-1 + 1) * 50 => 0
    //  0p = 50%     (0 + 1) * 50 => 50
    //  1p = 100%    (1 + 1) * 50 => 100
    return Math.round((answer + 1)*50)
}

const SimilarityWidget = ({topic, items, user_answers, saveAnswer}) =>
    <div className={styles['similarity-widget']}>
        <div className={styles.no}>PRIEŠ</div>
        <div className={styles.middle}>
            {items.map(item => {
                let item_answer = make_procental_answer(item.answers[topic.id])
                return (
                    <div className={styles.img} style={{left: item_answer * 5}} key={'item-' + item.id}>
                        <img src={item.logo} alt={item.title + ' logo'} />
                    </div>
                )
            })}
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


SimilarityWidget.propTypes = {
    topic: React.PropTypes.object.isRequired,
    items: React.PropTypes.array.isRequired,
    user_answers: React.PropTypes.object.isRequired,
    saveAnswer: React.PropTypes.func
}

export default SimilarityWidget