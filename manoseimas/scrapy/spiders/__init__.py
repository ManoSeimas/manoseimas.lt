import urlparse

from scrapy import log
from scrapy.contrib.spiders import CrawlSpider


class ManoSeimasSpider(CrawlSpider):
    def _get_query_attr(self, url, key):
        return urlparse.parse_qs(urlparse.urlparse(url).query)[key][0]

    def _get_source(self, url, key):
        return {
            'id': unicode(self._get_query_attr(url, key)),
            'url': unicode(url),
            'name': u'lrslt',
        }

    def error(self, response, msg):
        s = {
            'msg': msg,
            'url': response.url,
        }
        self.log('%(msg)s, %(url)s' % s, level=log.ERROR)
