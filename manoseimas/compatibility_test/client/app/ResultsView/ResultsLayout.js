import React, { PropTypes } from 'react'
import { Link } from 'react-router'
import { StatusBar, Footer } from '../../components'
import Tabs from './Tabs'
import Sidebar from './Sidebar'
import styles from '../../styles/views/results.css'

export const ResultsLayout = ({ children }) =>
    <div>
        <header>
            <a href="/">
                <img src='/static/img/logo-black.png'
                     className='logo'
                     alt='manoSeimas logo'
                     title='manoSeimas.lt home' />
            </a>
            <StatusBar current={12} max={12} />
        </header>
        <div className={styles['main-area']}>
            <div className={styles.content}>
                <h2 className='title'>Rezultatai</h2>
                <Tabs />
                {children}
            </div>
            <Sidebar />
        </div>
        <Footer />
    </div>

ResultsLayout.propTyoes = {
    children: PropTypes.element.isRequired
}

export default ResultsLayout