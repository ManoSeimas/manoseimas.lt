function(doc) {
    var words, word;
    var chars = {
        'ą': 'a', 'Ą': 'a',
        'č': 'c', 'Č': 'c',
        'ę': 'e', 'Ę': 'e',
        'ė': 'e', 'Ė': 'e',
        'į': 'i', 'Į': 'i',
        'ų': 'u', 'Ų': 'u',
        'ū': 'u', 'Ū': 'u',
        'š': 's', 'Š': 's',
        'ž': 'z', 'Ž': 'z'
    };
    var pattern = [];
    for (var c in chars) {
        pattern.push(c);
    }
    var chars_re = RegExp(pattern.join('|'), 'g');

    var ignore = [
        'antai', 'ar', 'arba', 'taip', 'ne', 'is', 'su', 'prie', 'uz', 'argi',
        'be', 'bene', 'bent', 'bet', 'beveik', 'dar', 'gal', 'gi', 'ir', 'jau',
        'juk', 'juo', 'kažin', 'ko', 'kone', 'kuo', 'kuone', 'lyg', 'ne',
        'nebe', 'nebent', 'nei', 'nejaugi', 'net', 'ne', 'pat', 'per', 'tarsi',
        'tartum', 'tegu', 'tik', 'tiktai', 'veik', 'vien', 'vis', 'vos', 'vel',
        'ypac', 'stai'
            ];

    var get_words = function (text) {
        words = text.replace(chars_re, function(match) {
            return chars[match];
        });
        words = words.toLowerCase();
        return words.split(/[^a-z]+/);
    };

    if (doc.importance > 0) {
        words = [];

        if (doc.title) {
            words = get_words(doc.title);
        }

        if (doc.documents) {
            for (var j=0; j<doc.documents.length; j++) {
                words = words.concat( get_words(doc.documents[j].name) )
            }
        }

        for (var j=0; j<words.length; j++) {
            word = words[j];
            if (word && ignore.indexOf(word) == -1) {
                emit([word, doc.importance, doc.created], null);
            }
        }

    }
}
