from django.contrib import admin

from manoseimas.mps_v2.models import ParliamentMember, GroupMembership, Group
from manoseimas.mps_v2.models import PoliticalParty


class GroupAdmin(admin.ModelAdmin):
    list_filter = ('type',)


class MpMembershipAdmin(admin.TabularInline):
    model = ParliamentMember.groups.through
    fk_name = 'member'


class ParliamentMemberAdmin(admin.ModelAdmin):
    inlines = (MpMembershipAdmin,)


admin.site.register(ParliamentMember, ParliamentMemberAdmin)
admin.site.register(GroupMembership)
admin.site.register(Group, GroupAdmin)
admin.site.register(PoliticalParty)
