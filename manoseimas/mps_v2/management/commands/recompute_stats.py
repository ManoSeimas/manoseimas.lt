from collections import namedtuple

from tqdm import tqdm
from toposort import toposort_flatten

from django.core.management.base import BaseCommand
from django.db import transaction
from django.apps import apps

from manoseimas.mps_v2 import models


ItemStats = namedtuple('ItemStats',
                       ('id', 'statement_count', 'long_statement_count',
                        'votes', 'discusion_contribution_percentage',
                        'passed_law_project_ratio'))


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

    def sort_precomp_models(self, model_classes):
        reverse = {cls.__name__: cls for cls in model_classes}
        deps = {cls.__name__: set(getattr(cls,
                                          'precomputation_depends_on',
                                          tuple()))
                for cls in model_classes}
        ordered = toposort_flatten(deps)
        return map(lambda name: reverse[name], ordered)

    def compute_precomputed_fields(self, options):
        model_classes = self.sort_precomp_models(filter(
            lambda model_cls: getattr(model_cls, 'precomputed_fields', None),
            apps.get_models()
        ))
        for model_cls in model_classes:
            if hasattr(model_cls, 'precomputation_filter'):
                objects = model_cls.objects.filter(
                    **model_cls.precomputation_filter
                )
            else:
                objects = model_cls.objects.all()
            if options['verbosity'] > 0:
                self.stdout.write('Computing fields for {}'.format(model_cls.__name__))
            objects_iter = tqdm(objects) if options['verbosity'] > 0 else objects
            for object in objects_iter:
                for field, compute_fn in model_cls.precomputed_fields:
                    if callable(compute_fn):
                        value = compute_fn()
                    else:
                        compute_fn_callable = getattr(object, compute_fn)
                        if not callable(compute_fn_callable):
                            raise ValueError(
                                'Compute function {} for {}.{}'
                                ' does not exist.'.format(compute_fn,
                                                          model_cls,
                                                          field)
                            )
                        value = compute_fn_callable()

                    setattr(object, field, value)
                object.save()

    # XXX Might be a bad idea to hold a xact with write locks for a minute.
    @transaction.atomic
    def handle(self, **options):

        if options['verbosity'] > 0:
            self.stdout.write('Computing precomputed model fields')
        self.compute_precomputed_fields(options)

        if options['verbosity'] > 0:
            self.stdout.write('Computing MP rankings...')
        mps = models.ParliamentMember.objects.all()
        mps_iter = tqdm(mps) if options['verbosity'] > 0 else mps
        stats = [ItemStats(mp.id,
                           mp.statement_count,
                           mp.long_statement_count,
                           mp.vote_percentage,
                           mp.discussion_contribution_percentage,
                           mp.passed_law_project_ratio)
                 for mp in mps_iter]
        self.save_rankings(models.MPRanking, mps, stats)

        if options['verbosity'] > 0:
            self.stdout.write('Computing Fraction rankings...')
        fractions = models.Group.objects.filter(
            type=models.Group.TYPE_FRACTION
        )
        fractions_iter = tqdm(fractions) if options['verbosity'] > 0 else fractions
        fraction_stats = [
            ItemStats(
                fraction.id,
                fraction.avg_statement_count,
                fraction.avg_long_statement_count,
                fraction.avg_vote_percentage,
                fraction.avg_discussion_contribution_percentage,
                fraction.avg_passed_law_project_ratio,
            ) for fraction in fractions_iter
        ]
        self.save_rankings(models.GroupRanking, fractions, fraction_stats)
