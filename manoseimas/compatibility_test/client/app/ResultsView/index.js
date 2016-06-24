import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router'
import { setActiveTab } from '../../store/modules/results'
import { Tabs, StatusBar } from '../../components'
import SimilarityFractions from './SimilarityFractions'
import SimilarityMps from './SimilarityMps'
import styles from '../../styles/views/results.css'


class ResultsView extends React.Component {

    static propTypes = {
        active_tab: PropTypes.string.isRequired,
        setActiveTab: PropTypes.func.isRequired,
        answers: PropTypes.object,
        fractions: PropTypes.array,
        mps: PropTypes.array
    }

    getAnswer (answer) {
        answer = (answer) ? answer.toString() : '0'
        switch (answer) {
            case '1':
                return 'taip'
            case '-1':
                return 'ne'
            default:
                return 'praleista'
        }
    }

    render () {
        let tabs = [
            { id: 'fractions', title: 'Pagal frakcijas' },
            { id: 'mps', title: 'Pagal Seimo narius'}
        ]

        return (
            <div>
                <header>
                    <img src='/static/img/logo-black.png' className='logo' />
                    <StatusBar current={10} max={10} />
                </header>

                <div className={styles.content}>
                    <h2 className='title'>Rezultatai</h2>
                    <Tabs tabs={tabs} active={this.props.active_tab} onClickHandler={this.props.setActiveTab} />
                    {(this.props.active_tab === 'fractions')
                        ? <SimilarityFractions fractions={this.props.fractions} user_answers={this.props.answers} />
                        : <SimilarityMps mps={this.props.mps} user_answers={this.props.answers} />
                    }

                    <h2>My votes:</h2>
                    <ul>
                        {this.props.topics.map(topic => {
                            return <li key={topic.id}>{topic.name} - {this.getAnswer(this.props.answers[topic.id])}</li>
                        })}
                    </ul>
                    <Link to='/'>Restart test</Link>
                </div>
            </div>
        )
    }

}

const mapStateToProps = (state) => ({
    active_tab: state.results.active_tab,
    answers: state.results.answers,
    fractions: state.results.fractions,
    mps: state.results.mps,
    topics: state.test_state.topics
})

export default connect((mapStateToProps), {
    setActiveTab
})(ResultsView)