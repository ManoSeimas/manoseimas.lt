import React from 'react'
import { Link } from 'react-router'

const Topic = (props) =>
    <div>
        <Link to="/">Back</Link>
        <div>
          Topic {props.topic.name} - {props.topic.description}
          <a className='button' onClick={props.onClickHandler}>Toliau</a>
        </div>
    </div>

Topic.propTypes = {
  topic: React.PropTypes.object,
  onClickHandler: React.PropTypes.func
}

export default Topic