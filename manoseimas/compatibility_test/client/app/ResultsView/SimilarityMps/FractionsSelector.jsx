import React from 'react'
import styles from '../../../styles/views/results.css'

const FractionsSelector = ({fractions, selectFraction, selected_fractions}) =>
    <div className={styles['fractions-selector']}>
        {fractions.map(fraction => {
            return <div className={styles.img}
                        key={'fraction-' + fraction.id}
                        style={(selected_fractions.indexOf(fraction.id) > -1)
                                ? {border: '#646464 2px solid'}
                                : undefined}>
                <img src={fraction.logo}
                     alt={fraction.title + ' logo'}
                     onClick={() => selectFraction(fraction.id)} />{fraction.id}
            </div>
        })}
    </div>

FractionsSelector.propTypes = {
    fractions: React.PropTypes.array,
    selected_fractions: React.PropTypes.array,
    selectFraction: React.PropTypes.func
}

export default FractionsSelector