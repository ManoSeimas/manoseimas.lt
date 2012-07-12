from zope.component import adapts
from zope.component import provideAdapter
from sboard.profiles.interfaces import IProfile
from sboard.profiles.nodes import ProfileView
from manoseimas.compat.models import PersonPosition
from manoseimas.mps.nodes import prepare_position_list

class ManoseimasProfileView(ProfileView):
    adapts(IProfile)
    template = 'sboard/profile.html'

    def render(self, **overrides):
        context = {
            'positions': prepare_position_list(self.node),
        }
        context.update(overrides)
        return super(ManoseimasProfileView, self).render(**context)

provideAdapter(ManoseimasProfileView)
