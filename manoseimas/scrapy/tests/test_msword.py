import unittest

from manoseimas.scrapy.tests.utils import fixture
from manoseimas.scrapy.helpers.msword import doc2xml


class TestWordConversion(unittest.TestCase):

    def test_doc2xml(self):
        xml = doc2xml(fixture('lobist_veiklos_atatskaita_2012.doc'))
        expected = fixture('lobist_veiklos_atatskaita_2012.doc.xml')
        self.assertEqual(xml, expected)
