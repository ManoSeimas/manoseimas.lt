from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from manoseimas.scrapy.models import Voting
from manoseimas.scrapy.services import crawl_voting


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, **options):
        votings = Voting.objects.all()
        for voting in tqdm(votings):
            crawl_voting(voting.source)
