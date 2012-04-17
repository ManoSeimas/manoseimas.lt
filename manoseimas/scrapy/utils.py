from urlparse import urljoin

from scrapy.utils.response import get_base_url


class Increment(object):
    def __init__(self, nr):
        self.nr = nr

    def __call__(self, step=1):
        self.nr += step
        return self.nr


def get_absolute_url(response, url):
    """
    Returns abosolute URL from given url and response.

    """
    return urljoin(get_base_url(response), url)


def get_first(hxs, xpath):
    """
    Return first item from given HTML XPath Selector object and XPath string.

    If no items found, None will be returned.

    If at least one item is found, first from list will be taken, stripped and
    returned.

    Parameters:

    hxs
        HtmlXPathSelector instance.

    xpath
        XPath string, that will be passed to hxs select method.

    """
    result = hxs.select(xpath).extract()
    if result:
        return result[0].strip()
    else:
        return None


def get_all(hxs, xpath, sep=''):
    result = hxs.select(xpath).extract()
    if result:
        return sep.join(result).strip()
    else:
        return None


def split_by_words(s, idx):
    """
    Splits string of words at specified word index to split.

    >>> split_by_words('a b c', 1)
    ('a', 'b c')
    >>> split_by_words('a b c', -1)
    ('a b', 'c')
    >>> split_by_words('a', -2)
    ('', 'a')

    """
    words = s.split()
    return (' '.join(words[:idx]), ' '.join(words[idx:]))
