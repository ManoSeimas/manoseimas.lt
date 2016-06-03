import urlparse

from six import text_type

from scrapy import log
from scrapy.contrib.spiders import CrawlSpider
from manoseimas.scrapy.loaders import absolute_url


class ManoSeimasSpider(CrawlSpider):
    def _get_query_attr(self, url, key):
        return urlparse.parse_qs(urlparse.urlparse(url).query)[key][0]

    def _get_source_absolute_url(self, response, url, key):
        return {
            'id': text_type(self._get_query_attr(url, key)),
            'url': text_type(absolute_url([url], {'response': response})),
            'name': u'lrslt',
        }

    def _get_source(self, url, key):
        return {
            'id': text_type(self._get_query_attr(url, key)),
            'url': text_type(url),
            'name': u'lrslt',
        }

    def error(self, response, msg):
        s = {
            'msg': msg,
            'url': response.url,
        }
        self.log('%(msg)s, %(url)s' % s, level=log.ERROR)


def mark_no_cache(request):
    request.meta['_no_cache'] = True
    return request
