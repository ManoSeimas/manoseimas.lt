import React from 'react'
import { Block, StatusBar } from '../../components'
import styles from '../../styles/views/start.css'

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
                    <strong>Atsakyk į 12 klausimų</strong> apie svarbiausius Lietuvos įvykius,
                    dėl kurių balsuota 2012-2016 metų Seime.
                </span>
            </Block>
            <Block number={2}>
               <span>
                    <strong>Gauk rezultatus</strong>, kurie Seimo nariai ir partijos balsavo
                    panašiausiai į tave.
                </span>
            </Block>
            <Block number={3} style={{marginTop: '15px'}} desktopOnly={true}>
                <span>
                    <strong>Dalinkis</strong> rezultatais su draugais.
                </span>
            </Block>

            <div className={styles['block']}>
                <div className={styles['note']}>
                    Dėmesio, manoSeimas.lt apžvelgia tik 12 svarbių valstybės
                    gyvenimo klausimų. Primename, kad renkantis už ką balsuoti, neužtenka
                    vadovautis vien šio testo rezultatais.
                </div>
                <a className='button' onClick={props.onClickHandler}>Pradėti</a>
            </div>
        </div>

        {(props.img_url) ?
            <div className={styles['context']}>
                <img src={props.img_url} alt="" />
            </div>
        : <div className={styles['context-image']}></div>
        }
    </div>

StartTest.propTypes = {
    onClickHandler: React.PropTypes.func.isRequired,
    amount: React.PropTypes.number.isRequired,
    title: React.PropTypes.string.isRequired,
    img_url: React.PropTypes.string
}

export default StartTest
