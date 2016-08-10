import React from 'react'
import styles from '../styles/components/similarity-bar.css'

const SimilarityBar = ({similarity, slim}) => {
    let color = '#0A9955'
    if (similarity < 90)
        color = '#248F5C'
    if (similarity < 80)
        color = '#3E8664'
    if (similarity < 70)
        color = '#587C6B'
    if (similarity < 60)
        color = '#737373'
    if (similarity < 50)
        color = '#885864'
    if (similarity < 40)
        color = '#9E3D55'
    if (similarity < 30)
        color = '#B42246'
    if (similarity < 20)
        color = '#CA0837'

    let bar_style = 'bar'
    if (slim)
        bar_style = 'slim-bar'

    return <div className={styles[bar_style]}>
        <div style={{backgroundColor: color, width: similarity + '%'}}></div>
    </div>
}

SimilarityBar.propTypes = {
    similarity: React.PropTypes.number,
    slim: React.PropTypes.bool
}

export default SimilarityBar