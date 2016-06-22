from django.contrib import admin

from manoseimas.compatibility_test import models


class VotingInline(admin.TabularInline):
    model = models.TopicVoting
    raw_id_fields = [
        'voting',
    ]


class ArgumentInline(admin.TabularInline):
    model = models.Argument


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    inlines = [
        ArgumentInline,
        VotingInline
    ]


class TestGroupInline(admin.TabularInline):
    model = models.TestGroup


class CompatTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    inlines = [TestGroupInline]


class TestGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(models.CompatTest, CompatTestAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.TestGroup, TestGroupAdmin)
