import React, { PropTypes } from 'react'
import Modal from '../Modal'
import { Button } from '../../../../components'
import styles from './styles.css'

export default class Arguments extends React.Component {

    static propTypes = {
        arguments: PropTypes.object.isRequired,
        toggleArguments: PropTypes.func.isRequired,
        opened: PropTypes.bool.isRequired
    }

    render () {
        return (
            <div className='inline'>
                {(this.props.opened)
                    ? <Modal><h3>Modal opened</h3></Modal>
                    : <Button type='small'
                              action={this.props.toggleArguments}
                              arrow={true}>Padėkite apsispręsti</Button>
                }
            </div>
        )
    }

}
