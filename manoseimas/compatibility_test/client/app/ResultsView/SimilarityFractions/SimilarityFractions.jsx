import React, { PropTypes } from 'react'
import { subscribe } from 'subscribe-ui-event'
import { SimilarityBar, StickyHeader } from '../../../components'
import FractionMps from './FractionMps'
import styles from '../../../styles/views/results.css'

class SimilarityFractions extends React.Component {

    constructor (props) {
        super(props)
        this.subscribers
        this.header_position
        this.scrollHandler = this.scrollHandler.bind(this)
        this.showMoreMps = this.showMoreMps.bind(this)
    }

    static propTypes = {
      user_answers: PropTypes.object,
      fractions: PropTypes.array,
      mps: PropTypes.array,
      show_header: PropTypes.bool,
      expanded_number: PropTypes.string,
      showHeader: PropTypes.func,
      hideHeader: PropTypes.func,
      expandFraction: PropTypes.func,
      setActiveTab: PropTypes.func,
      setSelectedFractions: PropTypes.func
    }

    static contextTypes = {
        router: React.PropTypes.object
    }

    componentDidMount () {
        // We have to wait until images will load.
        setTimeout(() => {
            let node = this.refs['similarities']
            this.header_position = node.offsetTop + node.offsetHeight - 100
        }, 3000);
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

    scrollHandler (event, payload) {
        if (payload.scroll.top > this.header_position && !this.props.show_header) {
            this.props.showHeader()
        }

        if (payload.scroll.top < this.header_position && this.props.show_header) {
            this.props.hideHeader()
        }
    }

    get_mps (fraction) {
        let mps = []
        for (let mp of this.props.mps) {
            if (mp.fraction == fraction) {
                mps.push(mp)
            }
        }
        return mps
    }

    showMoreMps (fraction_id) {
        // Open /mps and set selected_fractions to fraction_id
        this.context.router.push('/results/mps')
        this.props.setSelectedFractions([fraction_id])
    }

    render () {
        let {fractions, mps, user_answers, show_header, expanded_fraction} = this.props
        return (
            <div ref='similarities'>
            {fractions.map(fraction => {
                if (fraction.members_amount > 0) {
                    return (
                        <div className={styles.item} key={fraction.short_title}>
                            <div className={styles.img}>
                                <img src={fraction.logo} alt={fraction.title + ' logo'} />
                            </div>
                            <main>
                                <div className={styles.title}>{`${fraction.title}, ${fraction.similarity}%`}</div>
                                <SimilarityBar similarity={fraction.similarity} />
                                <a onClick={() => this.props.expandFraction(fraction.id)}>
                                    {fraction.members_amount} nariai {' '}
                                    <div className={styles.arrow}></div>
                                </a>
                            </main>
                            {(expanded_fraction === fraction.id)
                                ? <FractionMps mps={this.get_mps(fraction.short_title)}
                                               user_answers={user_answers}
                                               showMoreMps={this.showMoreMps} />
                                : ''
                            }
                        </div>
                    )
                }
            })}
            {(show_header)
                ? <StickyHeader width="680px">
                    <div className={styles['similarity-header']}>
                        {fractions.map(fraction => {
                            return (
                                <div className={styles.img} style={{left: fraction.similarity * 6}} key={fraction.short_title}>
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