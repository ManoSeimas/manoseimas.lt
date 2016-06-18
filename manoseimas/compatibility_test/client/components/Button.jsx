import React from 'react'
import styles from '../styles/components/button.css'

const Button = (props) => {
    const button_style = (props.type) ? 'button_' + props.type : 'button'
    return <div className={styles[button_style]} onClick={props.action}>
        {props.children}
    </div>
}

Button.propTypes = {
    action: React.PropTypes.func.isRequired,
    children: React.PropTypes.element,
    type: React.PropTypes.string
}

export default Button