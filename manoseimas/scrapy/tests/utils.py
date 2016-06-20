import json
import os.path

from six.moves.urllib.parse import urlparse
from six.moves.urllib.parse import parse_qsl

from scrapy.http import HtmlResponse


def fixture(name, raw=False):
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'fixtures', name)) as f:
        if not raw and name.endswith(".json"):
            return json.loads(f.read())
        else:
            return f.read()


def crawl(Pipeline, spider, param, method, path, urls):
    pipeline = Pipeline()
    pipeline.open_spider(spider)
    for url in urls:
        query = dict(parse_qsl(urlparse(url).query))

        if param not in query:
            raise ValueError('Unknonw url: %s' % url)

        response = HtmlResponse(url, body=fixture(path % query[param]))
        for item in getattr(spider, method)(response):
            pipeline.process_item(item, None)
