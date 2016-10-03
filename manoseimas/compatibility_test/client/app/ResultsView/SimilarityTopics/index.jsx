import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import { saveAnswer,
         getResults,
         toggleImportance } from '../../../store/modules/results'
import Topics from './Topics'
import Loader from 'react-loader'
import styles from '../../../styles/views/results.css'

class SimilarityTopicsContainer extends React.Component {

    static propTypes = {
      user_answers: PropTypes.object,
      fractions: PropTypes.array,
      mps: PropTypes.array,
      topics: PropTypes.array,
      saveAnswer: PropTypes.func,
      getResults: PropTypes.func,
      toggleImportance: PropTypes.func,
    }

    componentWillMount () {
        // Load test results if they are still not in redux store.
        if (!this.props.fractions.length){
            this.props.getResults()
        }
    }

    render () {
        let {fractions, user_answers, topics} = this.props
        return (
          <Loader loaded={fractions.length > 0}>
            <div>
                <Topics topics={topics}
                        fractions={fractions}
                        user_answers={user_answers}
                        toggleImportance={this.props.toggleImportance}
                        saveAnswer={this.props.saveAnswer} />
            </div>
          </Loader>
        )
    }
}

const mapStateToProps = (state) => ({
    user_answers: state.results.answers,
    fractions: state.results.fractions,
    mps: state.results.mps,
    topics: state.test_state.topics,
})

export default connect((mapStateToProps), {
    saveAnswer,
    toggleImportance,
    getResults,
})(SimilarityTopicsContainer)
