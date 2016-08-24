import React from 'react'
import styles from '../styles/components/button.css'

const Button = (props) => {
    const button_style = (props.type) ? 'button_' + props.type : 'button'
    const active = (props.active) ? 'active' : undefined
    const arrow = (props.arrow) ? <div className={styles.arrow}></div> : undefined
    return (
        <div className={`${styles[button_style]} ${styles[active]}`} onClick={props.action}>
            <div>{props.children}</div>
            {arrow}
        </div>
    )
}

Button.propTypes = {
    action: React.PropTypes.func,
    children: React.PropTypes.string,
    type: React.PropTypes.string,
    arrow: React.PropTypes.bool,
    active: React.PropTypes.bool
}

export default Button