import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router'


const Results = (props) =>
    <div>
        <h1>Results page for {props.title}</h1>
        <Link to='/'>Restart test</Link>
    </div>

Results.propTypes = {
  title: React.PropTypes.string
}

const mapStateToProps = (state) => ({
    title: state.test_state.title
})

export default connect((mapStateToProps), {})(Results)