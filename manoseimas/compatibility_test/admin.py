from django.contrib import admin
from manoseimas.compatibility_test.models import CompatTest
from manoseimas.compatibility_test.models import PoliticalTopic
from manoseimas.compatibility_test.models import Argument
from manoseimas.compatibility_test.models import Voting
from manoseimas.compatibility_test.models import TestGroup


class VotingInline(admin.TabularInline):
    model = Voting


class ArgumentInline(admin.TabularInline):
    model = Argument


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'test')
    list_filter = ('name',)
    inlines = [
        ArgumentInline,
        VotingInline
    ]


class TopicInline(admin.TabularInline):
    model = PoliticalTopic


class CompatTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    inlines = [
        TopicInline,
    ]

admin.site.register(CompatTest, CompatTestAdmin)
admin.site.register(PoliticalTopic, TopicAdmin)
admin.site.register(TestGroup)
