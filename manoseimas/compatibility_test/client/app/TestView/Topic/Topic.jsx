import React from 'react'
import { Link } from 'react-router'
import { StatusBar, TopicGroup } from '../../../components'

const Topic = (props) =>
    <div>
        <header>
            <img src='/static/img/logo-black.png' className='logo' />
            <StatusBar current={props.doneTopics} max={props.topicsAmount} />
            <TopicGroup name={props.topic.group} number={'0' + props.doneTopics} />
        </header>

        <div>
          Topic {props.topic.name} - {props.topic.description}
          <a className='button' onClick={props.onClickHandler}>Toliau</a>
        </div>
    </div>

Topic.propTypes = {
  topic: React.PropTypes.object,
  doneTopics: React.PropTypes.string,
  topicsAmount: React.PropTypes.number,
  onClickHandler: React.PropTypes.func
}

export default Topic