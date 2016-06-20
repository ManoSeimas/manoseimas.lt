import React from 'react'
import styles from '../styles/components/status_bar.css'

const StatusBar = (props) => {

    function steps () {
        let steps = []
        for (let i=0; i < props.max; i++) {
           let class_name = styles.step
           if (i < props.current)
               class_name = styles['active-step']
           steps.push(<div className={class_name} key={i}></div>)
        }
        return steps
    }

    return <div className={styles['question-steps']}>{steps()}</div>
}

StatusBar.propTypes = {
    max: React.PropTypes.number.isRequired,
    current: React.PropTypes.number.isRequired
}

export default StatusBar