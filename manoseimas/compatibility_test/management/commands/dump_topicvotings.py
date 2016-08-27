import json

from django.core.management.base import BaseCommand
from django.db import transaction

from manoseimas.compatibility_test.models import TopicVoting


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('dest_file')

    @transaction.atomic
    def handle(self, **options):
        topic_votings = TopicVoting.objects.select_related()
        dump = [{'topic_id': tv.topic_id,
                 'voting_url': tv.voting.source,
                 'factor': tv.factor} for tv in topic_votings]
        with open(options['dest_file'], 'wb') as f:
            json.dump(dump, f, indent=4, sort_keys=True)
