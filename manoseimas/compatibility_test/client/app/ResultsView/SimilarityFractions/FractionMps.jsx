import React from 'react'
import styles from '../../../styles/views/results.css'
import { SimilarityBar } from '../../../components'


const FractionMps = ({mps, user_answers, showMoreMps}) =>
    <div className={styles.members}>
        {(mps.length < 5)
            ? mps.map(mp => {
                return <div className={styles.item} key={mp.id}>
                    <div className={styles.img}>
                        <img src={mp.logo} alt={mp.name + ' logo'} />
                    </div>
                    <main>
                        <div className={styles.title}>{mp.name}, {mp.fraction}, {mp.similarity}%</div>
                        <SimilarityBar similarity={mp.similarity} slim={true} />
                    </main>
                </div>
            })
            : [0, 1, mps.length-2, mps.length-1].map(item => {
                let mp = mps[item]
                return <div className={styles.item} key={mp.id}>
                    <div className={styles.img}>
                        <img src={mp.logo} alt={mp.name + ' logo'} />
                    </div>
                    <main>
                        <div className={styles.title}>{mp.name}, {mp.fraction}, {mp.similarity}%</div>
                        <SimilarityBar similarity={mp.similarity} slim={true} />
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
