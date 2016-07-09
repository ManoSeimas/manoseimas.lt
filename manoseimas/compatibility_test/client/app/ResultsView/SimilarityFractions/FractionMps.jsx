import React from 'react'
import styles from '../../../styles/views/results.css'
import { SimilarityBar } from '../../../components'


function calculate_similarity (user_answers, mp_answers) {
    let points = 0,
    answers_count = 0,
    answers = user_answers

    for (let answer_id in mp_answers) {
        if (answers[answer_id] && answers[answer_id].answer) {
            let answer_points = Math.abs((answers[answer_id].answer + Number(mp_answers[answer_id])) / 2)
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

const FractionMps = ({mps, user_answers, showMoreMps}) =>
    <div className={styles.members}>
        {(mps.length < 5)
            ? mps.map(mp => {
                let similarity = calculate_similarity(user_answers, mp.answers)
                return <div className={styles.item} key={mp.id}>
                    <div className={styles.img}>
                        <img src={mp.logo} alt={mp.name + ' logo'} />
                    </div>
                    <main>
                        <div className={styles.title}>{mp.name}, {mp.fraction}, {similarity}%</div>
                        <SimilarityBar similarity={similarity} slim={true} />
                    </main>
                </div>
            })
            : [0, 1, mps.length-2, mps.length-1].map(item => {
                let mp = mps[item]
                let similarity = calculate_similarity(user_answers, mp.answers)
                return <div className={styles.item} key={mp.id}>
                    <div className={styles.img}>
                        <img src={mp.logo} alt={mp.name + ' logo'} />
                    </div>
                    <main>
                        <div className={styles.title}>{mp.name}, {mp.fraction}, {similarity}%</div>
                        <SimilarityBar similarity={similarity} slim={true} />
                    </main>
                    {(item === 1)
                        ? <a className={styles.more} onClick={() => showMoreMps(mp.fraction_id)}>
                            Dar {mps.length - 4} nariai</a>
                        : ''
                    }
                </div>
            })
        }
    </div>

FractionMps.propTypes = {
    mps: React.PropTypes.array,
    user_answers: React.PropTypes.object,
    showMoreMps: React.PropTypes.func
}

export default FractionMps
