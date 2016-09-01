import React from 'react'
import { connect } from 'react-redux'
import { subscribe } from 'subscribe-ui-event'
import { FacebookShare } from '../../components'
import styles from '../../styles/views/results.css'

class Sidebar extends React.Component {

    static propTypes = {
        fractions: React.PropTypes.array
    }

    constructor (props) {
        super(props)
        this.state = { sticky: false }
        this.subscribers
        this.scrollHandler = this.scrollHandler.bind(this)
    }

    componentDidMount () {
        console.log('scroll')
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
        if (payload.scroll.top > 100 && !this.state.sticky) {
            this.setState({sticky: true})
        }

        if (payload.scroll.top < 101 && this.state.sticky) {
            this.setState({sticky: false})
        }
    }

    trackFBShare (response) {
        if (response)
            window.ga('send', 'event', {
                eventCategory: 'Facebook Share',
                eventAction: 'click',
                eventLabel: 'Post successfully shared'
            })
    }

    render () {
        let sticky_style = {}
        if (this.state.sticky) {
            sticky_style = {
                position: 'fixed',
                top: '10px'
            }
        }

        if (this.props.fractions.length !== 0)
            return (
                <div className={styles.side}>
                    <div  style={sticky_style}>
                        <FacebookShare responseHandler={this.trackFBShare} fractions={this.props.fractions} />
                    </div>
                </div>
            )

        return null
    }

}

const mapStateToProps = (state) => ({
    fractions: state.results.fractions
})

export default connect((mapStateToProps), {})(Sidebar)
