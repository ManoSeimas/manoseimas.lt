import requests

from scrapy.http.response.html import HtmlResponse

from manoseimas.scrapy.models import Voting
from manoseimas.scrapy.pipelines import ManoseimasPipeline
from manoseimas.scrapy.spiders.sittings import SittingsSpider


def get_voting_by_source_id():
    pass


def get_voting_by_lrslt_url():
    pass


def get_recent_votings():
    pass


def _fetch(url):
    r = requests.get(url)
    return HtmlResponse(r.url, body=r.content)


def crawl_voting(source):
    spider = SittingsSpider(resume='no', start_url=source)

    # Parse voting
    response = _fetch(source)
    items = list(spider.parse_person_votes(response))
    voting_id = items[-1]['_id']

    # Parse question
    question_url = spider.get_question_url(response)[0]
    response = _fetch(question_url)
    items.extend(list(spider.parse_question(response)))

    pipeline = ManoseimasPipeline()
    for item in items:
        pipeline.process_item(item, spider)
    voting = Voting.objects.get(key=voting_id)
    return voting
