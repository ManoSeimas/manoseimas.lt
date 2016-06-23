import React from 'react'
import styles from '../styles/components/tabs.css'

const Tabs = ({tabs, active, onClickHandler}) =>
    <div clasName={styles['tabs']}>
        {tabs.map(tab =>  <Tab key={tab.id} id={tab.id}
                               active={active === tab.id}
                               title={tab.title}
                               onClickHandler={onClickHandler} />)}
    </div>

Tabs.propTypes = {
    active: React.PropTypes.string,
    tabs: React.PropTypes.array.isRequired
}


const Tab = ({id, title, active, onClickHandler}) =>
    <div className={(active) ? styles['active-tab'] : styles['tab']}
         onClick={() => onClickHandler(id)}>{title}</div>

Tab.propTypes = {
    active: React.PropTypes.bool,
    title: React.PropTypes.string.isRequired
}

export default Tabs