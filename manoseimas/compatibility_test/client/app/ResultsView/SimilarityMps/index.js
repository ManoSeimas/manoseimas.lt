import React from 'react'

function similarity (user_answers, fraction_answers) {
    let points = 0,
        answers_count = 0

    for (let answer_id in fraction_answers) {
        if (user_answers[answer_id]) {
            answers_count++
            points += Math.abs((user_answers[answer_id] + fraction_answers[answer_id]) / 2)
        }
    }

    return Math.round((points / answers_count)*100)
}

const SimilarityMps = ({user_answers, mps}) =>
    <div>
        <p>Kuo didesnis procentas, tuo labiau Seimo narys atitinka Jūsų pažiūras.</p>
        <ul>
            {mps.map(mp => {
                return <li>{mp.name} - {similarity(user_answers, mp.answers)}%</li>
            })}
        </ul>
    </div>

SimilarityMps.propTypes = {
  user_answers: React.PropTypes.object,
  mps: React.PropTypes.array
}

export default SimilarityMps