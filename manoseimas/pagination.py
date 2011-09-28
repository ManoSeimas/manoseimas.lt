import urllib

from couchdbkit.client import ViewResults

DEFAULT_NAMES = ('key', 'docid', 'prev')


class CouchDbPaginator(ViewResults):
    def __init__(self, view, page=None, **options):
        self.names = options.get('names', {})
        for name in DEFAULT_NAMES:
            self.names.setdefault(name, name)

        self.rows_per_page = options.get('rows_per_page', 25)

        page = page or {}
        key = page.get('key')
        docid = page.get('docid')
        prev = page.get('prev', False)

        params = view.params.copy()
        params.update(dict(limit=self.rows_per_page+1, descending=prev,
                           startkey=key, startkey_docid=docid))

        super(CouchDbPaginator, self).__init__(view.view, **params)
        self.fetch()

        if prev:
            self._result_cache['rows'].reverse()

        self.prev_row = self.next_row = None

        if len(self._result_cache['rows']) > 0 and key:
            self.prev_row = self._result_cache['rows'][0]

        if len(self._result_cache['rows']) > self.rows_per_page:
            self.next_row = self._result_cache['rows'].pop()

    def _get_page_url(self, page, prev=False):
        qry = {
            self.names['key']: page['key'].encode('utf-8'),
            self.names['docid']: page['id'].encode('utf-8'),
        }
        if prev:
            qry['prev'] = True
        return '?' + urllib.urlencode(qry)

    def has_next_page(self):
        return bool(self.next_row)

    def has_prev_page(self):
        return bool(self.prev_row)

    def get_next_page_url(self):
        if self.next_row:
            return self._get_page_url(self.next_row)
        else:
            return None

    def get_prev_page_url(self):
        if self.prev_row:
            return self._get_page_url(self.prev_row, prev=True)
        else:
            return None

    __getitem__ = None
