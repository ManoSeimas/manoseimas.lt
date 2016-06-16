from django.contrib import admin

from manoseimas.scrapy.models import Question
from manoseimas.scrapy.models import Person
from manoseimas.scrapy.models import Voting
from manoseimas.scrapy.models import PersonVote


class VotingAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'timestamp', 'documents', 'votes', 'source')
    search_fields = ('=source',)

    def title(self, obj):
        return obj.get_title()

    def documents(self, obj):
        return len(obj.value['documents'])

    def votes(self, obj):
        return len(obj.value['votes']) if 'votes' in obj.value else None


admin.site.register(Question)
admin.site.register(Person)
admin.site.register(Voting, VotingAdmin)
admin.site.register(PersonVote)
