from compressor.filters.base import FilterBase

from react.jsx import JSXTransformer


class JSXCompiler(FilterBase):

    def __init__(self, content, attrs=None, filter_type=None, charset=None,
                 filename=None):
        super(JSXCompiler, self).__init__(content, filter_type, filename)
        self.transformer = JSXTransformer()

    def input(self, **kwargs):
        if self.filename:
            return self.transformer.transform(self.filename)
        else:
            return self.transformer.transform_string(self.content)
