from django.contrib import admin

from manoseimas.mps_v2.models import ParliamentMember, GroupMembership, Group
from manoseimas.mps_v2.models import PoliticalParty


admin.site.register(ParliamentMember)
admin.site.register(GroupMembership)
admin.site.register(Group)
admin.site.register(PoliticalParty)
