import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import { saveAnswer,
         getResults,
         toggleImportance,
         showHeader,
         hideHeader,
         expandFraction } from '../../../store/modules/results'
import SimilarityFractions from './SimilarityFractions'
import Topics from './Topics'
import styles from '../../../styles/views/results.css'

class SimilarityFractionsContainer extends React.Component {

    static propTypes = {
      user_answers: PropTypes.object,
      fractions: PropTypes.array,
      mps: PropTypes.array,
      topics: PropTypes.array,
      saveAnswer: PropTypes.func,
      getResults: PropTypes.func,
      toggleImportance: PropTypes.func,
      show_header: PropTypes.bool,
      showHeader: PropTypes.func,
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
        let {fractions, mps, user_answers, topics, show_header, expanded_fraction} = this.props
        return (
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
                                     showHeader={this.props.showHeader}
                                     hideHeader={this.props.hideHeader} />
                <Topics topics={topics}
                        fractions={fractions}
                        user_answers={user_answers}
                        toggleImportance={this.props.toggleImportance}
                        saveAnswer={this.props.saveAnswer} />
            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    user_answers: state.results.answers,
    fractions: state.results.fractions,
    mps: state.results.mps,
    topics: state.test_state.topics,
    show_header: state.results.show_header,
    expanded_fraction: state.results.expanded_fraction
})

export default connect((mapStateToProps), {
    saveAnswer,
    toggleImportance,
    getResults,
    showHeader,
    hideHeader,
    expandFraction
})(SimilarityFractionsContainer)
