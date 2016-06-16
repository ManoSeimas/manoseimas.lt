import React from 'react'

const Results = (props) =>
    <div>
        <Link to="/">Back</Link>
        <h1>Results page for {props.title}</h1>
    </div>

Results.propTypes = {
  title: React.PropTypes.string
}

export default Results