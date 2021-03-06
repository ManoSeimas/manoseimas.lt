# -*- coding: utf-8 -*-
import os.path
import StringIO
import unittest
import datetime

from django.conf import settings

from scrapy.http import HtmlResponse

from ..items import Person
from ..pipelines import ManoseimasPipeline, LobbyistNameMatcher
from ..spiders.mps import MpsSpider
from manoseimas.scrapy import models

from .utils import fixture


class FakePipeline(ManoseimasPipeline):
    def __init__(self, *args, **kwargs):
        self._stored_items = {}
        super(FakePipeline, self).__init__(*args, **kwargs)

    def get_doc(self, db, item):
        return self._stored_items.get(item['_id'], None)

    def store_item(self, db, doc, item):
        self._stored_items[item['_id']] = doc


class TestPipeline(unittest.TestCase):

    def test_pipline(self):
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

        # content_type = mimetypes.guess_type('photo.png')[0]
        item['_attachments'] = [
            ('avatar', StringIO.StringIO('attachment content'), 'image/png')
        ]

        self.assertFalse(models.Person.objects.filter(key=item['_id']).exists())

        pipeline = ManoseimasPipeline()
        pipeline.process_item(item, None)

        doc = models.Person.objects.get(key=item['_id'])
        doc.updated -= datetime.timedelta(minutes=5)
        doc.save()
        rev = doc.updated

        # Update same item once again, document revision must be different.
        pipeline.process_item(item, None)
        doc = models.Person.objects.get(key=item['_id'])
        self.assertNotEqual(rev, doc.updated)

        with open(os.path.join(settings.MEDIA_ROOT, 'attachments', 'person', str(doc.pk), 'avatar')) as f:
            content = f.read()
        self.assertEqual(content, 'attachment content')

        doc.delete()

    def test_pipline_from_spider(self):
        spider = MpsSpider()
        url = ('http://www3.lrs.lt/pls/inter/w5_show?'
               'p_r=6113&p_k=1&p_a=5&p_asm_id=48690&p_kade_id=6')
        response = HtmlResponse(url, body=fixture('mp_48690.html'))

        items = list(spider.parse_person(response))
        item = items[0]

        pipeline = ManoseimasPipeline()
        pipeline.process_item(item, spider)


class TestLobbyistNameMatcher(unittest.TestCase):

    def test_canonical_name(self):
        canonical_name = LobbyistNameMatcher.canonical_name
        self.assertEqual(canonical_name(u"Vardenis Pavardenis"), u"VARDENIS PAVARDENIS")
        self.assertEqual(canonical_name(u"UAB „Bendrovė“"), u"UAB BENDROVĖ")
        self.assertEqual(canonical_name(u'UAB "INLINEN"'), u"UAB INLINEN")
        self.assertEqual(canonical_name(u'UAB “GLAXOSMITHKLINE LIETUVA”'), u"UAB GLAXOSMITHKLINE LIETUVA")
