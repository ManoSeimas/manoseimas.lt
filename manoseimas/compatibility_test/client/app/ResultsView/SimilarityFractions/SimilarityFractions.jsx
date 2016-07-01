import React, { PropTypes } from 'react'
import { subscribe } from 'subscribe-ui-event'
import { SimilarityBar, StickyHeader } from '../../../components'
import styles from '../../../styles/views/results.css'

class SimilarityFractions extends React.Component {

    constructor (props) {
        super(props)
        this.subscribers
        this.header_position
        this.scrollHandler = this.scrollHandler.bind(this)
    }

    static propTypes = {
      user_answers: PropTypes.object,
      fractions: PropTypes.array,
      mps: PropTypes.array,
      show_header: PropTypes.bool,
      expanded_number: PropTypes.string,
      showHeader: PropTypes.func,
      hideHeader: PropTypes.func,
      expandFraction: PropTypes.func
    }

    componentDidMount () {
        // We have to wait until images will load.
        setTimeout(() => {
            let node = this.refs['similarities']
            this.header_position = node.offsetTop + node.offsetHeight - 100
        }, 1000);
        this.subscribers = [
            subscribe('scroll', this.scrollHandler, {enableScrollInfo:true})
        ]
    }

    componentWillUnmount () {
        let subscribers = this.subscribers || []
        for (let subscriber of subscribers) {
            subscriber.unsubscribe()
        }
    }

    scrollHandler(event, payload) {
        if (payload.scroll.top > this.header_position && !this.props.show_header) {
            this.props.showHeader()
        }

        if (payload.scroll.top < this.header_position && this.props.show_header) {
            this.props.hideHeader()
        }
    }

    calculate_similarity (fraction_answers) {
        let points = 0,
            answers_count = 0,
            answers = this.props.user_answers

        for (let answer_id in fraction_answers) {
            if (answers[answer_id] && answers[answer_id].answer) {
                let answer_points = Math.abs((answers[answer_id].answer + fraction_answers[answer_id]) / 2)
                if (answers[answer_id].important) {
                    answers_count += 2
                    answer_points *= 2
                } else {
                    answers_count++
                }
                points += answer_points
            }
        }

        return Math.round((points / answers_count)*100)
    }

    render () {
        let {fractions, mps, user_answers, show_header, expanded_fraction} = this.props
        return (
            <div ref='similarities'>
            {fractions.map(fraction => {
                let similarity = this.calculate_similarity(fraction.answers)
                return (
                    <div className={styles.item} key={fraction.short_title}>
                        <div className={styles.img}>
                            <img src={fraction.logo} alt={fraction.title + ' logo'} />
                        </div>
                        <main>
                            <div className={styles.title}>{fraction.title}, {similarity}%</div>
                            <SimilarityBar similarity={similarity} />
                            <a onClick={() => this.props.expandFraction(fraction.id)}>
                                {fraction.members_amount} nariai {' '}
                                <div className={styles.arrow}></div>
                            </a>
                        </main>
                        {(expanded_fraction === fraction.id)
                            ? <div className={styles.members}>
                                {mps.map(mp => {
                                    if (mp.fraction === fraction.short_title) {
                                        let similarity = this.calculate_similarity(mp.answers)
                                        return <div className={styles.item} key={mp.id}>
                                            <div className={styles.img}>
                                                <img src={mp.logo} alt={mp.name + ' logo'} />
                                            </div>
                                            <main>
                                                <div className={styles.title}>{mp.name}, {mp.fraction}, {similarity}%</div>
                                                <SimilarityBar similarity={similarity} slim={true} />
                                            </main>
                                        </div>
                                    }
                                })}
                            </div>
                            : ''
                        }
                    </div>
                )
            })}
            {(show_header)
                ? <StickyHeader width="650px">
                    <div className={styles['similarity-header']}>
                        {fractions.map(fraction => {
                            let similarity = this.calculate_similarity(fraction.answers)
                            return (
                                <div className={styles.img} style={{left: similarity * 6}} key={fraction.short_title}>
                                    <img src={fraction.logo} alt={fraction.title + ' logo'} />
                                </div>
                            )
                        })}
                        <div className={styles['similarity-bar']}>
                            <div>0%</div>
                            <div className={styles.line}></div>
                            <div>100%</div>
                        </div>
                    </div>
                </StickyHeader>
                : ''}
            </div>
        )
    }

}

export default SimilarityFractions