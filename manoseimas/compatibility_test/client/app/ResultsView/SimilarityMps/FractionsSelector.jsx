import React from 'react'
import styles from '../../../styles/views/results.css'

const FractionsSelector = ({fractions, selectFraction, selected_fractions}) =>
    <div className={styles['fractions-selector']}>
        {fractions.map(fraction => {
            if (fraction.members_amount > 0) {
                return <div className={styles.logo}>
                    <div className={styles.img}
                                key={'fraction-' + fraction.id}
                                style={(selected_fractions.indexOf(fraction.id) > -1)
                                        ? { border: '#646464 3px solid',
                                            width: '65px',
                                            height: '65px' }
                                        : undefined}>
                        <img src={fraction.logo}
                             alt={fraction.title + ' logo'}
                             onClick={() => selectFraction(fraction.id)} />
                    </div>
                    {(selected_fractions.indexOf(fraction.id) > -1)
                        ? <img src="/static/img/tick.png" className={styles.tick} />
                        : ''
                    }
                </div>
            }
        })}
    </div>

FractionsSelector.propTypes = {
    fractions: React.PropTypes.array,
    selected_fractions: React.PropTypes.array,
    selectFraction: React.PropTypes.func
}

export default FractionsSelector