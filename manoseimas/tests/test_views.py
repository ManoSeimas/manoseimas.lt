# coding: utf-8

from __future__ import unicode_literals

from django_webtest import WebTest

from manoseimas.scrapy.spiders.mps import MpsSpider
from manoseimas.scrapy.spiders.sittings import SittingsSpider
from manoseimas.scrapy.pipelines import ManoseimasPipeline, ManoSeimasModelPersistPipeline
from manoseimas.scrapy.tests.utils import crawl
from manoseimas.scrapy.models import Voting


class TestViews(WebTest):

    maxDiff = None

    def test_votings(self):
        self.app.get('/votings/')

    def test_widget(self):
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

        voting = Voting.objects.order_by('pk').last()

        self.app.get('/widget/?voting_id=%s' % voting.key)
        resp = self.app.get('/widget/data/voting/%s' % voting.key)
        self.assertEqual(resp.json['fractions']['JF'], {
            '_id': 'JF',
            'image': None,
            'source': None,
            'abbreviation': 'JF',
            'slug': 'jungtine-liberalu-ir-centro-sajungos-ir-tautos-prisikelimo-partijos-frakcija',
            'title': 'Jungtinė (Liberalų ir centro sąjungos ir Tautos prisikėlimo partijos) frakcija',
        })
        self.assertEqual(resp.json['mps']['53911p'], {
            '_id': '53911p',
            'first_name': 'Antanas',
            'fraction': 'JF',
            'image': None,
            'last_name': 'Nedzinskas',
            'slug': 'antanas-nedzinskas',
            'source': {'id': '53911p', 'name': 'lrslt', 'url': None},
            'title': 'Antanas Nedzinskas',
        })
        self.assertEqual(resp.json['voting']['_id'], '-10765v')
        self.assertEqual(resp.json['voting']['votes']['abstain'], [
            ['53924p', 'LSF'],
            ['63p', 'TSLKDF'],
            ['53902p', 'JF'],
        ])
