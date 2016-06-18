import React from 'react'
import styles from '../styles/components/button.css'

const ButtonsBlock = (props) =>
    <div className={styles['button_block']}>
        {props.children}
    </div>

ButtonsBlock.propTypes = {
    children: React.PropTypes.element
}

export default ButtonsBlock