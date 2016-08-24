import React from 'react'
import { connect } from 'react-redux'
import { SimilarityBar, SimilarityWidget } from '../../../components'
import { expandTopics, selectFraction } from '../../../store/modules/mps_state'
import { getResults, setTab, saveAnswer } from '../../../store/modules/results'
import FractionsSelector from './FractionsSelector'
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
      selectFraction: React.PropTypes.func
    }

    componentWillMount () {
        // Load test results if they are still not in redux store.
        if (!this.props.mps.length){
            this.props.getResults()
        }
        this.props.setTab('mps')
    }

    render () {
        let {user_answers, mps, fractions, selected_fractions, topics, expanded_mp} = this.props
        return (
            <div>
                <div className={styles.note}>
                    Pasirinkite dominančias frakcijas (galima rinktis kelias iš karto):
                </div>
                <FractionsSelector fractions={fractions}
                                   selected_fractions={selected_fractions}
                                   selectFraction={this.props.selectFraction} />

                <div className={styles.note}>
                    Kuo didesnis procentas, tuo labiau Seimo narys atitinka Jūsų pažiūras.
                </div>
                {mps.map(mp => {
                    let fraction = fractions.find((element, index, array) => mp.fraction_id === element.id) || {}
                    if ((selected_fractions.indexOf(mp.fraction_id) > -1 || selected_fractions.length === 0) && mp.similarity) {
                        return (
                            <div className={styles.item} key={mp.id}>
                                <div className={styles.logo}>
                                    <div className={styles.img}>
                                        <img src={mp.logo} alt={mp.title + ' logo'} />
                                    </div>
                                    <img src={fraction.logo} className={styles['fraction-logo']} />
                                </div>
                                <main>
                                    <div className={styles.title}>{mp.name}, {mp.fraction}, {mp.similarity}%</div>
                                    <SimilarityBar similarity={mp.similarity} />
                                    <a onClick={() => this.props.expandTopics(mp.id)}>
                                        Atsakymai pagal klausimus
                                        <div className={styles.arrow}></div>
                                    </a>
                                </main>
                                {(expanded_mp === mp.id)
                                    ? <div className={styles.topics}><ol>
                                    {topics.map(topic => {
                                        return <li key={topic.id}>
                                            {topic.name} <br />
                                            <SimilarityWidget topic={topic}
                                                              items={[mp]}
                                                              saveAnswer={this.props.saveAnswer}
                                                              user_answers={user_answers} />
                                        </li>
                                    })}
                                    </ol></div>
                                    : ''
                                }
                            </div>
                        )
                    }
                })}
            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    user_answers: state.results.answers,
    topics: state.test_state.topics,
    mps: state.results.mps,
    fractions: state.results.fractions,
    selected_fractions: state.mps_state.selected_fractions,
    expanded_mp: state.mps_state.expanded_mp
})

export default connect((mapStateToProps), {
    expandTopics,
    getResults,
    saveAnswer,
    setTab,
    selectFraction
})(SimilarityMps)
