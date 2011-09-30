from couchdbkit.ext.django import schema


class Document(schema.Document):
    @property
    def id(self):
        """
        Django templates do not allow access properties that starts with '_'::

            TemplateSyntaxError at /

                Variables and attributes may not begin with underscores: 'document._id'

        This method allows to access id without '_'.

        """
        return self._id
