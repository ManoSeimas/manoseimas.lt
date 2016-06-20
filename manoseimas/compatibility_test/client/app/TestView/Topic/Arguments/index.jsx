import React from 'react'
import styles from './styles.css'

const Arguments = (props) =>
    <div className={styles.arguments}>
        <div className={styles.box}>
            <div className={styles['positive-head']}>Už</div>
            {props.arguments.map(argument => {
                if (argument.supporting)
                    return <div className={styles.argument} key={argument.id}>
                            <h3>{argument.name}</h3>
                            <p>{argument.description}</p>
                        </div>
            })}
        </div>
        <div className={styles['negative-box']}>
            <div className={styles['negative-head']}>Prieš</div>
            {props.arguments.map(argument => {
                if (!argument.supporting)
                    return <div className={styles.argument} key={argument.id}>
                            <h3>{argument.name}</h3>
                            <p>{argument.description}</p>
                        </div>
            })}
        </div>
    </div>

Arguments.propTypes = {
    arguments: React.PropTypes.object.isRequired
}

export default Arguments