import React from 'react'
import styles from './styles.css'
import Modal from 'react-modal'


const Arguments = (props) =>
    <div className={styles.arguments}>
        <div className={styles.box}>
            <div className={styles['positive-head']}>Už</div>
            {props.arguments.map(argument => {
                if (argument.supporting)
                    return <Argument argument={argument} />
            })}
        </div>
        <div className={styles['negative-box']}>
            <div className={styles['negative-head']}>Prieš</div>
            {props.arguments.map(argument => {
                if (!argument.supporting)
                    return <Argument argument={argument} />
            })}
        </div>
    </div>

Arguments.propTypes = {
    arguments: React.PropTypes.array.isRequired
}


class Argument extends React.Component {

    constructor () {
        super()
        this.openModal = this.openModal.bind(this)
        this.closeModal = this.closeModal.bind(this)
        this.state = {open: false}
    }

    static propTypes = {
        argument: React.PropTypes.object.isRequired
    }

    openModal () { this.setState({open: true}) }
    closeModal () { this.setState({open: false}) }

    customStyle () {
        return {
            overlay : {
                position          : 'fixed',
                top               : 0,
                left              : 0,
                right             : 0,
                bottom            : 0,
                backgroundColor   : 'rgba(0, 0, 0, 0.75)'
            },
            content : {
                position                   : 'absolute',
                width                      : '600px',
                height                     : 'auto',
                top                        : '50%',
                left                       : '50%',
                bottom                     : '30px;',
                transform                  : 'translate(-50%, -50%)',
                border                     : '1px solid #ccc',
                background                 : '#fff',
                overflow                   : 'none',
                WebkitOverflowScrolling    : 'touch',
                borderRadius               : '4px',
                outline                    : 'none',
                padding                    : '30px'
            }
        }
    }

    render () {
        let argument = this.props.argument
        return (
            <div className={styles.argument} key={argument.id}>
                <h3>{argument.name}</h3>
                <p>{argument.short_description}
                    {(argument.description)
                        ? <a className={styles.more} onClick={this.openModal}>Daugiau</a>
                        : undefined }
                </p>

                <Modal
                    isOpen={this.state.open}
                    style={this.customStyle()}
                    onRequestClose={this.closeModal}>
                    <h2 className={styles.title}>{argument.name}</h2>
                    <div className={styles.text}
                         dangerouslySetInnerHTML={{__html:argument.description}} />
                </Modal>
            </div>
        )
    }
}

export default Arguments