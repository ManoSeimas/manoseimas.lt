import json

from django.core.management.base import BaseCommand
from django.db import transaction

from manoseimas.compatibility_test.models import TopicVoting
from manoseimas.scrapy.models import Voting


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('source_file')

    @transaction.atomic
    def handle(self, **options):
        filename = options['source_file']
        with open(filename, 'rb') as f:
            topicvotings = json.load(f)
        # delete topicvotings, they're likely invalid.
        TopicVoting.objects.all().delete()
        for tv in topicvotings:
            voting = Voting.objects.get(source=tv['voting_url'])
            topicvoting = TopicVoting(topic_id=tv['topic_id'],
                                      factor=tv['factor'],
                                      voting=voting)
            topicvoting.save()
