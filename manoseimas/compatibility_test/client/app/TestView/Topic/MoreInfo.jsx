import React from 'react'

const MoreInfo = (props) =>
    <div>{props.description}</div>

MoreInfo.propTypes = {
    description: React.PropTypes.string
}

export default MoreInfo