from django.contrib import admin

from manoseimas.mps_v2.models import ParliamentMember, GroupMembership, Group
from manoseimas.mps_v2.models import PoliticalParty


class GroupAdmin(admin.ModelAdmin):
    list_filter = ('type',)


admin.site.register(ParliamentMember)
admin.site.register(GroupMembership)
admin.site.register(Group, GroupAdmin)
admin.site.register(PoliticalParty)
