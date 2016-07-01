import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import { Tabs } from '../../components'
import { setActiveTab } from '../../store/modules/results'

class ResultTabs extends React.Component {

    constructor (props, context) {
        super(props)
        this._setActiveTab = this._setActiveTab.bind(this)
    }

    static propTypes = {
        active_tab: PropTypes.string.isRequired,
        setActiveTab: PropTypes.func
    }

    static contextTypes = {
        router: React.PropTypes.object
    }

    _setActiveTab (id) {
        this.props.setActiveTab(id)
        if (id === 'mps') {
            this.context.router.push('/results/mps')
        } else {
            this.context.router.push('/results')
        }
    }

    render () {
        let tabs = [
            { id: 'fractions', title: 'Pagal frakcijas' },
            { id: 'mps', title: 'Pagal Seimo narius'}
        ]
        return <Tabs tabs={tabs}
                     active={this.props.active_tab}
                     onClickHandler={this._setActiveTab} />

    }
}

const mapStateToProps = (state) => ({
    active_tab: state.results.active_tab
})

export default connect((mapStateToProps), {
    setActiveTab,
})(ResultTabs)