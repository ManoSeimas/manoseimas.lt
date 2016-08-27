import React from 'react'
import styles from '../styles/components/block.css'

const Block = (props) =>
    <div className={(props.desktopOnly) ? styles['instruction-no-mobile'] : styles.instruction}>
        <div className={styles.number}>{props.number}</div>
        <div className={styles.text} style={props.style}>
            {props.children}
        </div>
    </div>

Block.propTypes = {
    number: React.PropTypes.number.isRequired,
    children: React.PropTypes.element
}

export default Block