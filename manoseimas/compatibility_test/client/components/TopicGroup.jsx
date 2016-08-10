import React from 'react'
import styles from '../styles/components/topic_group.css'

const TopicGroup = (props) =>
    <div className={styles['topic-group']}>
       <div className={styles.number}>{props.number}</div>
       <div className={styles.name}>{props.name}</div>
    </div>

TopicGroup.propTypes = {
    number: React.PropTypes.string.isRequired,
    name: React.PropTypes.string
}

export default TopicGroup
