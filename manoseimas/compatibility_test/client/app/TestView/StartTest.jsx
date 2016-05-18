import React from 'react'
import { Link } from 'react-router'
import { Block, StatusBar } from '../../components'
import styles from '../../styles/base.css'

const StartTest = (props) =>
    <div>
        <header>
            <img src='/static/img/logo-black.png' className='logo' />
            <StatusBar current={1} max={10} />
        </header>

        <div className={styles['content']}>
            <h2>Testo pavadinimas</h2>
            <Block number={1}>
                <strong>Atsakykite į 10 klausimų</strong> apie svarbiausius Lietuvos įvykius,
                dėl kurių balsuota Seime.
            </Block>
            <Block number={2}>
                <strong>Gaukite rezultatus</strong>, kurios partijos ir Seimo nariai balsavo
                panašiausiai į Jus.
            </Block>

            <div className={styles['block']}>
                <div className={styles['note']}>
                    Dėmesio, manoSeimas.lt apžvelgia tik 10 svarbių valstybės gyvenimo
                    klausimų. Todėl primename, kad renkantis už ką balsuoti, neužtenka
                    vadovautis šio testo rezultatais.
                </div>

                <Link to='/question' className='button'>Pradėti</Link>
            </div>
        </div>

        <div className={styles['context-image']}></div>
    </div>

export default StartTest