# coding: utf-8

import re
import string

import lxml.html.clean
import lxml.html.defs

words_re = re.compile(r'\w+', re.UNICODE)
clean_chunk_re = re.compile(
        r'(^%(chars)s)|(%(chars)s$)' % {'chars': r'(\s|[:,.])+'}, re.UNICODE)
split_by_comma_re = re.compile(r'\s*,\s*')


def clean_chunk(chunk):
    return clean_chunk_re.sub('', chunk)


def clean_html(content):
    # See http://lxml.de/api/lxml.html.clean.Cleaner-class.html
    attrs = lxml.html.defs.safe_attrs - {'class'}
    cleaner = lxml.html.clean.Cleaner(style=True, safe_attrs=attrs)
    return cleaner.clean_html(content)


def split_by_comma(text):
    """

    >>> split_by_comma('Ceslovas.Jursenas@lrs.lt ,  cejurs@lrs.lt')
    ['Ceslovas.Jursenas@lrs.lt', 'cejurs@lrs.lt']
    >>> split_by_comma('2396025 ,   2396626')
    ['2396025', '2396626']
    >>> split_by_comma('2396025')
    ['2396025']

    """
    return split_by_comma_re.split(text)


def find_key(keys, words, normalize=string.lower):
    """Return first key in keys list by given list of words.

    This function expects, that keys are sorted(keys, key=len, reverse=True)
    and normalized.

    >>> find_key(['a b c', 'a b', 'a'], ['a'])
    'a'
    >>> find_key(['a b c', 'a b', 'a'], ['a', 'b'])
    'a b'
    >>> find_key(['a b c', 'a b', 'a'], ['a', 'b', 'c'])
    'a b c'
    >>> find_key(['a b c', 'a b', 'a'], ['a', 'b', 'c', 'd'])
    'a b c'
    >>> find_key(['a b c', 'a b', 'a'], ['x', 'a'])


    """
    words = list(words)
    while words:
        word = normalize(' '.join(words))
        for key in keys:
            if len(word) > len(key):
                break
            if key == word:
                return key
        words.pop()


def mapwords(wordmap):
    def callback(word):
        word = word.lower()
        if word in wordmap:
            return wordmap[word]
        else:
            return word
    return callback


def fill_stack(stack, iterator, size):
    """Fill stack with size items from iterator.

    >>> stack = []
    >>> iterator = iter(range(9))
    >>> fill_stack(stack, iterator, 2)
    [0, 1]
    >>> stack.pop()
    1
    >>> fill_stack(stack, iterator, 2)
    [0, 2]
    >>> fill_stack(stack, iterator, 6)
    [0, 2, 3, 4, 5, 6]
    >>> fill_stack(stack, iterator, 2)
    [0, 2, 3, 4, 5, 6]

    """
    missing = size - len(stack)
    while missing > 0:
        item = next(iterator, None)
        if item is None:
            return stack
        else:
            stack.append(item)
            missing -= 1
    return stack


def str2dict(keys, text, stack_size=3, normalize=string.lower,
             clean_chunk=clean_chunk):
    u"""Returns dict from given text, by splitting it with given keys.

    >>> list(str2dict(['A', 'b', 'c'], 'a 1 B 2 c 3'))
    [('a', '1'), ('b', '2'), ('c', '3')]

    >>> list(str2dict(['a', 'b', 'b c'], '0 a 1 b 2 C 3 b C 23'))
    [('', '0'), ('a', '1'), ('b', '2 C 3'), ('b c', '23')]

    >>> list(str2dict(['a', 'B', 'C'], '0 a 1 b 2 c 3 b c 23'))
    [('', '0'), ('a', '1'), ('b', '2'), ('c', '3'), ('b', ''), ('c', '23')]

    >>> list(str2dict(['x'], 'a 1 b 2 c 3',
    ...               normalize=mapwords({'a': 'x', 'b': 'x'})))
    [('x', '1'), ('x', '2 c 3')]

    Real world example:

    >>> import pprint
    >>> text = (u'Seimo narys   nuo  2008-11-17  iki  2008-11-18 . Išrinktas '
    ...         u'pagal sąrašą ,  iškėlė  Tėvynės sąjunga - Lietuvos '
    ...         u'krikščionys demokratai Kandidato puslapis')
    >>> keys = [u'seimo narys', u'išrinktas', u'iškėlė', u'kandidato puslapis']
    >>> r1 = dict(str2dict(keys, text))
    >>> print(unicode(pprint.pformat(r1), 'unicode_escape'))
    {u'iškėlė': u'Tėvynės sąjunga - Lietuvos krikščionys demokratai',
     u'išrinktas': u'pagal sąrašą',
     u'kandidato puslapis': u'',
     u'seimo narys': u'nuo  2008-11-17  iki  2008-11-18'}
    >>> r2 = dict(str2dict(['nuo', 'iki'], r1['seimo narys']))
    >>> print(unicode(pprint.pformat(r2), 'unicode_escape'))
    {'iki': u'2008-11-18', 'nuo': u'2008-11-17'}

    """
    keys = (normalize(key) for key in keys)
    keys = list(sorted(keys, key=len, reverse=True))
    words = words_re.finditer(text)
    next_key = ''
    stack = []
    position = 0
    while fill_stack(stack, words, stack_size):
        stack_words = (m.group() for m in stack)
        key = find_key(keys, stack_words, normalize)
        if key:
            key_size = len(key.split(' '))
            matches = stack[:key_size]
            chunk = text[position:matches[0].start()]
            chunk = clean_chunk(chunk)
            if next_key or chunk:
                yield (next_key, chunk)
            next_key = key
            position = matches[-1].end()
            stack = stack[key_size:]
        else:
            stack.pop(0)

    chunk = text[position:]
    chunk = clean_chunk(chunk)
    if next_key or chunk:
        yield (next_key, chunk)
