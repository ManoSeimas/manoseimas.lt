import requests
from scrapy.http.response.html import HtmlResponse

from django.contrib import admin

from manoseimas.scrapy.models import Question
from manoseimas.scrapy.models import Person
from manoseimas.scrapy.models import Voting
from manoseimas.scrapy.models import PersonVote
from manoseimas.scrapy.pipelines import ManoseimasPipeline
from manoseimas.scrapy.spiders.sittings import SittingsSpider


def fetch(url):
    r = requests.get(url)
    return HtmlResponse(r.url, body=r.content)


class VotingAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'timestamp', 'documents', 'votes', 'source')
    search_fields = ('=source',)

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
        return self._crawl_voting(source)

    def save_model(self, request, obj, form, change):
        if change:
            return super(VotingAdmin, self).save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        if change:
            return super(VotingAdmin, self).save_related(request, form, formsets, change)

    def _crawl_voting(self, source):
        spider = SittingsSpider(resume='no', start_url=source)

        # Parse voting
        response = fetch(source)
        items = list(spider.parse_person_votes(response))
        voting_id = items[-1]['_id']

        # Parse question
        question_url = spider.get_question_url(response)[0]
        response = fetch(question_url)
        items.extend(list(spider.parse_question(response)))

        pipeline = ManoseimasPipeline()
        for item in items:
            pipeline.process_item(item, spider)
        voting = Voting.objects.get(key=voting_id)
        return voting


admin.site.register(Question)
admin.site.register(Person)
admin.site.register(Voting, VotingAdmin)
admin.site.register(PersonVote)
