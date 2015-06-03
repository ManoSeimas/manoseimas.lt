import tqdm

from django.core.management.base import BaseCommand

import manoseimas.common.utils.words as words_utils
import manoseimas.mps_v2.models as mpsv2_models


class Command(BaseCommand):
    help = 'Procompute word counts for stenogram statements'

    def handle(self, **options):
        total = mpsv2_models.StenogramStatement.objects.count()
        statements = mpsv2_models.StenogramStatement.objects.all()
        for statement in tqdm.tqdm(statements):
            statement.word_count = words_utils.get_word_count(statement.text)
            statement.save()

        self.stdout.write(
            'Successfully updated word counts for %d statements.' % total
        )
