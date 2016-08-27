import React from 'react'
import { connect } from 'react-redux'
import { expandTopics, selectFraction, showAllMps } from '../../../store/modules/mps_state'
import { getResults, setTab, saveAnswer } from '../../../store/modules/results'
import FractionsSelector from './FractionsSelector'
import ListOfMps from './ListOfMps'
import Loader from 'react-loader'
import styles from '../../../styles/views/results.css'

class SimilarityMps extends React.Component {

    static propTypes = {
      user_answers: React.PropTypes.object,
      mps: React.PropTypes.array,
      fractions: React.PropTypes.array,
      topics: React.PropTypes.array,
      expanded_mp: React.PropTypes.number,
      selected_fractions: React.PropTypes.array,
      expandTopics: React.PropTypes.func,
      getResults: React.PropTypes.func,
      saveAnswer: React.PropTypes.func,
      setTab: React.PropTypes.func,
      selectFraction: React.PropTypes.func,
      show_all_mps: React.PropTypes.bool
    }

    componentWillMount () {
        // Load test results if they are still not in redux store.
        if (!this.props.mps.length){
            this.props.getResults()
        }
        this.props.setTab('mps')
    }

    render () {
        const {
            selected_fractions,
            user_answers,
            mps,
            fractions,
            topics,
            expanded_mp,
            show_all_mps
        } = this.props
        return (
            <Loader loaded={mps.length > 0}>
                <div>
                    <div className={styles.note}>
                        Pasirinkite dominančias frakcijas (galima rinktis kelias iš karto):
                    </div>
                    <FractionsSelector fractions={fractions}
                                       selected_fractions={selected_fractions}
                                       selectFraction={this.props.selectFraction} />
                    <ListOfMps mps={mps}
                               fractions={fractions}
                               topics={topics}
                               expanded_mp={expanded_mp}
                               expandTopics={this.props.expandTopics}
                               showAllMps={this.props.showAllMps}
                               show_all_mps={show_all_mps}
                               selected_fractions={selected_fractions}
                               user_answers={user_answers} />
                </div>
            </Loader>
        )
    }
}

const mapStateToProps = (state) => ({
    user_answers: state.results.answers,
    topics: state.test_state.topics,
    mps: state.results.mps,
    fractions: state.results.fractions,
    selected_fractions: state.mps_state.selected_fractions,
    expanded_mp: state.mps_state.expanded_mp,
    show_all_mps: state.mps_state.show_all_mps
})

export default connect((mapStateToProps), {
    expandTopics,
    getResults,
    saveAnswer,
    setTab,
    selectFraction,
    showAllMps
})(SimilarityMps)
