import React from 'react'
import { Block, StatusBar } from '../../../components'
import styles from '../../../styles/base.css'

const StartTest = (props) =>
    <div>
        <header>
            <img src='/static/img/logo-black.png' className='logo' />
            <StatusBar current={0} max={props.amount} />
        </header>

        <div className={styles['content']}>
            <h2>{props.title}</h2>
            <Block number={1}>
                <span>
                    <strong>Atsakykite į 10 klausimų</strong> apie svarbiausius Lietuvos įvykius,
                dėl kurių balsuota Seime.
                </span>
            </Block>
            <Block number={2}>
               <span>
                   <strong>Gaukite rezultatus</strong>, kurios partijos ir Seimo nariai balsavo
                   panašiausiai į Jus.
                </span>
            </Block>

            <div className={styles['block']}>
                <div className={styles['note']}>
                    Dėmesio, manoSeimas.lt apžvelgia tik 10 svarbių valstybės gyvenimo
                    klausimų. Todėl primename, kad renkantis už ką balsuoti, neužtenka
                    vadovautis šio testo rezultatais.
                </div>
                <a className='button' onClick={props.onClickHandler}>Pradėti</a>
            </div>
        </div>

        <div className={styles['context-image']}></div>
    </div>

StartTest.propTypes = {
    onClickHandler: React.PropTypes.func.isRequired,
    amount: React.PropTypes.number.isRequired,
    title: React.PropTypes.string.isRequired
}

export default StartTest
