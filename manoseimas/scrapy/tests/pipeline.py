import unittest

from couchdbkit import Server
from mock import patch

from scrapy.http import HtmlResponse

from ..items import Person
from ..pipelines import ManoseimasPipeline
from ..pipelines import get_db
from ..spiders.mps import MpsSpider

from .utils import fixture


class FakePipeline(ManoseimasPipeline):
    def __init__(self, *args, **kwargs):
        self._stored_items = {}
        super(FakePipeline, self).__init__(*args, **kwargs)

    def get_doc(self, item_name, item):
        return self._stored_items.get(item['_id'], dict(item))

    def store_item(self, item_name, doc, item):
        self._stored_items[item['_id']] = doc



class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.server = Server()
        self.db = self.server.get_or_create_db('manoseimas_pipline_testdb')

    def tearDown(self):
        self.server.delete_db(self.db.dbname)

    @patch('manoseimas.scrapy.pipelines.get_db')
    def test_pipline(self, mock_get_db):
        mock_get_db.return_value = self.db

        item = Person()

        item['_id'] = '000001'
        item['first_name'] = u'Firstname'
        item['last_name'] = u'Lastname'
        item['dob'] = u'2000-01-01'
        item['email'] = [u'Firstname.Lastname@lrs.lt']
        item['phone'] = [u'2396631']
        item['parliament'] = ['2008-2012', '2004-2008', '2000-2004',
                              '1996-2000', '1990-1992']
        item['groups'] = [
            {
                'type': 'party',
                'name': (u'T\u0117vyn\u0117s s\u0105junga - Lietuvos '
                         u'krik\u0161\u010dionys demokratai'),
            },
            {
                'type': u'committee',
                'name': u'U\u017esienio reikal\u0173 komitetas',
                'membership': [u'2011-12-22', None],
                'position': u'Komiteto narys',
                'source': (u'http://www3.lrs.lt/pls/inter/w5_show?'
                           u'p_r=6113&p_k=1&p_a=6&p_pad_id=44&p_kade_id=6'),
            },
        ]
        item['source'] = {
            'id': u'48690',
            'url': (u'http://www3.lrs.lt/pls/inter/w5_show?'
                    u'p_r=6113&p_k=1&p_a=5&p_asm_id=48690&p_kade_id=6'),
            'name': u'lrslt',
        }

        self.assertFalse(self.db.doc_exist(item['_id']))

        pipeline = ManoseimasPipeline()
        pipeline.process_item(item, None)

        self.assertTrue(self.db.doc_exist(item['_id']))

        doc = self.db.get(item['_id'])
        rev = doc['_rev']

        # Update same item once again, document revision must be different.
        pipeline.process_item(item, None)
        doc = self.db.get(item['_id'])
        self.assertNotEqual(rev, doc['_rev'])

    def test_pipline_from_spider(self):
        spider = MpsSpider()
        url = ('http://www3.lrs.lt/pls/inter/w5_show?'
               'p_r=6113&p_k=1&p_a=5&p_asm_id=48690&p_kade_id=6')
        response = HtmlResponse(url, body=fixture('mp_48690.html'))

        items = list(spider.parse_person(response))
        item = items[0]

        pipeline = ManoseimasPipeline()
        pipeline.process_item(item, spider)


class TestPipelineGetDB(unittest.TestCase):
    @patch('manoseimas.scrapy.pipelines.settings')
    def test_get_db(self, mock_settings):
        settings = {
            'COUCHDB_DATABASES': (
                ('legalacts', 'http://127.0.0.1:5984', 'my_legalacts_testdb',),
                ('person', 'http://127.0.0.1:5984', 'my_person_testdb',),
            )
        }
        mock_settings.__getitem__.side_effect = lambda key: settings[key]

        db = get_db('person', cache=False)
        self.assertEqual(db.dbname, 'my_person_testdb')
        db.server.delete_db(db.dbname)

        db = get_db('legalacts', cache=False)
        self.assertEqual(db.dbname, 'my_legalacts_testdb')
        db.server.delete_db(db.dbname)
