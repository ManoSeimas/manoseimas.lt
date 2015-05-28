# Will be renamed to scrapy.extensions.httpcache in 0.25
from scrapy.contrib.httpcache import DummyPolicy


class NoCacheFlagPolicy(DummyPolicy):

    def should_cache_request(self, request):
        return (super(NoCacheFlagPolicy, self).should_cache_request(request)
                and not request.meta.get('_no_cache', False))

    def should_cache_response(self, response, request):
        should_cache = super(NoCacheFlagPolicy, self).should_cache_response(
            response,
            request
        )
        return should_cache and not request.meta.get('_no_cache', False)

    def is_cached_response_valid(self, cachedresponse, response, request):
        return request.meta.get('_no_cache', False)
