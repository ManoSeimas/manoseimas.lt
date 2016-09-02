import React from 'react'
import styles from '../styles/components/similarity-widget.css'

const ChangeVote = ({answer, onClick}) =>
    <img src={(answer.show_icon) ? answer.img : '/static/img/person.png'}
         onClick={onClick} />

const ShowVote = ({answer}) => {
    if (answer.show_icon) {
        return <img src={answer.img} />
    }
    return null
}

class SimilarityWidget extends React.Component {

    static propTypes = {
        topic: React.PropTypes.object.isRequired,
        items: React.PropTypes.array.isRequired,
        user_answers: React.PropTypes.object.isRequired,
        saveAnswer: React.PropTypes.func
    }

    constructor (props) {
        super(props)
        this.state = { element_width: undefined }
    }

    componentDidMount () {
        this.setState({ element_width: this.refs.middle.offsetWidth})
    }

    getAnswer (user_answers, topic_id) {
        if (user_answers[topic_id])
            return user_answers[topic_id].answer
        return undefined
    }

    answerType (type, user_answers, topic_id) {
        const types = {
            positive: {
                img: '/static/img/person-positive.png',
                show_icon: (this.getAnswer(user_answers, topic_id) > 0),
                value: 2
            },
            neutral: {
                img: '/static/img/person-active.png',
                show_icon: (this.getAnswer(user_answers, topic_id) === undefined),
                value: undefined
            },
            negative: {
                img: '/static/img/person-negative.png',
                show_icon: (this.getAnswer(user_answers, topic_id) < 0),
                value: -2
            }
        }
        return types[type]
    }

    make_procental_answer (answer) {
        // -1p = 0%     (-1 + 1) * 50 => 0
        //  0p = 50%     (0 + 1) * 50 => 50
        //  1p = 100%    (1 + 1) * 50 => 100
        if (isNaN(answer))
            return 0
        return Math.round((Number(answer) / 2 + 1)*50)
    }

    get_image_position (percents) {
        let coeficient = this.state.element_width / 100
        let corection = 25  // Correction per image radius, we want to start from img center.
        return percents * coeficient - corection
    }

    render () {
        const {topic, items, user_answers, saveAnswer} = this.props

        return (
            <div className={styles['similarity-widget']}>
                <div className={styles.no}>PRIEŠ</div>
                <div className={styles.middle} ref='middle'>
                    {items.map(item => {
                        let answer = (item.answers) ? item.answers[topic.id] : 0
                        let percents = this.make_procental_answer(answer)
                        return (
                            <div className={styles.img}
                                 style={{left: this.get_image_position(percents), zIndex: percents}}
                                 key={'item-' + item.id}>
                                <img src={item.logo} alt={`${item.title} logo`} title={`${item.title} - ${percents}%`} />
                            </div>
                        )
                    })}
                    <div className={styles.line}></div>
                    <div className={styles.actions}>
                        <div className={styles.action}>
                            {(saveAnswer)
                                ? <ChangeVote answer={this.answerType('negative', user_answers, topic.id)}
                                              onClick={() => saveAnswer(topic.id, -2)} />
                                : <ShowVote answer={this.answerType('negative', user_answers, topic.id)} />
                            }
                        </div>
                        <div className={styles.action}>
                            {(saveAnswer)
                                ? <ChangeVote answer={this.answerType('neutral', user_answers, topic.id)}
                                              onClick={() => saveAnswer(topic.id, undefined)} />
                                : <ShowVote answer={this.answerType('neutral', user_answers, topic.id)} />
                            }
                        </div>
                        <div className={styles.action}>
                            {(saveAnswer)
                                ? <ChangeVote answer={this.answerType('positive', user_answers, topic.id)}
                                              onClick={() => saveAnswer(topic.id, 2)} />
                                : <ShowVote answer={this.answerType('positive', user_answers, topic.id)} />
                            }
                        </div>
                    </div>
                </div>
                <div className={styles.yes}>UŽ</div>
            </div>
        )
    }
}

export default SimilarityWidget
