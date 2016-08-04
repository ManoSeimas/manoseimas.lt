import React from 'react'
import styles from '../styles/components/similarity-bar.css'

const SimilarityBar = ({similarity, slim}) => {
    let color = '#00a162'
    if (similarity < 60)
        color = '#646464'
    if (similarity < 40)
        color = '#ca0837'

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