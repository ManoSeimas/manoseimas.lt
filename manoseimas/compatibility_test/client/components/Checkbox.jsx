import React from 'react'
import styles from '../styles/components/checkbox.css'

const Checkbox = ({name, value, checked, actionHandler, children}) =>
    <div>
        <input type='checkbox'
               name={name}
               id={name}
               checked={checked}
               value={value} />
        <label htmlFor={name}
               className={styles.checkbox}
               onClick={actionHandler}>{children}</label>
    </div>

Checkbox.propTypes = {
    actionHandler: React.PropTypes.func,
    name: React.PropTypes.string.isRequired,
    value: React.PropTypes.string.isRequired,
    children: React.PropTypes.string
}

export default Checkbox