from django.contrib import admin

from manoseimas.compatibility_test.models import CompatTest
from manoseimas.compatibility_test.models import Topic
from manoseimas.compatibility_test.models import TopicVoting
from manoseimas.compatibility_test.models import Argument
from manoseimas.compatibility_test.models import TestGroup


class VotingInline(admin.TabularInline):
    model = TopicVoting


class ArgumentInline(admin.TabularInline):
    model = Argument


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    inlines = [
        ArgumentInline,
        VotingInline
    ]


class TestGroupInline(admin.TabularInline):
    model = TestGroup


class CompatTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    inlines = [TestGroupInline]


class TestGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(CompatTest, CompatTestAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TestGroup, TestGroupAdmin)
