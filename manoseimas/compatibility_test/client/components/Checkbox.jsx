import React from 'react'
import styles from '../styles/components/checkbox.css'

const Checkbox = ({name, value, checked, actionHandler, children}) =>
    <div>
        <input type='checkbox'
               name={name}
               id={name}
               value={value}
               checked={checked}
               onChange={actionHandler} />
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