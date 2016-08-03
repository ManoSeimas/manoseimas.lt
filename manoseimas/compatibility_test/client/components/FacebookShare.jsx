import React from 'react'
import { connect } from 'react-redux'
import { subscribe } from 'subscribe-ui-event'
import Button from './Button'
import styles from '../styles/components/facebook-share.css'

class FacebookShare extends React.Component {

    constructor (props) {
        super(props)
        this.state = { sticky: false }
        this.subscribers
        this.shareOnFacebook = this.shareOnFacebook.bind(this)
        this.scrollHandler = this.scrollHandler.bind(this)
    }

    static propTypes = {
        responseHandler: React.PropTypes.func,
        fractions: React.PropTypes.array
    }

    componentDidMount () {
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

    shareOnFacebook () {
        const location = window.location.href.split('/')
        const base_url = location[0] + '//' + location[2]

        const fraction_one = this.props.fractions[0]
        const fraction_two = this.props.fractions[1]
        const fraction_three = this.props.fractions[2]

        const picture = base_url + '/static/img/fb-share/' + `${fraction_one.short_title}/${fraction_two.short_title}-${fraction_three.short_title}.png`

        let description = ''
        description = description + `${fraction_one.title} ${fraction_one.similarity}%; `
        description = description + `${fraction_two.title} ${fraction_two.similarity}%; `
        description = description + `${fraction_three.title} ${fraction_three.similarity}%. \n`
        description = description + 'Su kokiomis politinėmis partijomis ir politikais sutampi tu?'
        let caption = 'Sužinok daugiau >>>'

        FB.ui({
            method: 'feed',
            link: base_url + '/test',
            picture: picture,
            name: 'Politinių pažiūrų testas',
            caption: caption,
            description: description
        }, this.props.responseHandler)
    }

    render () {
        let fractions = this.props.fractions
        let sticky_style = {}
        if (this.state.sticky) {
            sticky_style = {
                position: 'fixed',
                top: '10px'
            }
        }
        return (
            <div className={styles['share-block']} style={sticky_style}>
                <header>Mano balsavimai seime sutaptų su:</header>
                {(fractions.length > 2)
                    ? <div className={styles.fractions}>
                        <div className={styles['img-main']}>
                            <img src={fractions[0].logo} />
                        </div>
                        <div className={styles['img-second']}>
                            <img src={fractions[1].logo} />
                        </div>
                        <div className={styles['img-third']}>
                            <img src={fractions[2].logo} />
                        </div>
                    </div>
                    : ''
                }
                <Button type='facebook' action={this.shareOnFacebook}>
                    Pasidalinti
                </Button>
            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    fractions: state.results.fractions
})

export default connect((mapStateToProps), {})(FacebookShare)
