import React from 'react'
import { connect } from 'react-redux'
import { SimilarityBar } from '../../../components'
import styles from '../../../styles/views/results.css'


class SimilarityMps extends React.Component {

    static propTypes = {
      user_answers: React.PropTypes.object,
      mps: React.PropTypes.array
    }

    calculate_similarity (user_answers, fraction_answers) {
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

    render () {
        let {user_answers, mps} = this.props
        return (
            <div>
                <div className={styles.note}>
                    Kuo didesnis procentas, tuo labiau Seimo narys atitinka Jūsų pažiūras.
                </div>
                {mps.map(mp => {
                    let similarity = this.calculate_similarity(user_answers, mp.answers)
                    return (
                        <div className={styles.item} key={mp.id}>
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
        )
    }
}

const mapStateToProps = (state) => ({
    user_answers: state.results.answers,
    mps: state.results.mps
})

export default connect((mapStateToProps), {})(SimilarityMps)
