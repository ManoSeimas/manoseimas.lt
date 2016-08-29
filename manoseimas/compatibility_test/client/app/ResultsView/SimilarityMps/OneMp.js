import React from 'react'
import { SimilarityBar, SimilarityWidget } from '../../../components'
import styles from '../../../styles/views/results.css'

const OneMp = ({mp, fraction, topics, user_answers, expandTopics, expanded_mp}) =>
  <div className={styles.item} key={mp.id}>
      <a href={mp.url} className={styles.logo} target='_blank'>
          <div className={styles.img}>
              <img src={mp.logo} alt={mp.title + ' logo'} />
          </div>
          <img src={fraction.logo} className={styles['fraction-logo']} />
      </a>
      <main>
          <div className={styles.title}>{mp.name}, {mp.fraction}, {mp.similarity}%</div>
          <SimilarityBar similarity={mp.similarity} />
          <a onClick={() => expandTopics(mp.id)}>
              Atsakymai pagal klausimus
              <div className={styles.arrow}></div>
          </a>
      </main>
      {(expanded_mp === mp.id)
          ? <div className={styles.topics}><ol>
              {topics.map(topic => {
                  return <li key={topic.id}>
                      {topic.name} <br />
                      <SimilarityWidget topic={topic}
                                        items={[mp]}
                                        user_answers={user_answers} />
                  </li>
              })}
            </ol></div>
          : ''
      }
  </div>

export default OneMp