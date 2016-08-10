# coding: utf-8

from __future__ import unicode_literals

from django.conf import settings
from django.core import management

from django_webtest import WebTest

from manoseimas.scrapy.spiders.mps import MpsSpider
from manoseimas.scrapy.spiders.sittings import SittingsSpider
from manoseimas.scrapy.spiders.stenograms import StenogramSpider
from manoseimas.scrapy.pipelines import ManoseimasPipeline
from manoseimas.scrapy.pipelines import ManoSeimasModelPersistPipeline
from manoseimas.scrapy.tests.utils import crawl
from manoseimas.compatibility_test.factories import TopicFactory, compatibility_test_factory
from manoseimas.mps_v2.models import ParliamentMember


class TestRecomputeStats(WebTest):

    def test_recompute_stats(self):
        crawl(
            Pipeline=ManoSeimasModelPersistPipeline, spider=MpsSpider(),
            param='p_asm_id', method='parse_person', path='mp_%s.html', urls=[
                'http://www3.lrs.lt/pls/inter/w5_show?p_r=6113&p_k=1&p_a=5&p_asm_id=53911&p_kade_id=6',
            ],
        )

        crawl(
            Pipeline=ManoseimasPipeline, spider=SittingsSpider(),
            param='p_svarst_kl_stad_id', method='parse_question', path='questions/%s.html', urls=[
                'http://www3.lrs.lt/pls/inter/w5_sale_new.klaus_stadija?p_svarst_kl_stad_id=-9209',
            ],
        )

        crawl(
            Pipeline=ManoseimasPipeline, spider=SittingsSpider(),
            param='p_bals_id', method='parse_person_votes', path='votings/%s.html', urls=[
                'http://www3.lrs.lt/pls/inter/w5_sale_new.bals?p_bals_id=-10765',
            ],
        )

        crawl(
            Pipeline=ManoSeimasModelPersistPipeline, spider=StenogramSpider(),
            param='p_id', method='parse_stenogram', path='stenogram_%s.html', urls=[
                'http://www3.lrs.lt/pls/inter2/dokpaieska.showdoc_l?p_id=395116',
            ],
        )

        management.call_command('recompute_stats', verbosity=0)

        resp = self.app.get('/json/fractions/')
        self.assertEqual(resp.json, {'items': [{
            'avg_discussion_contribution_percentage': 0.0,
            'avg_long_statement_count': None,
            'avg_passed_law_project_ratio': 0.0,
            'avg_statement_count': None,
            'avg_vote_percentage': 50.0,
            'logo_url': '/static/img/fractions/fraction-default.png',
            'member_count': 1,
            'name': 'Liberalų ir centro sąjungos frakcija',
            'slug': 'liberalu-ir-centro-sajungos-frakcija',
            'type': 'fraction',
            'url': '/mp/fractions/liberalu-ir-centro-sajungos-frakcija/'
        }]})

        def _get_positions(mp):
            mp = ParliamentMember.objects.get(pk=mp.pk)
            return {int(k): float(v) for k, v in mp.positions.items()}

        mp = ParliamentMember.objects.get(source_id='53911p')

        # Check if MP positions where updated
        self.assertEqual(_get_positions(mp), {})

        # Try to update MP positions manually
        term = settings.PARLIAMENT_TERMS['2008-2012']
        topic = TopicFactory(name='Aukštojo mokslo reforma')
        compatibility_test_factory(term, topic, [('53911p', mp.fraction.abbr, mp.first_name, mp.last_name, [1, 2])])
        self.assertEqual(_get_positions(mp), {topic.pk: 1.5})

        # Try to update MP positions via recompute_stats management command
        management.call_command('recompute_stats', verbosity=0)
        self.assertEqual(_get_positions(mp), {topic.pk: 1.5})
