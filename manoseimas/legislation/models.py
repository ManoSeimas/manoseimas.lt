from django.utils.safestring import mark_safe

from couchdbkit.ext.django import schema

from sboard.models import Node


class LegalAct(Node):
    # A legal act marker.
    is_legal_act = schema.BooleanProperty(default=True)

    # Legal act number, i.e.: I-1222
    number = schema.StringProperty()

    # Lower case name with stripped spaces. This name is used to find relations
    # between legal acts.
    cleaned_name = schema.StringProperty()

    def render_body(self):
        return mark_safe(self.get_body())


class Law(LegalAct):
    """Main Law nodel model.

    ID of this node is slugified name.

    """
    _default_importance = 7


class LawChange(LegalAct):
    """Law that changes an existing law.

    ID of this node is UUID.

    """
    pass


class LawProject(LegalAct):
    """Law project node model.

    ID of this node is UUID.

    """
    pass
