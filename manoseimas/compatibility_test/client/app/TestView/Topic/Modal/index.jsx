import React from 'react'
import styles from './styles.css'

const Modal = (props) =>
    <div className={styles.modal}>
        {props.children}
    </div>

Modal.propTypes = {
    children: React.PropTypes.element
}

export default Modal