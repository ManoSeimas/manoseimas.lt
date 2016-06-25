import React from 'react'
import styles from '../styles/components/similarity-bar.css'

const SimilarityBar = ({similarity}) => {
    let color = '#00a162'
    if (similarity < 70)
        color = '#646464'
    if (similarity < 40)
        color = '#ca0837'

    return <div className={styles.bar}>
        <div style={{backgroundColor: color, width: similarity + '%'}}></div>
    </div>
}

SimilarityBar.propTypes = {
    similarity: React.PropTypes.number
}

export default SimilarityBar