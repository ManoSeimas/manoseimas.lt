import React from 'react'
import styles from '../styles/components/manobalsas.css'

const ManoBalsas = (props) =>
    <div className={styles.block}>
        <div className={styles.note}>
            Nori pasilyginti pagal politikų pasisakymus?
        </div>
        <a href="http://manobalsas.lt" target="_blank">
            <img src="/static/img/manobalsas-logo.png" />
        </a>
    </div>

export default ManoBalsas
