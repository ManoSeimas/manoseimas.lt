# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

import mock

from scrapy.http import HtmlResponse
from django_webtest import WebTest

from django.core.urlresolvers import reverse

from manoseimas.factories import AdminUserFactory
from manoseimas.scrapy.tests.utils import fixture
from manoseimas.scrapy.models import Voting
from manoseimas.scrapy.models import PersonVote


def _response(path, fragment, item_id):
    url = 'http://www3.lrs.lt/pls/inter/w5_sale_new.%s=%s' % (fragment, item_id)
    return HtmlResponse(url, body=fixture('%s/%s.html' % (path, item_id)))


class TestViews(WebTest):

    @mock.patch('manoseimas.scrapy.services._fetch')
    def test_index_view(self, fetch):
        fetch.side_effect = [
            _response('votings', 'bals?p_bals_id', '-10765'),
            _response('questions', 'klaus_stadija?p_svarst_kl_stad_id', '-9211'),
        ]

        AdminUserFactory()

        url = 'http://www3.lrs.lt/pls/inter/w5_sale_new.bals?p_bals_id=-10765'

        resp = self.app.get(reverse('admin:scrapy_voting_add'), user='admin')
        form = resp.forms['voting_form']
        form['source'] = url
        form.submit('_save')

        voting = Voting.objects.get(source=url)
        self.assertEqual(voting.key, '-10765v')
        self.assertEqual(voting.name, 'dėl pritarimo po pateikimo;')
        self.assertEqual(voting.get_title(), (
            'Valstybės saugumo departamento įstatymo 10 straipsnio pakeitimo '
            'ĮSTATYMO PROJEKTAS (Nr. XIP-2992)'
        ))
        self.assertEqual(PersonVote.objects.filter(voting_id='-10765v').count(), 85)
