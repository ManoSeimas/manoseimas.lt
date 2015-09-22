import re
import cgi

from docutils.parsers.rst import roles
from docutils import nodes


# Define description role for docutils.
DESCRIPTION_RE = re.compile(r'^(.*?) \((.*)\)$')
def description_role(role, rawtext, text, lineno, inliner,
                     options={}, content=[]):

    match = DESCRIPTION_RE.match(text)
    if not match:
        msg = inliner.reporter.error(
            'Description text should be in the format "Thing (description)"; '
            '"%s" is invalid.' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    thing, description = match.groups()
    html = u'<span class="description" title="%s">%s</span>' % (
        cgi.escape(description),
        cgi.escape(thing),
    )
    options['format'] = 'html'
    roles.set_classes(options)
    node = nodes.raw(rawtext, html, **options)
    node.source, node.line = inliner.reporter.get_source_and_line(lineno)
    return [node], []

roles.register_local_role('description', description_role)
