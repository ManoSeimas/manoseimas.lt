import React from 'react'
import styles from './styles.css'

const Modal = (props) =>
    <div className={styles.modal}>
        <div className={styles.header}>
             <h2>{props.title}</h2>
             <div className={styles.close}
                  onClick={props.closeModal}>X</div>
        </div>
        <div>{props.children}</div>
    </div>

Modal.propTypes = {
    title: React.PropTypes.string,
    closeModal: React.PropTypes.func,
    children: React.PropTypes.element
}

export default Modal