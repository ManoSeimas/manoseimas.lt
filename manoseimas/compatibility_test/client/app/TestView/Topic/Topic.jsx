import React from 'react'
import { StatusBar, TopicGroup, ButtonsBlock, Button } from '../../../components'
import styles from '../../../styles/base.css'

const Topic = (props) =>
    <div>
        <header>
            <img src='/static/img/logo-black.png' className='logo' />
            <StatusBar current={props.doneTopics} max={props.topicsAmount} />
            <TopicGroup name={props.topic.group} number={'0' + props.doneTopics} />
        </header>

        <div className={styles.content}>
            <div className={styles.text}>
                <strong>{props.topic.name}</strong>
            </div>
            <ButtonsBlock>
                <Button type={'yes'} action={props.onClickHandler}>Taip</Button>
                <Button type={'no'} action={props.onClickHandler}>Ne</Button>
                <Button type={'skip'} action={props.onClickHandler}>Praleisti</Button>
            </ButtonsBlock>
        </div>

        <div className={styles['context-image']}></div>
    </div>

Topic.propTypes = {
  topic: React.PropTypes.object,
  doneTopics: React.PropTypes.string,
  topicsAmount: React.PropTypes.number,
  onClickHandler: React.PropTypes.func
}

export default Topic