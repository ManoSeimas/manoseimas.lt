from zope.component import adapts
from zope.component import provideAdapter
from sboard.profiles.interfaces import IProfile
from sboard.profiles.nodes import ProfileView
from manoseimas.compat.models import PersonPosition
from manoseimas.mps.nodes import classify_position
from manoseimas.mps.nodes import format_position_percent

class ManoseimasProfileView(ProfileView):
    adapts(IProfile)
    template = 'sboard/profile.html'

    def render(self, **overrides):
        positions = list(PersonPosition.objects.filter(profile=self.node))
        positions.sort(key=lambda pp: pp.node.ref.title)
        context = {
            'positions': [{
                'solution': pp.node,
                'position': classify_position(pp.position),
                'percent': format_position_percent(pp),
            } for pp in positions],
        }
        context.update(overrides)
        return super(ManoseimasProfileView, self).render(**context)

provideAdapter(ManoseimasProfileView)
