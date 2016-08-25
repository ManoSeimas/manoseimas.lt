import React from 'react'
import OneMp from './OneMp'
import styles from '../../../styles/views/results.css'

const ListOfMps = (props) => {
  const {
    mps,
    fractions,
    user_answers,
    selected_fractions,
    show_all_mps,
    topics,
    expanded_mp } = props
  return (
    <div className={styles.mps}>
      <div className={styles.note}>
        Kuo didesnis procentas, tuo labiau Seimo narys atitinka Jūsų pažiūras.
      </div>
      {(show_all_mps)
        ? mps.map(mp => {
            let fraction = fractions.find((element, index, array) => mp.fraction_id === element.id) || {}
            if ((selected_fractions.indexOf(mp.fraction_id) > -1 || selected_fractions.length === 0) && mp.similarity) {
                return <OneMp mp={mp}
                              key={mp.id}
                              fraction={fraction}
                              topics={topics}
                              user_answers={user_answers}
                              expanded_mp={expanded_mp}
                              expandTopics={props.expandTopics} />
            }
        })
        : [0, 1, 2, 3, 4, mps.length-5, mps.length-4, mps.length-3, mps.length-2, mps.length-1].map(item => {
          let mp = mps[item]
          let fraction = fractions.find((element, index, array) => mp.fraction_id === element.id) || {}
          return <div>
            <OneMp mp={mp}
                   key={mp.id}
                   fraction={fraction}
                   topics={topics}
                   user_answers={user_answers}
                   expanded_mp={expanded_mp}
                   expandTopics={props.expandTopics} />
            {(item === 4)
              ? <a className={styles.more}
                   onClick={() => props.showAllMps()}>
                   &gt; Kiti {mps.length - 4} parlamentarai &lt;
                </a>
              : null
            }
          </div>
        })
      }
    </div>
  )
}

export default ListOfMps
