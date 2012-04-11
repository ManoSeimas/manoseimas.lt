# Copyright (C) 2012  Mantas Zimnickas <sirexas@gmail.com>
#
# This file is part of manoseimas.lt project.
#
# manoseimas.lt is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# manoseimas.lt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with manoseimas.lt.  If not, see <http://www.gnu.org/licenses/>.

from zope.interface import implements

from django.utils.safestring import mark_safe

from couchdbkit.ext.django import schema

from sboard.factory import provideNode
from sboard.models import Node

from .interfaces import ILaw
from .interfaces import ILawChange
from .interfaces import ILawProject


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

    implements(ILaw)

    _default_importance = 7

provideNode(Law, "law")


class LawChange(LegalAct):
    """Law that changes an existing law.

    ID of this node is UUID.

    """
    implements(ILawChange)

provideNode(LawChange, "lawchange")


class LawProject(LegalAct):
    """Law project node model.

    ID of this node is UUID.

    """
    implements(ILawProject)

provideNode(LawProject, "lawproject")
