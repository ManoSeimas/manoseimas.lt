

class NoCacheInitialURLMiddleware(object):

    def is_initial_request(self, request):
        return not bool(request.headers.get('Referer'))

    def process_request(self, request, spider):
        if self.is_initial_request(request):
            request.meta['_no_cache'] = True

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass
