from couchdbkit.exceptions import ResourceNotFound
from couchdbkit.ext.django import schema


class LegalAct(schema.Document):
    name = schema.StringProperty()

    @classmethod
    def search(cls, params, limit=25, **kw):
        starts = params['query']
        ends = starts + 'Z'
        return cls.view('_all_docs', limit=limit, **kw)[starts:ends]

    def current_version(self):
        try:
            return self.fetch_attachment('current_version.html')
        except ResourceNotFound:
            return self.original_version()

    def original_version(self):
        try:
            return self.fetch_attachment('original_version.html')
        except ResourceNotFound:
            return u''
