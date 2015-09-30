# -*- coding: utf-8 -*-
import datetime

from scrapy import log

from manoseimas.scrapy import pipelines
from manoseimas.scrapy.items import Lobbyist
from manoseimas.scrapy.loaders import Loader
from manoseimas.scrapy.spiders import ManoSeimasSpider


DATE_REGEXP = r'\b\d{4}[-. ]\d{2}[-. ]\d{2}\b'


class LobbyistsSpider(ManoSeimasSpider):
    name = 'lobbyists'
    allowed_domains = ['www.vtek.lt']
    start_urls = [
        'http://www.vtek.lt/index.php/deklaravimas',
    ]
    pipelines = (
        pipelines.ManoSeimasModelPersistPipeline,
    )

    def parse(self, response):
        tables = response.xpath("//h2[contains(., 'Registruoti lobistai')]/../..//table")
        if not tables:
            self.error(response, "Lobbyist table not found")
            return
        if len(tables) > 1:
            self.log("More than one possible lobbyist table found, {}".format(response.url),
                     level=log.WARNING)
        table = tables[0]
        columns = table.xpath('.//tr[1]/td/text()').extract()
        # Expected: [
        #   u'Eil. Nr.',
        #   u'Lobisto vardas, pavardė ar pavadinimas',
        #   u'Įmonės registro kodas',
        #   u'Įrašymo į lobistų sąrašą data ir sprendimo Nr.',
        # ]
        if len(columns) != 4:
            self.error(response, "Lobbyist table has unexpected number of columns ({})".format(len(columns)))
            return
        for n, row in enumerate(table.css('tr')):
            if n == 0:
                # skip headers
                continue
            yield self._parse_lobbyist(response, row)

    def _parse_lobbyist(self, response, row):
        nr, name, company_code, inclusion = row.css('td')
        lobbyist = Loader(self, response, Lobbyist(), row,
                          required=('name', 'date_of_inclusion', 'decision'))
        lobbyist.add_value('source_url', response.url)
        lobbyist.add_value('raw_data', row.extract())
        lobbyist.add_value(None, self._parse_number(nr))
        lobbyist.add_value(None, self._parse_name(name))
        lobbyist.add_value(None, self._parse_company_code(company_code))
        lobbyist.add_value(None, self._parse_inclusion(inclusion))
        return lobbyist.load_item()

    def _parse_number(self, td):
        # Example inputs:
        #  - <td>1.</td>
        #  - <td>35</td>
        return {}  # we're not interested

    def _parse_name(self, td):
        # Example inputs:
        #  - <td>BRONIUS ANTANAS RASIMAS</td>
        #  - <td><p><a href="...">UAB "FOO &amp; BAR"</a></p><p>Gintautas Bartkus, Jonas Platelis</p></td>
        #  - <td><a href="http://www.juris.lt/">UAB "VOX JURIS"</a><br />2015-04-15 sprendimu Nr. KS-31 (L) lobistinė veikla nutraukta.</td>
        #  - <td><a href="http://www.lamco.lt/">MYKOLAS JUOZAPAVIČIUS</a></td>
        #  - <td>NINA BARBORA EVANS 2012 02 21 sprendimu Nr. KS-16 (L) sustabdyta lobistinė veikla iki prašymo atnaujinti.</td>
        #  - <td>MINDAUGAS VOLDEMARAS<br /> 2015 03 04 sprendimu Nr. KS-20 (L) sustabdyta lobistinė veikla iki prašymo atnaujinti.</td>
        #  - <td><p>VŠĮ "MOKESČIŲ IR VERSLO PROCESŲ ADMINISTRAVIMO CENTRAS"</p><p>Sandra Šarkauskaitė</p></td>
        name = map(self.maybe_titlecase, td.xpath('text() | a/text()').re(r'^(.*?)(?:\s*%s sprendimu.*)?$' % DATE_REGEXP))
        company_name = td.xpath('p[1]/text() | p[1]/a/text()').extract()
        url = td.xpath('a/@href | p[1]/a/@href').extract()
        representatives = td.xpath('p[2]/text()').extract()
        status = td.xpath('text() | a/text()').re(r'\b(%s sprendimu.*)$' % DATE_REGEXP)
        return dict(name=name + company_name, url=url, representatives=representatives, status=status)

    @staticmethod
    def maybe_titlecase(s):
        if '"' in s or u'“' in s:
            # name of a company
            return s
        else:
            # name of a person
            return s.title()

    @staticmethod
    def parse_date(s):
        return datetime.date(*map(int, s.replace(' ', '-').replace('.', '-').split('-')))

    def _parse_company_code(self, td):
        # Example inputs:
        #  - <td>&nbsp;</td>
        #  - <td>303063215</td>
        return dict(company_code=td.xpath('text()').extract())

    def _parse_inclusion(self, td):
        # Example inputs:
        #  - <td>2015 05 20 Nr. KS-36 (L)</td>
        #  - <td>2012 10 02 Nr. KS - 108 (L)</td>
        #  - <td>2012 04 17 Nr. KS -22 (L)</td>
        #  - <td style="text-align: center;">2011 12 06 Nr. KS - 75 (L)</td>
        #  - <td>2002 10 04 Nr. 23 (L)</td>
        date = map(self.parse_date, td.xpath('text()').re(r'^(%s)' % DATE_REGEXP))
        decision = td.xpath('text()').re(r'^(?:%s)?(.*)$' % DATE_REGEXP)
        return dict(date_of_inclusion=date, decision=decision)
