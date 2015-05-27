import string

from urlparse import urljoin

from scrapy.contrib.loader import processor, ItemLoader
from scrapy.selector import Selector


class Loader(ItemLoader):
    default_input_processor = processor.MapCompose(string.strip)
    default_output_processor = processor.Join()

    def __init__(self, spider, response, *args, **kw):
        self.spider = spider
        self.response = kw['response'] = response
        self.required = kw.pop('required', tuple())
        super(Loader, self).__init__(*args, **kw)

    def reset_required(self, *args):
        self.required = args

    def load_item(self):
        """
        Checks if all required fields exists.

        """
        missing = []
        for field_name in self.required:
            if field_name not in self._values:
                missing.append(field_name)

        item = super(Loader, self).load_item()

        if missing:
            self.spider.error(
                self.response,
                "Missing fields: '%s' in %s" % ("', '".join(missing), item)
            )

        return item


def absolute_url(value, loader_context=None):
    response = loader_context['response']
    xs = Selector(response)
    base_url = xs.xpath('//base/@href').extract()
    base_url = (urljoin(response.url, base_url[0].encode(response.encoding))
                if base_url else response.url)
    return urljoin(base_url, ''.join(value))
