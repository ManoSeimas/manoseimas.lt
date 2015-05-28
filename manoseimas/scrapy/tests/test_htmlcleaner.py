import unittest

from manoseimas.scrapy import textutils


class HtmlCleanerTests(unittest.TestCase):
    def test_clean(self):
        result = textutils.clean_html(
            '<p class="MsoNormal" style="MARGIN: 0cm 0cm 0pt">'
            '<b style="mso-bidi-font-weight: normal">Gimimo vieta</b>'
            '</p>'
        )
        self.assertEqual(result, '<p><b>Gimimo vieta</b></p>')
