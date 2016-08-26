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

  const selected_mps = mps.filter(mp => selected_fractions.indexOf(mp.fraction_id) > -1 || selected_fractions.length === 0)
  return (
    <div className={styles.mps}>
      <div className={styles.note}>
        Kuo didesnis procentas, tuo labiau Seimo narys atitinka Jūsų pažiūras.
      </div>
      {(show_all_mps)
        ? selected_mps.map(mp => {
            let fraction = fractions.find((element, index, array) => mp.fraction_id === element.id) || {}
            if (mp.similarity) {
                return <OneMp mp={mp}
                              key={mp.id}
                              fraction={fraction}
                              topics={topics}
                              user_answers={user_answers}
                              expanded_mp={expanded_mp}
                              expandTopics={props.expandTopics} />
            }
        })
        : [0, 1, 2, 3, 4, selected_mps.length-5, selected_mps.length-4, selected_mps.length-3, selected_mps.length-2, selected_mps.length-1].map(item => {
          let mp = selected_mps[item]
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
                   &gt; Kiti {selected_mps.length - 4} parlamentarai &lt;
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
