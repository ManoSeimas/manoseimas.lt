import React from 'react'
import { StatusBar, TopicGroup, ButtonsBlock, Button } from '../../../components'
import Modal from './Modal'
import Arguments from './Arguments'
import MoreInfo from './MoreInfo'
import styles from '../../../styles/components/topic.css'

const Topic = (props) => {
    let topic_arguments = {}
    return <div>
        <header>
            <img src='/static/img/logo-black.png' className='logo' />
            <StatusBar current={props.doneTopics} max={props.topicsAmount} />
            <TopicGroup name={props.topic.group} number={'0' + props.doneTopics.toString()} />
        </header>

        <div className={styles.content}>
            <div className={styles.topic}>
                <div className={styles.text}>
                    <strong>{props.topic.name}</strong>
                </div>
                <div className={styles.actions}>
                    <div className={styles.absolute}>
                        <Button type='small'
                                action={props.toggleDetails}
                                arrow={true}>Daugiau informacijos</Button>
                        <Button type='small'
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

            <ButtonsBlock>
                <Button type={'yes'} action={props.onClickHandler}>Taip</Button>
                <Button type={'no'} action={props.onClickHandler}>Ne</Button>
                <Button type={'skip'} action={props.onClickHandler}>Praleisti</Button>
            </ButtonsBlock>
        </div>

        <div className={styles['context-image']}></div>
    </div>
}

Topic.propTypes = {
    topic: React.PropTypes.object,
    doneTopics: React.PropTypes.number,
    topicsAmount: React.PropTypes.number,
    onClickHandler: React.PropTypes.func,
    toggleArguments: React.PropTypes.func,
    toggleDetails: React.PropTypes.func,
}

export default Topic