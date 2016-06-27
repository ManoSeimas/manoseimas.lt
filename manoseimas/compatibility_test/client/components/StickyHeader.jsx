import React from 'react'
import styles from '../styles/components/sticky-header.css'

const StickyHeader = ({children, width}) =>
    <div className={styles['sticky-header']} style={(width) ? {width: width} : undefined}>
        {children}
    </div>

StickyHeader.propTypes = {
    children: React.PropTypes.element,
    widht: React.PropTypes.string
}

export default StickyHeader