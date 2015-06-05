from collections import namedtuple

from django.core.management.base import BaseCommand
from django.db import transaction

from manoseimas.mps_v2 import models


ItemStats = namedtuple('ItemStats',
                       ('id', 'statement_count', 'long_statement_count',
                        'votes', 'discusion_contribution_percentage'))


class Command(BaseCommand):
    help = 'Recompute MP and Fraction stats'

    def rank_members(self, data, key_fn=lambda e: e[0], val_fn=lambda e: e[1]):
        ordered = sorted(data, key=val_fn, reverse=True)
        return tuple((key_fn(item), rank + 1)
                     for rank, item in enumerate(ordered))

    def save_rankings(self, rank_cls, items, stats):
        ranks = {}
        for i in range(1, len(stats[0])):
            ranked = self.rank_members(stats, val_fn=lambda e: e[i])
            ranks['{}_rank'.format(ItemStats._fields[i])] = dict(ranked)
        for item in items:
            ranking, created = rank_cls.objects.get_or_create(
                target=item)
            for key, rank in ranks.items():
                setattr(ranking, key, rank[item.id])
            ranking.save()

    @transaction.atomic
    def handle(self, **options):

        def mean(items):
            return float(sum(items)) / len(items) if items else 0.0

        mps = models.ParliamentMember.objects.all()
        stats = [ItemStats(mp.id,
                           mp.get_statement_count(),
                           mp.get_long_statement_count(),
                           mp.get_discussion_contribution_percentage(),
                           sum(mp.votes.values()) if mp.votes else 0)
                 for mp in mps]
        self.save_rankings(models.MPRanking, mps, stats)

        fractions = models.Group.objects.filter(
            type=models.Group.TYPE_FRACTION
        )
        fraction_stats = [
            ItemStats(
                fraction.id,
                mean(map(models.ParliamentMember.get_statement_count,
                         fraction.active_members)),
                mean(map(models.ParliamentMember.get_long_statement_count,
                         fraction.active_members)),
                mean(map(
                     models.ParliamentMember.get_discussion_contribution_percentage,  # noqa
                     fraction.active_members
                )),
                mean(map(lambda mp: sum(mp.votes.values()
                                        if mp.votes else 0),
                         fraction.active_members))
            ) for fraction in fractions
        ]
        self.save_rankings(models.GroupRanking, fractions, fraction_stats)
