import React, { PropTypes } from 'react'
import { Link } from 'react-router'
import { StatusBar } from '../../components'
import Tabs from './Tabs'
import styles from '../../styles/views/results.css'

export const ResultsLayout = ({ children }) =>
    <div>
        <header>
            <img src='/static/img/logo-black.png' className='logo' />
            <StatusBar current={10} max={10} />
        </header>
        <div className={styles.content}>
            <h2 className='title'>Rezultatai</h2>
            <Tabs />
            {children}
        </div>
        <Link to='/'>Restart test</Link>
    </div>

ResultsLayout.propTyoes = {
    children: PropTypes.element.isRequired
}

export default ResultsLayout