# -*- coding: utf-8 -*-
import scrapy

from manoseimas.scrapy import pipelines
from manoseimas.scrapy.items import LobbyistDeclaration
from manoseimas.scrapy.helpers.msword import doc2xml
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.spiders import ManoSeimasSpider


class LobbyistDeclarationsSpider(ManoSeimasSpider):
    name = 'lobbyist_declarations'
    allowed_domains = ['www.vtek.lt', 'old.vtek.lt']
    start_urls = [
        'http://www.vtek.lt/index.php/deklaravimas',
    ]
    pipelines = (
        pipelines.ManoSeimasModelPersistPipeline,
    )

    def parse(self, response):
        links = response.xpath(u"//h2[contains(., 'Lobistų deklaracijos')]/../following-sibling::div[@class='list_content']//a")
        if not links:
            self.error(response, "Lobbyist declarations not found")
            return
        for link in links:
            year = link.xpath('text()').extract()[0]
            url = link.xpath('@href').extract()[0]
            request = scrapy.Request(url, self.parse_declaration_doc)
            request.meta['year'] = year
            yield request

    def parse_declaration_doc(self, response):
        docbook_xml = doc2xml(response.body)
        fake_response = response.replace(body=docbook_xml)
        return self.parse_declaration_xml(fake_response)

    def parse_declaration_xml(self, response):
        columns = response.xpath('//row[1]/entry/text()').extract()
        # Expected:
        #  - 'Eilės\nNr.'
        #  - 'Lobisto vardas, pavardė ar pavadinimas'
        #  - 'Teisės akto ar teisės akto projekto, dėl kurio vykdyta lobistinė veikla, pavadinimas'
        #  - 'Pastabos'
        if len(columns) != 4:
            self.error(response, "Lobbyist declaration has unexpected number of columns ({})".format(len(columns)))
            return
        rows = response.xpath('//row')[1:]
        for row in rows:
            yield self._parse_lobbyist(response, row)

    def _parse_lobbyist(self, response, row):
        nr, name, law_projects, comments = row.xpath('entry')
        declaration = Loader(self, response, LobbyistDeclaration(), row,
                             required=('name', ))
        declaration.add_value('source_url', response.url)
        declaration.add_value(None, self._parse_number(nr))
        declaration.add_value(None, self._parse_name(name))
        declaration.add_value(None, self._parse_comments(comments))
        return declaration.load_item()

    def _parse_number(self, entry):
        # Example inputs:
        #  - <entry>1.</entry>
        return {}  # we're not interested

    def _parse_name(self, entry):
        # Example inputs:
        # - <entry>ROMAS STUMBRYS</entry>
        # - <entry>BRONIUS ANTANAS RASIMAS</entry>
        # - <entry>UAB "ERNST &amp; YOUNG BALTIC"</entry>
        # - <entry>UAB “GLAXOSMITHKLINE LIETUVA”</entry>
        # - <entry>UAB „VENTO NUOVO“</entry>
        # - <entry>ADVOKATŲ PROFESINĖ BENDRIJA "BALTIC LEGAL SOLUTIONS LIETUVA”</entry>
        # - <entry>VŠĮ "MOKESČIŲ IR VERSLO PROCESŲ ADMINISTRAVIMO CENTRAS"</entry>
        return {'name': entry.xpath('text()').extract()}

    def _parse_comments(self, entry):
        # Example inputs:
        # - <entry></entry>
        # - <entry>Lobistinės veiklos nevykdė</entry>
        return {'comments': entry.xpath('text()').extract()}
