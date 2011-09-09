from couchdbkit.ext.django import schema


class CouchDb(schema.Document):
    @property
    def id(self):
        """
        Django templates do not allow access properties that starts with '_'::

            TemplateSyntaxError at /

                Variables and attributes may not begin with underscores: 'document._id'

        This method allows to access id without '_'.

        """
        return self._id


class Document(CouchDb):
    name = schema.StringProperty()

    @classmethod
    def by_number(cls, **kw):
        return cls.view('documents/by_number', include_docs=True, **kw)

    @classmethod
    def search(cls, params, limit=10, **kw):
        starts = params['query']
        ends = starts + 'Z'
        return cls.by_number(limit=limit, **kw)[starts:ends]
