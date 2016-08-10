import React from 'react'

const MoreInfo = (props) =>
    <div dangerouslySetInnerHTML={{__html:props.description}} />

MoreInfo.propTypes = {
    description: React.PropTypes.string
}

export default MoreInfo