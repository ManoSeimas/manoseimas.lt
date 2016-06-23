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

const SimilarityFractions = ({user_answers, fractions}) =>
    <div>
        <p>Kuo didesnis procentas, tuo labiau frakcija atitinka Jūsų pažiūras.</p>
        <ul>
            {fractions.map(fraction => {
                return <li key={fraction.short_title}>{fraction.title} - {similarity(user_answers, fraction.answers)}%</li>
            })}
        </ul>
    </div>

SimilarityFractions.propTypes = {
  user_answers: React.PropTypes.object,
  fractions: React.PropTypes.array
}

export default SimilarityFractions