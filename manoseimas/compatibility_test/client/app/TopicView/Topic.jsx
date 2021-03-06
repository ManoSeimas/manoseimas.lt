import React from 'react'
import { StatusBar, TopicGroup, ButtonsBlock, Button, Checkbox } from '../../components'
import Arguments from './Arguments'
import Modal from './Modal'
import MoreInfo from './MoreInfo'
import styles from '../../styles/views/topic.css'

const Topic = (props) => {
    const zero = (props.doneTopics < 10) ? '0' : ''
    const answer = props.answers[props.topic.id]
    return <div>
        <header>
            <a href="/">
                <img src='/static/img/logo-black.png' className='logo' />
            </a>
            <StatusBar current={props.doneTopics} max={props.topicsAmount} />
            <TopicGroup name={props.topic.group} number={zero + props.doneTopics.toString()} />
        </header>

        <div className={styles.content}>
            <div className={styles.topic}>
                <div className={styles.text}>
                    <strong>{props.topic.name}</strong>
                </div>
                <div className={styles.actions}>
                    <div className={styles.relative}>
                        <Button type='small'
                                active={props.topic.more_modal}
                                action={props.toggleDetails}
                                arrow={true}>Daugiau informacijos</Button>
                        <Button type='small'
                                active={props.topic.arguments_modal}
                                action={props.toggleArguments}
                                arrow={true}>Padėkite apsispręsti</Button>
                    </div>
                    {(props.topic.more_modal)
                        ? <Modal title='Daugiau informacijos' closeModal={props.toggleDetails}>
                              <MoreInfo description={props.topic.description} />
                          </Modal>
                        : ''
                    }
                    {(props.topic.arguments_modal)
                        ? <Modal title='Padėkite apsispręsti' closeModal={props.toggleArguments}>
                              <Arguments arguments={props.topic.arguments} />
                          </Modal>
                        : ''
                    }
                </div>
            </div>

            <Checkbox name={'topic'+props.topic.id}
                      value={props.topic.id.toString()}
                      checked={(answer) ? answer.important : false}
                      actionHandler={() => props.toggleImportance(props.topic.id)}>
                Šis klausimas man svarbus
            </Checkbox>

            <ButtonsBlock>
                <Button type='yes'
                        action={() => props.saveAnswer(props.topic.id, 2)}>Taip</Button>
                <Button type='no'
                        action={() => props.saveAnswer(props.topic.id, -2)}>Ne</Button>
                <Button type='skip' action={props.nextTopic}>Praleisti</Button>
            </ButtonsBlock>


        </div>

        <div className={styles['topic-image']}>
            {(props.topic.image)
                ? <img src={props.topic.image} alt='topic image' />
                : undefined}
        </div>
    </div>
}

Topic.propTypes = {
    answers: React.PropTypes.object,
    topic: React.PropTypes.object,
    doneTopics: React.PropTypes.number,
    topicsAmount: React.PropTypes.number,
    saveAnswer: React.PropTypes.func,
    nextTopic: React.PropTypes.func,
    toggleArguments: React.PropTypes.func,
    toggleDetails: React.PropTypes.func,
    toggleImportance: React.PropTypes.func
}

export default Topic