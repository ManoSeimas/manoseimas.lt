import React from 'react'
import styles from '../styles/components/block.css'

const Block = (props) =>
    <div className={styles.instruction}>
        <div className={styles.number}>{props.number}</div>
        <div className={styles.text}>
            {props.children}
        </div>
    </div>

Block.propTypes = {
    number: React.PropTypes.number.isRequired,
    children: React.PropTypes.element
}

export default Block