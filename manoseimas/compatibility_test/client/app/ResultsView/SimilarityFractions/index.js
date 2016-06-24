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

const SimilarityFractions = ({user_answers, fractions}) =>
    <div>
        <div className={styles.note}>
            Kuo didesnis procentas, tuo labiau frakcija atitinka Jūsų pažiūras.
        </div>
        {fractions.map(fraction => {
            let similarity = calculate_similarity(user_answers, fraction.answers)
            return (
                <div className={styles.item}>
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
    </div>


SimilarityFractions.propTypes = {
  user_answers: React.PropTypes.object,
  fractions: React.PropTypes.array
}

export default SimilarityFractions