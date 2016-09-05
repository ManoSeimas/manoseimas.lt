# coding: utf-8
from django.contrib import admin

from manoseimas.compatibility_test import models
from manoseimas.compatibility_test import services


class VotingInline(admin.TabularInline):
    model = models.TopicVoting
    raw_id_fields = [
        'voting',
    ]


class ArgumentInline(admin.TabularInline):
    model = models.Argument


class TestGroupTopicsInline(admin.TabularInline):
    model = models.TestGroup.topics.through
    raw_id_fields = [
        'topic',
    ]
    min_num = 1
    extra = 0
    verbose_name = 'Temų grupė'
    verbose_name_plural = 'Temų grupės'


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    list_filter = ('groups__test',)
    change_form_template = 'admin_topic.jade'
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        TestGroupTopicsInline,
        ArgumentInline,
        VotingInline,
    ]

    def save_related(self, request, form, formsets, change):
        super(TopicAdmin, self).save_related(request, form, formsets, change)
        services.update_topic_positions(services.get_topic_positions())


class TestGroupInline(admin.TabularInline):
    model = models.TestGroup
    raw_id_fields = [
        'topics',
    ]


class CompatTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    inlines = [TestGroupInline]


class TestGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'test')
    exclude = ('topics',)


class UserResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'result')


admin.site.register(models.CompatTest, CompatTestAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.TestGroup, TestGroupAdmin)
admin.site.register(models.UserResult, UserResultAdmin)