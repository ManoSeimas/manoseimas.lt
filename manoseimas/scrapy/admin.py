from django.contrib import admin

from manoseimas.scrapy import services
from manoseimas.scrapy.models import Question
from manoseimas.scrapy.models import Person
from manoseimas.scrapy.models import Voting
from manoseimas.scrapy.models import PersonVote


class VotingAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'timestamp', 'documents', 'votes', 'source')
    search_fields = ('source',)

    def title(self, obj):
        return obj.get_title()

    def documents(self, obj):
        return len(obj.value['documents'])

    def votes(self, obj):
        return len(obj.value['votes']) if 'votes' in obj.value else None

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['fields'] = ('source',)
        return super(VotingAdmin, self).get_form(request, obj, **kwargs)

    def save_form(self, request, form, change):
        if change:
            return super(VotingAdmin, self).save_form(request, form, change)
        source = form.cleaned_data['source']
        return services.crawl_voting(source)

    def save_model(self, request, obj, form, change):
        if change:
            return super(VotingAdmin, self).save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        if change:
            return super(VotingAdmin, self).save_related(request, form, formsets, change)


class PersonVoteAdmin(admin.ModelAdmin):
    list_display = ('p_asm_id', 'name', 'vote', 'value', 'fraction')
    list_filter = ('name',)


admin.site.register(Question)
admin.site.register(Person)
admin.site.register(Voting, VotingAdmin)
admin.site.register(PersonVote, PersonVoteAdmin)
