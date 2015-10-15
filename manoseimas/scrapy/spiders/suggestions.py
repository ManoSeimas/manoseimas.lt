# -*- coding: utf-8 -*-
import datetime
import logging
import re
import urllib
from collections import defaultdict

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

from manoseimas.scrapy.spiders import ManoSeimasSpider
from manoseimas.scrapy.items import Suggestion
from manoseimas.scrapy import pipelines


class SuggestionsSpider(ManoSeimasSpider):
    """Scrape suggestions from committee resolutions.

    Tip: if you think some data is discarded unnecessarily, run bin/scrapy
    with --loglevel=INFO
    """

    name = 'suggestions'
    allowed_domains = ['lrs.lt']

    # Query parameters:
    # - 'p_drus' (dokumento rūšis): document type
    # - 'p_kalb_id' (kalbos identifikatorius): language ID
    # - 'p_rus' (rušiavimas): sort order
    # - 'p_gal' (galutinis?): document status
    start_urls = [
        'http://www3.lrs.lt/pls/inter3/dokpaieska.rezult_l?' +
        urllib.urlencode({
            'p_drus': '290', # Rūšis: Pagrindinio komiteto išvada
            'p_nuo': '2012-11-16',
            'p_kalb_id': '1', # Kalba: Lietuvių
            'p_rus': '1', # Rūšiuoti rezultatus pagal: Registravimo datą
        }),
    ]

    rules = (
        # This handles pagination for us.
        Rule(SgmlLinkExtractor(allow=r'dokpaieska.rezult_l\?')),

        # This handles committee resolutions.
        Rule(SgmlLinkExtractor(allow=r'dokpaieska.showdoc_l\?p_id=-?\d+.*',
                               deny=r'p_daug=[1-9]'),
             'parse_document'),
    )

    pipelines = (
        pipelines.ManoSeimasModelPersistPipeline,
    )

    def parse_document(self, response):
        source_id = self._get_query_attr(response.url, 'p_id')
        tables = response.xpath("//div/table")
        empties = 0
        source_index = 0
        for table in tables:
            for item in self._parse_table(table, response.url):
                if not item['submitter']:
                    empties += 1
                    continue
                item['source_id'] = source_id
                item['source_index'] = source_index
                yield item
                source_index += 1
        if empties:
            # Examples of documents producing this warning:
            # - http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=487050&p_tr2=2
            #   (extra empty row between header and table data)
            # - http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=467948&p_tr2=2
            #   http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=444377&p_tr2=2
            #   http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=444379&p_tr2=2
            #   (this table was used to specify the suggestions of the
            #   committee itself, so there are no submitters, obviously)
            # - http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=467537&p_tr2=2
            #   (1st suggestion is unattributed)
            self.log("{n} empty rows discarded at {url}".format(n=empties, url=response.url),
                     level=logging.WARNING)

    def _parse_table(self, table, url):
        if not self._is_table_interesting(table, url):
            return
        last_item = None
        heuristic = 'left'
        if '491388' in url:
            # http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=491388&p_tr2=2
            heuristic = 'right'
        indexes = list(self._table_column_indexes(table, heuristic=heuristic))
        rows = self._process_rowspan_colspan(table.xpath('thead/tr|tr')[2:])
        for row in rows:
            for item in self._parse_row(row, indexes):
                if not item['submitter'] and not item['opinion']:
                    # sometimes there are blank rows
                    continue
                item['source_url'] = url
                if not item['submitter'] and last_item:
                    item['submitter'] = last_item['submitter']
                    item['date'] = last_item['date']
                    item['document'] = last_item['document']
                yield item
                last_item = item

    def _is_table_interesting(self, table, url):
        # We expect a table that has the following columns:
        #   [u'Eil. Nr.',
        #    u'Pasiūlymo teikėjas, data',
        #    u'Siūloma keisti',                     # colspan=3
        #    u'Pasiūlymo turinys',
        #    u'Komiteto nuomonė',
        #    u'Argumentai, pagrindžiantys nuomonę']
        # All of these except "Siūloma keisti" have a rowspan of 2.  The 2nd row
        # subdivides the "Siūloma keisti" column:
        #   [u'Str.', u'Str. d.', u'P.']
        columns = self._parse_table_columns(table)
        columns2 = self._parse_table_columns(table, 2)
        n = len(columns)
        m = len(columns2)
        if (n, m) == (6, 3):
            # I think false positives are unlikely, so I'm not checking actual column titles.
            return True
        # Here are some of the tables I've seen:
        # - [n=7] Eil. Nr. | Pasiūlymo teikėjas, data | Siūloma keisti | Pastabos | Pasiūlymo turinys | Komiteto nuomonė | Argumentai, pagrindžiantys nuomonę
        #   This is basically the right table, except it has one extra column in the middle.
        #   Example: http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=1076776&p_tr2=2
        # - [n=6,m=6] Eil. Nr. | Projekto Nr. | Teisės akto projekto pavadinimas | Teikia | Siūlo | Svarstymo mėnuo
        #   These are in section 6 or 7 (Komiteto sprendimas ir pasiūlymai) and don't interest us.
        # - [n=6,m=0] Eil. Nr. | Projekto Nr. | Teisės akto projekto pavadinimas | Teikia | Siūlo | Svarstymo mėnuo
        #   Same as above, but once the table had no heading and only one row of data.
        # - [n=5] Eil. Nr. | Projekto Nr. | Teisės akto projekto pavadinimas | Teikia | Siūlo
        #   These are in section 6 or 7 (Komiteto sprendimas ir pasiūlymai) and don't interest us.
        # - [n=4] Institucija | Turinys | Komiteto nuomonė | Argumentai, pagrindžiantys nuomonę
        #   These are in section 3 (Vyriausybės ar už pozicijos rengimą atsakingos institucijos parengta ar aprobuota pozicija)
        # - [n=3] Institucija | Turinys | Komiteto nuomonė
        #   These are in section 3 (Vyriausybės ar už pozicijos rengimą atsakingos institucijos parengta ar aprobuota pozicija)
        # - [n=2] Dėl (topic) | (paragraph of text)
        #   This is in section 8 (Komiteto sprendimas); it has no header row
        # - [n=1] (paragraph of text)
        #   Just a paragraph of text, somehow wrapped in a table without a border.
        # We might want to suppress the warning for known false positives.
        level = logging.INFO
        if n == 6 and m in (6, 0):
            level = logging.DEBUG
        elif n <= 2:
            level = logging.DEBUG
        if len(columns) != 6:
            self.log(u"Skipping table with wrong number of columns ({n}) at {url}:\n{columns}".format(
                n=n, url=url, columns=self._format_columns_for_log(columns)), level=level)
        else:
            self.log(u"Skipping table with wrong number of columns ({m}) in second row at {url}:\n{columns}".format(
                m=m, url=url, columns=self._format_columns_for_log(columns2)), level=level)
        return False

    @classmethod
    def _parse_table_columns(cls, table, row=1):
        return [
            cls._extract_text(col)
            for col in table.xpath("(thead/tr|tr)[%d]/td" % row)
        ]

    @classmethod
    def _table_column_bounds(cls, table, row=1):
        idx = 0
        for col in table.xpath("(thead/tr|tr)[%d]/td" % row):
            yield idx
            idx += cls._colspan(col)
        yield idx

    @classmethod
    def _table_column_indexes(cls, table, row=1, heuristic='middle'):
        bounds = list(cls._table_column_bounds(table, row=row))
        if heuristic == 'middle':
            return [(low + high) // 2 for (low, high) in zip(bounds, bounds[1:])]
        elif heuristic == 'right':
            return [(high - 1) for (low, high) in zip(bounds, bounds[1:])]
        else:
            return [low for (low, high) in zip(bounds, bounds[1:])]

    @staticmethod
    def _truncate(s, maxlen=50):
        if len(s) > maxlen:
            return s[:maxlen - 3] + '...'
        else:
            return s

    @classmethod
    def _format_columns_for_log(cls, columns):
        return u' | '.join(map(cls._truncate, columns))

    @staticmethod
    def _colspan(td):
        return int((td.xpath('@colspan').extract() or ['1'])[0])

    @staticmethod
    def _rowspan(td):
        return int((td.xpath('@rowspan').extract() or ['1'])[0])

    @classmethod
    def _process_rowspan_colspan(cls, rows):
        pending = defaultdict(list)
        for row in rows:
            output = []
            for td in row.xpath('td'):
                while pending[len(output)]:
                    output.append(pending[len(output)].pop())
                colspan = cls._colspan(td)
                rowspan = cls._rowspan(td)
                for n in range(colspan):
                    pending[len(output)] += [td] * (rowspan - 1)
                    output.append(td)
            while pending[len(output)]:
                output.append(pending[len(output)].pop())
            yield output

    @classmethod
    def _parse_row(cls, row, column_indexes):
        # Columns:
        # 0. Eil. Nr.
        # 1. Pasiūlymo teikėjas, data
        # 2. Siūloma keisti: Str., Str.d., P.
        # 3. Pasiūlymo turinys
        # 4. Komiteto nuomonė
        # 5. Argumentai, pagrindžiantys nuomonę
        submitter_and_date = cls._extract_text(row[column_indexes[1]])
        opinion = cls._extract_text(row[column_indexes[4]])
        yield Suggestion(
            opinion=cls._clean_opinion(opinion),
            **cls._parse_submitter(submitter_and_date)
        )

    @classmethod
    def _parse_submitter(cls, submitter_and_date):
        # Expect one of:
        # - ""
        # - "Submitter YYYY-MM-DD"
        # - "Submitter, YYYY-MM-DD"
        # - "Submitter (YYYY-DD-MM)"
        # - "Submitter ( YYYY-DD-MM )"
        # - "Submitter ( YYYY- DD-MM)"
        # - "Submitter (YYYY-MM-DD, raštas Nr. g-YYYY-NNNN)"
        # - "Submitter (YYYY-MM-DD, nutarimas Nr. NNN)"
        # - "Submitter YYYY-MM-DD Nr. 1.NN-NN"
        # - "Submitter, YYYY-MM-DD Nr. g-YYYY-NNNN"
        # - "Submitter, YYYY-MM-DD Nr. g-YYYY-NNNN"
        # - "Submitter, YYYY-MM-DD d. Nutarimas Nr. NNN"
        # - "Submitter, YYYY MM DD Nutarimas Nr. NNN"
        # - "Submitter, YYYYMMDD (Nr.NNN)"
        # - "Submitter, YYYY-" (!)
        # - "Submitter, YYYY-MM" (!)
        # - "Submitter, YYYY-MM-" (!)
        # - "SubmitterYYYY-MM-DD" (!)
        # - "Submitter YYYY-MM-DD nutarimas Nr. NNN"
        # - "Submitter YYYY m. liepos NN d. išvada Nr. NNN"
        # - "Submitter (YYYY m. rugpjūčio 19 d. nutarimas Nr. NNN)"
        # - "Submitter (YYYYm. rugpjūčio 19 d. nutarimas Nr. NNN)"
        # - "Submitter (YYYY-MM-DD raštas Nr. NS-NNNN) (išrašas)"
        # - "Submitter YYYY-MM-DD Nr. XIIP-NNNN(N)"
        # BTW submitter might be hyphenated, for extra fun, e.g.
        # - "Seimo kanceliarijos Teisės departamentas"
        # - "Seimo kanceliari-jos Teisės departa-mentas"
        # and there are other fun possibilities, like
        # - "Anoniminis"
        # - "Asociacija ,,Infobalt“"
        # - "Asociacija „Infobalt“"
        # - "Asociacija „INFOBALT“"
        # - "ETD prie TM"
        # - "Europos teisės departamentas"
        # - "Europos teisės Departamentas"
        # - "Europos Teisės departamentas prie TM"
        # - "Europos Teisės departamentas prie Teisingumo ministerijos"
        # - "Europos teisės departamentas prie Lietuvos Respublikos teisingumo ministerijos"
        # - "TD"
        # - "(TD)"
        # - "Teisės departamentas"
        # - "Teisės departamen-tas prie Lietuvos Respublikos teisingumo ministerijos"
        # And combined goodness:
        # - "Jurbarko rajono verslininkų organizacija, NNNN-NN-NN Kartu pridėtas NNNN-NN-NN raštas"
        # - "Jurbarko rajono verslininkų organizacija, NNNN-NN-NN Kartu pridėtas ir NNNN-NN-NN raštas."
        # - "Huntingtono ligos asociacija, Lietuvos išsėtinės sklerozės sąjunga, Lietuvos asociacija „Gyvastis“, Lietuvos sergančiųjų genetinėmis nervų-raumenų ligomis asociacija „Sraunus\", Lietuvos vaikų vėžio asociacija „Paguoda“, Onkohematologinių ligonių bendrija „Kraujas\", NNNN-NN-NN"
        # - "Lietuvos Pediatrų draugijos pirmininkas prof. A. Valiulis, Lietuvos vaikų nefrologų draugijos pirmininkė prof. A. Jankauskienė, Lietuvos vaikų gastroenterologų ir mitybos draugijos pirmininkas doc. V. Urbonas, Lietuvos vaikų hematologų draugijos pirmininkė dr. S. Trakymienė, Lietuvos vaikų kardiologų draugijos pirmininkė doc. O. Kinčinienė, Vilniaus krašto pediatrų draugijos pirmininkė doc. R. Vankevičienė, NNNN-NN-NN"
        # - "Lietuvos Respub-likos specialiųjų tyrimų tarnyba, NNNN-NN-NN antikorup-cinio vertinimo išvada, Nr. N-NN-NNN"
        # - "LR Seimo Sveikatos reikalų komiteto neetatinė ekspertė Mykolo Romerio universiteto Politikos mokslų instituto profesorė dr. Danguolė Jankauskienė, NNNN-NN-NN"
        # - "Seimo nariai L. Dmitrijeva V.V. Margevičienė R. Tamašiūnienė J. Vaickienė V. Filipovičienė G. Purvaneckienė J. Varkala R. Baškienė M.A. Pavilionienė A. Matulas NNNN-NN-NN"
        # - "VšĮ „Psichikos sveikatos perspektyvos“, NNNN.NN.NN VšĮ Žmogaus teisių stebėjimo institutas, NNNN.NN.NN Asociacija „Lietuvos neįgaliųjų forumas“, NNNN.NN.NN VšĮ „Paramos vaikams centras“, NNNN.NN.NN Asociacija „Nacionalinis aktyvių mamų sambūris“, NNNN.NN.NN Žiburio fondas, NNNN.NN.NN LPF SOS vaikų kaimų Lietuvoje draugija, NNNN.NN.NN VšĮ Šeimos santykių institutas, NNNN.NN.NN Visuomeninė organizacija „Gelbėkit vaikus“, NNNN.NN.NN"
        # - "Teikia: Seimo nariai: Dainius Budrys, Vaidotas Bacevičius, Vytautas Gapšys, Juozas Olekas, Julius Sabatauskas, Erikas Tamašauskas."
        parts = re.split(r'(\d\d\d\d ?-? ?[01]? ?\d ?-? ?[0-3] ?\d)\b', submitter_and_date, maxsplit=1)
        submitter = parts[0]
        date = parts[1] if len(parts) > 1 else ''
        document = parts[2] if len(parts) > 2 else ''
        return dict(
            submitter=cls._clean_submitter(submitter),
            date=cls._clean_date(date),
            document=cls._clean_document(document),
        )

    @staticmethod
    def _clean_submitter(submitter):
        submitter = re.sub(r'\(gauta *$', '', submitter)
        submitter = submitter.rstrip('(, ')
        submitter = submitter.replace(',,', u'„')
        submitter = re.sub(ur'- ?(?!urbanist|visuotin)([a-ząčęėįšųūž])', r'\1', submitter)
        submitter = re.sub(ur'(\.)([A-ZĄČĘĖĮŠŲŪŽ])', r'\1 \2', submitter)
        submitter = submitter.replace('departamenras', 'departamentas')
        submitter = submitter.replace('departamentamentas', 'departamentas')
        submitter = submitter.replace(u'RespublikosPrezidentės', u'Respublikos Prezidentės')
        submitter = submitter.replace(u'Teisėsdepartamentas', u'Teisės departamentas')
        submitter = submitter.replace(u'Žaliais taškas', u'Žaliasis taškas')
        submitter = submitter.replace(u'LAMPETRA', u'Lampetra')
        submitter = submitter.replace(u'AB LESTO', u'AB „Lesto“')
        submitter = submitter.replace(u'AB Lietuvos dujos“', u'AB „Lietuvos dujos“')
        submitter = submitter.replace(u'AB Litgrid', u'AB „Litgrid“')
        submitter = submitter.replace(u'AB LOTOS Geonafta įmonių grupė', u'AB „LOTOS Geonafta įmonių grupė“')
        submitter = submitter.replace(u'įmonių grupė“ UAB', u'įmonių grupė“, UAB')
        return submitter

    @staticmethod
    def _clean_date(date):
        date = date.replace(' ', '')
        m = re.match(r'(\d\d\d\d)-?(\d?\d)-?(\d\d)', date)
        if m:
            try:
                date = str(datetime.date(*map(int, m.groups())))
            except ValueError:
                # TODO: log
                return ''
        return date

    @staticmethod
    def _clean_document(document):
        # "YYYY-MM-DD d. nr. 123"
        document = re.sub('^ *d[.]', '', document)
        # leading punctuation and spaces
        document = re.sub('^[- ;,)]+', '', document)
        # trailing spaces
        document = re.sub(' +$', '', document)
        # YYYY-MM-DD (Nr. NNN)
        document = re.sub('^[(](.*)[)]$', r'\1', document)
        # (YYYY-MM-DD Nr.NNN), but leave YYYY-MM-DD Nr. XIIP-NNN(N) alone
        document = re.sub('^([^()]*(?:[(][^)]*[)][^()]*)*)[)]*$', r'\1', document)
        # leading and trailing spaces inside the ( )
        return document.strip()

    @staticmethod
    def _clean_opinion(opinion):
        # Examples:
        # - ""
        # - "Pritarta"
        # - "Pritarti"
        # - "Pritarti."
        # - "29. Pritarti"
        # - "Pritari" [sic]
        # - "Atsižvelgti"
        # - "Nepritarti"
        # - "Nepritarti."
        # - "Ne-pritarti"
        # - "Nepri tarti"
        # - "Nepri-tarti"
        # - "Pritarti iš dalies"
        # - "Iš dalies pritarti"
        # - "Nesvarstyti"
        # - "Nesvarstyta"
        # - "Spręsti pagrindiniame komitete"
        # - "Siūlyti spręsti pagrindiniame komitete"
        # - "Siūlyti svarstyti pagrindi- niam komitetui"
        # - "Siūlyti svarstyti pagrindi-niam komitetui"
        # - "Apsispręsti pagrindiniame komitete"
        # - "Apsispręsti pagrindiniamekomitete"
        # - "Pritarti Pritarti"
        # - "Pritarti (už-N; prieš-N; susilaikė-N)"
        # - "Nepritarti (bendru sutarimu – už)"
        # - "Pritarti. Siūlomos pataisos neprieštarauja Lietuvos Respublikos įsipareigojimams tinkamai tvarkyti atliekas."
        # - "Atsižvelgti (gauta Vyriausybės nuomonė 2015-02-04)"
        # - "Atsižvelgti. Pritarti"
        # - "Iš esmės pritarti"
        # - "Iš esmės pritarti pataisymui"
        # - "Iš esmės pritarti Pritarti"
        # - "Pritarti dėl asmens informavimo"
        # - "Pritarti Pritarti Pritarti Pritarti Pritarti Pritarti Pritarti Pritarti Pritarti Pritarti Pritarti Pritarti Pritarti Pritarti iš dalies Nepritarti Atsižvelgti Pritarti"
        # - "Pritarti Pritarti Pritarti iš dalies Pritarti Pritarti. Atsižvelgti Atsižvelgti pagr. Komitetui, tačiau nestabdyti projekto XIIP- 2328 svarstymo ir priėmimo proceso Seime"
        # - "2014-03-18 d. Seimo plenarinio posėdžio metu nebuvo pritarta pasiūlymui prašyti Vyriausybės išvadų dėl įstatymo projekto XIIP-1539"
        # - "Su nuomone susipažinta"
        # - "Žr. TTK 2014 04 16 išvadą"
        # - ". Pritarti Pritarti iš dalies Pritarti"
        # - "Pritarti \\ Pritarti"
        # - "???"
        # - "`"
        return opinion.rstrip('.')

    @classmethod
    def _extract_text(cls, element):
        return cls._normalize_whitespace(
            ' '.join(element.xpath('.//text()').extract()))

    @staticmethod
    def _normalize_whitespace(s):
        return ' '.join(s.split())
