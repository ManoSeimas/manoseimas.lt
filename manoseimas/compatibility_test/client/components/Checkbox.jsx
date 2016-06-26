import React from 'react'
import styles from '../styles/components/checkbox.css'

const Checkbox = ({name, value, actionHandler, children}) =>
    <div onClick={actionHandler}>
        <input type='checkbox'
               name={name}
               id={name}
               value={value} />
        <label htmlFor={name}
               className={styles.checkbox}>{children}</label>
    </div>

Checkbox.propTypes = {
    actionHandler: React.PropTypes.func,
    name: React.PropTypes.string.isRequired,
    value: React.PropTypes.string.isRequired,
    children: React.PropTypes.string
}

export default Checkbox