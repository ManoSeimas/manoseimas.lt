import React from 'react'
import { SimilarityBar } from '../../../components'
import styles from '../../../styles/views/results.css'

function calculate_similarity (user_answers, fraction_answers) {
    let points = 0,
        answers_count = 0

    for (let answer_id in fraction_answers) {
        if (user_answers[answer_id]) {
            answers_count++
            points += Math.abs((user_answers[answer_id] + fraction_answers[answer_id]) / 2)
        }
    }

    return Math.round((points / answers_count)*100)
}

const SimilarityMps = ({user_answers, mps}) =>
    <div>
        <div className={styles.note}>
            Kuo didesnis procentas, tuo labiau Seimo narys atitinka Jūsų pažiūras.
        </div>
        {mps.map(mp => {
            let similarity = calculate_similarity(user_answers, mp.answers)
            return (
                <div className={styles.item}>
                    <div className={styles.img}>
                        <img src={mp.logo} alt={mp.title + ' logo'} />
                    </div>
                    <main>
                        <div className={styles.title}>{mp.name}, {mp.fraction}, {similarity}%</div>
                        <SimilarityBar similarity={similarity} />
                        <a href={'#' + mp.short_title}>
                            {mp.members_amount} nariai {' '}
                            <div className={styles.arrow}></div>
                        </a>
                    </main>
                </div>
            )
        })}
    </div>

SimilarityMps.propTypes = {
  user_answers: React.PropTypes.object,
  mps: React.PropTypes.array
}

export default SimilarityMps