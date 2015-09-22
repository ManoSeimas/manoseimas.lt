# coding: utf-8
from zope.component import adapts
from zope.component import provideAdapter
from django.utils.translation import ugettext as _
from sboard.profiles.interfaces import IProfile
from sboard.profiles.nodes import ProfileView
from manoseimas.compat.models import PersonPosition


USER_POSITION_NAMES = {
    -2: _('Tikrai ne'),
    -1: _('Ne'),
    1: _('Taip'),
    2: _('Tikrai taip'),
}


class ManoseimasProfileView(ProfileView):
    adapts(IProfile)
    template = 'sboard/profile.html'

    def render(self, **overrides):
        if self.request.user.id == self.node.uid:
            positions = [{
                'solution': pp.node,
                'val': int(pp.position),
                'text': USER_POSITION_NAMES[int(pp.position)],
            } for pp in PersonPosition.objects.filter(profile=self.node)]
            positions.sort(key=lambda p: p['solution'].ref.title)
        else:
            positions = None

        context = {
            'positions': positions,
            'position_mapping': USER_POSITION_NAMES,
        }
        context.update(overrides)
        return super(ManoseimasProfileView, self).render(**context)

provideAdapter(ManoseimasProfileView)
