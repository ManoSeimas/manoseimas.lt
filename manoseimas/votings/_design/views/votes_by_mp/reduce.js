function (key, values, rereduce) {
    return values.reduce(function(sum, item) {
        return {
            'aye': sum.aye + (item.aye || 0),
            'no': sum.no + (item.no || 0),
            'abstain': sum.abstain + (item.abstain || 0)
        }
    }, {'aye': 0, 'no': 0, 'abstain': 0});
}
