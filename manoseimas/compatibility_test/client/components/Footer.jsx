import React from 'react'
import styles from '../styles/components/footer.css'

const Footer = (props) =>
  <footer>
    <div className={styles.sponsors}>
      <div className={styles['sponsor-left']}>
        <a href='http://www.transparency.lt' target='_blank'>
          <img src='/static/img/tils-footer.png' />
        </a>
      </div>
      <div className={styles.sponsor}>
        <a href='http://lithuania.nlembassy.org' target='_blank'>
          <img src='/static/img/ambasada-footer.png' title='Nyderlandų ambasada' />
        </a>
      </div>
    </div>

    <div className={styles.menu}>
      <a className={styles.item} href='/team'>Komanda</a>
      <a className={styles.item} href='/team'>Apie iniciatyvą</a>
      <a className={styles.item} href='/team'>Testas</a>
    </div>

    <div className={styles.copyright}>
      © 2012-2016, manoSeimas.lt pateikiamas pagal&nbsp;
      <a href="http://creativecommons.org/licenses/by/4.0/">
        CC&nbsp;BY&nbsp;4.0
      </a>
      &nbsp;turinio naudojimo licenciją
    </div>
  </footer>

export default Footer
