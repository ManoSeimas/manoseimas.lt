import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import { getResults,
         toggleImportance,
         showHeader,
         hideHeader,
         setTab,
         expandFraction } from '../../../store/modules/results'
import { setSelectedFractions } from '../../../store/modules/mps_state.js'
import SimilarityFractions from './SimilarityFractions'
import Loader from 'react-loader'
import styles from '../../../styles/views/results.css'

class SimilarityFractionsContainer extends React.Component {

    static propTypes = {
      user_answers: PropTypes.object,
      fractions: PropTypes.array,
      mps: PropTypes.array,
      getResults: PropTypes.func,
      toggleImportance: PropTypes.func,
      show_header: PropTypes.bool,
      showHeader: PropTypes.func,
      setTab: PropTypes.func,
      setSelectedFractions: PropTypes.func,
      hideHeader: PropTypes.func,
      expanded_fraction: PropTypes.number,
      expandFraction: PropTypes.func
    }

    componentWillMount () {
        // Load test results if they are still not in redux store.
        if (!this.props.fractions.length){
            this.props.getResults()
        }
    }

    render () {
        let {fractions, mps, user_answers, show_header, expanded_fraction} = this.props
        return (
          <Loader loaded={fractions.length > 0}>
            <div>
                <div className={styles.note}>
                    Kuo didesnis procentas, tuo labiau frakcija atitinka Jūsų pažiūras.
                </div>
                <SimilarityFractions user_answers={user_answers}
                                     fractions={fractions}
                                     mps={mps}
                                     expanded_fraction={expanded_fraction}
                                     show_header={show_header}
                                     expandFraction={this.props.expandFraction}
                                     setActiveTab={this.props.setTab}
                                     setSelectedFractions={this.props.setSelectedFractions}
                                     showHeader={this.props.showHeader}
                                     hideHeader={this.props.hideHeader} />
            </div>
          </Loader>
        )
    }
}

const mapStateToProps = (state) => ({
    user_answers: state.results.answers,
    fractions: state.results.fractions,
    mps: state.results.mps,
    show_header: state.results.show_header,
    expanded_fraction: state.results.expanded_fraction
})

export default connect((mapStateToProps), {
    toggleImportance,
    getResults,
    showHeader,
    hideHeader,
    expandFraction,
    setTab,
    setSelectedFractions
})(SimilarityFractionsContainer)
