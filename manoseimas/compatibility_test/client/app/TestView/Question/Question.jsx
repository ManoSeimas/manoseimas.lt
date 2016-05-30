import React from 'react'
import { Link } from 'react-router'

const Question = (props) =>
    <div>
        <Link to="/">Back</Link>
        <div>
          Question {props.question.id} - {props.question.title}
          <a className='button' onClick={props.onClickHandler}>Toliau</a>
        </div>
    </div>

Question.propTypes = {
  question: React.PropTypes.object,
  onClickHandler: React.PropTypes.func
}

export default Question