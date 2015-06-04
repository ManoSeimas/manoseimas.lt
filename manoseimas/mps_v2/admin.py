from django.contrib import admin

from manoseimas.mps_v2.models import ParliamentMember, GroupMembership, Group
from manoseimas.mps_v2.models import PoliticalParty
from manoseimas.mps_v2.models import Stenogram, StenogramTopic
from manoseimas.mps_v2.models import StenogramStatement


class GroupAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    readonly_fields = ('slug',)


class MpMembershipAdmin(admin.TabularInline):
    model = ParliamentMember.groups.through
    fk_name = 'member'


class ParliamentMemberAdmin(admin.ModelAdmin):
    inlines = (MpMembershipAdmin,)


class StenogramStatementInline(admin.TabularInline):
    model = StenogramStatement
    readonly_fields = ('source', 'speaker', 'speaker_name', 'text')
    extra = 0


class StenogramTopicInline(admin.TabularInline):
    model = StenogramTopic
    readonly_fields = ('source', 'title')
    extra = 0


class StenogramAdmin(admin.ModelAdmin):
    inlines = (StenogramTopicInline,)


class StenogramTopicAdmin(admin.ModelAdmin):
    inlines = (StenogramStatementInline,)


admin.site.register(ParliamentMember, ParliamentMemberAdmin)
admin.site.register(GroupMembership)
admin.site.register(Group, GroupAdmin)
admin.site.register(PoliticalParty)
admin.site.register(Stenogram, StenogramAdmin)
admin.site.register(StenogramTopic, StenogramTopicAdmin)
admin.site.register(StenogramStatement)
