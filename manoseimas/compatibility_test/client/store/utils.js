import Cookies from 'js-cookie'

export function fetch(method, url, req_body) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest()
    request.open(method, url, true)
    request.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
    request.addEventListener('load', () => resolve(request.responseText))
    request.addEventListener('error', () => reject('Request Error: ', request.response))
    request.send(req_body)
  })
}

export function calculateSimilarity(fraction_answers, user_answers) {
    let points = 0,
        answers_count = 0,
        answers = user_answers

    // Similarity is 0% if there is no data about fracion answers
    if (!fraction_answers)
        return 0

    for (let answer_id in fraction_answers) {
        if (answers[answer_id] && answers[answer_id].answer) {
            let answer_points = Math.abs((answers[answer_id].answer + Number(fraction_answers[answer_id])) / 2)
            if (answers[answer_id].important) {
                answers_count += 2
                answer_points *= 2
            } else {
                answers_count++
            }
            points += answer_points
        }
    }

    return Math.round((points / answers_count)*100)
}

export function sortResults(results) {
    // Filter out old/inactive/renamed fractions which have 0 members.
    results.fractions = results.fractions.filter((fraction) => fraction.members_amount > 0)

    // Calculate similarity
    results.fractions = results.fractions.map((fraction) => {
        let similarity = calculateSimilarity(fraction.answers, results.user_answers || results.answers)
        fraction.similarity = similarity
        return fraction
    })

    // Sort fractions by similarity (desc)
    results.fractions.sort((a, b) => {
        if (a.similarity > b.similarity)
            return -1

        if (a.similarity < b.similarity)
            return 1

        return 0
    })

    return results
}
