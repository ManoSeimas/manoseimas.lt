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
from manoseimas.scrapy.helpers.dates import date_re, month_names_map
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
                    item['raw'] = last_item['raw']
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
        # Sometimes dates have some extra spaces in them for fun!
        # - "Lietuvos miško savininkų asociacija 201 3 -0 5 - 28 Nr. 41 G-2013-6553"
        # - "Lietuvos Respublikos teisingumo ministerija,2 013-11-12"
        # - "Seimo kanceliarijos Teisės departamentas, 201 5 -02-05"
        # - "Seimo kanceliarijos Teisės departamentas, 201 5 -0 4 - 17"
        # - "Seimo kanceliarijos Teisės departamentas, 201 5 -0 4 -20"
        raw = submitter_and_date
        short_date_re = re.compile(r'(\d\d\d\d ?-? ?[01]? ?\d ?-? ?[0-3] ?\d)\b')
        if not short_date_re.search(submitter_and_date):
            submitter_and_date = re.sub(r'(\d) (\d)', r'\1\2', submitter_and_date)
            submitter_and_date = cls._normalize_dates(submitter_and_date)
        parts = short_date_re.split(submitter_and_date, maxsplit=1)
        if len(parts) == 1:
            parts = re.split(r'()(\bG-20\d\d-\d+.*|\b[IVXL]+P-\d+.*)', submitter_and_date, maxsplit=1)
        submitter = parts[0]
        date = parts[1] if len(parts) > 1 else ''
        document = parts[2] if len(parts) > 2 else ''
        return dict(
            raw=raw,
            submitter=cls._clean_submitter(submitter),
            date=cls._clean_date(date),
            document=cls._clean_document(document),
        )

    @staticmethod
    def _clean_submitter(submitter):
        submitter = re.sub(r'\(sudaryta [^)]*\)?', '', submitter)
        submitter = re.sub(ur'([ \d])išvada.*$', r'\1', submitter)
        submitter = re.sub(r'\((?:pateikiama )?sutrumpintai\)', '', submitter)
        submitter = re.sub(ur'\s+dėl įstatymo projekto [^,]*', '', submitter)
        submitter = re.sub(ur', \d\d\d\d Nr. [^,]*', '', submitter)
        submitter = re.sub(r' *\d\d\d\d(-\d\d)?-? *$', '', submitter)
        submitter = re.sub(r'20\d\d?(-\d\d?)?(-\d\d?)?v?$', '', submitter)
        submitter = re.sub(r'\(gauta *[^)]*[)]?$', '', submitter)
        submitter = submitter.rstrip('(,; ')
        submitter = submitter.replace(',,', ur'„')
        submitter = re.sub(ur'- ?(?!urbanist|visuotin)([a-ząčęėįšųūž])', r'\1', submitter)
        submitter = re.sub(ur'(\.)([A-ZĄČĘĖĮŠŲŪŽ])', r'\1 \2', submitter)
        submitter = re.sub(ur'(?<!\bkt)(?<![A-ZĄČĘĖĮŠŲŪŽ])\.$', r'', submitter)
        submitter = re.sub(ur'(komitetas)(?! prie).+$', r'\1', submitter)
        submitter = re.sub(ur', \w+ \d+-\d+, LT-\d+ Vilnius', '', submitter, flags=re.UNICODE)
        submitter = re.sub(ur', tel\. [-\d]+', '', submitter)
        submitter = re.sub(ur',? el\. paštu \S+\@\S+\.\S+', '', submitter)
        submitter = re.sub(ur' +\d+\.\d+\.\d+\.\d+', '', submitter)
        names = [
            u'Adolf(as|o)',
            u'Agn(ė|ės)?'
            u'Aleksand(as|o)',
            u'Alg(is|io)',
            u'Antan(as|o)',
            u'Anatolij(us|jaus)',
            u'Albin(as|o)',
            u'Algimant(as|o)',
            u'Algird(as|o)',
            u'Andr(ius|iaus)',
            u'Arimant(as|o)',
            u'Artūr(as|o)',
            u'Arvyd(as|o)',
            u'Aurelij(a|os)',
            u'Audron(ė|ės)',
            u'Birut(ė|ės)',
            u'Bron(ius|iaus)',
            u'Česlov(as|o)',
            u'Dain(ius|iaus)',
            u'Daiv(a|os)',
            u'Dali(a|os)',
            u'Danguol(ė|ės)',
            u'Danguolė(s)',
            u'Dar(ius|iaus)',
            u'Deivid(as|o)',
            u'Dom(as|o)',
            u'Edvard(as|o)',
            u'Eduard(as|o)',
            u'Eligij(us|aus)',
            u'Erik(as|o)',
            u'Evald(as|o)',
            u'Eugenij(us|aus)',
            u'Giedr(ius|iaus)',
            u'Gintar(as|o)',
            u'Gintar(ė|ės)',
            u'Gy(tis|čio)',
            u'Igori(s|o)',
            u'Jaroslav(o)',
            u'Jon(as|o)',
            u'Jolit(a|os)',
            u'Juoz(as|o)',
            u'Jul(ius|iaus)',
            u'Jurg(is|io)',
            u'Jur(as|o)',
            u'Gedimin(as|o)',
            u'Giedr(ė|ės)',
            u'Gintaut(as|o)',
            u'Henrik(as|o)',
            u'Irm(a|os)',
            u'Kondrot(as|o)',
        ]
        # Split reason:
        #     /python2.7/sre_compile.py
        #     AssertionError: "sorry, but this version only supports 100 named groups"
        submitter = re.sub(u'|'.join(names), lambda m: m.group(0)[0] + '.', submitter)
        names = [
            u'Laim(a|os)',
            u'Laris(a|os)',
            u'Laur(a|os)',
            u'Lin(as|o)',
            u'Liucij(us|aus)',
            u'Leonard(|o)',
            u'Loret(a|os)',
            u'ij(a|os)',
            u'Martyn(a|os)',
            u'Mečislov(as|o)',
            u'Migl(ė|ės)',
            u'Mild(a|os)',
            u'Mindaug(as|o)',
            u'Nomed(a|os)',
            u'Kazimier(as|o)',
            u'Kaz(ys|io)',
            u'Kęstut(is|čio)',
            u'Kęst(as|o)',
            u'Nagl(is|io)',
            u'On(a|os)',
            u'Paul(ius|iaus)',
            u'Petr(as|o)',
            u'Povil(as|o)',
            u'Raimund(as|o)',
            u'Ramut(ė|ės)',
            u'Ras(a|os)',
            u'Remigij(us|aus)',
            u'Rimant(ė|ės)',
            u'Rimant(as|o)',
            u'Rim(a|os)',
            u'Rit(a|os)',
            u'Robert(as|o)',
            u'Roland(as|o)',
            u'Rok(as|o)',
            u'Saul(ius|iaus)',
            u'Sergej(|aus)',
            u'Stas(ys|io)',
            u'Vald(as|o)',
            u'Vaidot(as|o)',
            u'Valentin(as|o)',
            u'Valerij(us|aus)',
            u'Vand(a|os)',
            u'Vidmant(as|o)',
            u'Viktor(as|o)',
            u'Vilij(a|os)',
            u'Virginij(us|aus)',
            u'Vitalij(a|os)',
            u'Vitalij(us|aus)',
            u'Vinc(ė|ės)',
            u'Vit(as|o)',
            u'Vytaut(as|o)',
            u'Zit(a|os)',
        ]
        submitter = re.sub(u'|'.join(names), lambda m: m.group(0)[0] + '.', submitter)
        replacements = {
            u'departamenras': 'departamentas',
            u'departamentamentas': 'departamentas',
            u'departamantas': 'departamentas',
            u'departamntas': 'departamentas',
            u'departmentas': 'departamentas',
            u'departamentasprie': u'departamentas prie',
            u'departame ntas': 'departamentas',
            u'departametas': u'departamentas',
            u'RespublikosPrezidentės': u'Respublikos Prezidentės',
            u'Teisėsdepartamentas': u'Teisės departamentas',
            u'Teisės departamentas (TD)': u'Teisės departamentas',
            u'Teisės departamento (TD)': u'Teisės departamentas',
            u'Žaliais taškas': u'Žaliasis taškas',
            u'LAMPETRA': u'Lampetra',
            u'INFOBALT': u'Infobalt',
            u'AB LESTO': u'AB „Lesto“',
            u'AB Lietuvos dujos“': u'AB „Lietuvos dujos“',
            u'AB Litgrid': u'AB „Litgrid“',
            u'AB LOTOS Geonafta įmonių grupė': u'AB „LOTOS Geonafta įmonių grupė“',
            u'įmonių grupė“ UAB': u'įmonių grupė“, UAB',
            u'„Investors‘ Forum,“': u'„Investuotojų forumas“',
            u'Asociacija Lietuvos antstolių rūmai': u'Asociacija „Lietuvos antstolių rūmai“',
            u'Audito Komitet': u'Audito komitet',
            u"Darbų saugos specialistų darbdavių asociacija": u"Darbo saugos specialistų darbdavių asociacija",
            u'Legalaus Verslo aljansas': u'Legalaus verslo aljansas',
            u'Aukčiausiasis': u'Aukščiausiasis',
            u'Aukščiausiais Teismas': u'Aukščiausiasis Teismas',
            u'Aukščiausias Teismas': u'Aukščiausiasis Teismas',
            u'Aukščiausiasis teismas': u'Aukščiausiasis Teismas',
            u'Lietuvos Advokatūra': u'Lietuvos advokatūra',
            u' Apeliacinis Teismas': u' apeliacinis teismas',
            u' Apeliacinis teismas': u' apeliacinis teismas',
            u'Europos Teisės': u'Europos teisės',
            u'pramoninkų': u'pramonininkų',
            u'tarnyb a': u'tarnyba',
            u'tarnyba tarnyba': u'tarnyba',
            u'tarnyba (toliau– STT)': u'tarnyba',
            u'Seimo Biudžeto': u'Seimo biudžeto',
            u'Respublikos Finansų': u'Respublikos finansų',
            u'Respublikos Generalinė': u'Respublikos generalinė',
            u'Respublikos Specialiųjų': u'Respublikos specialiųjų',
            u'Respublikos Teisingumo': u'Respublikos teisingumo',
            u'Respublikos Transporto': u'Respublikos transporto',
            u'Respublikos Trišalė': u'Respublikos trišalė',
            u'Respublikos Ūkio': u'Respublikos ūkio',
            u'Respublikos Vaiko': u'Respublikos vaiko',
            u'Respublikos Valst': u'Respublikos valst',
            u'Respublikos Vyr': u'Respublikos vyr',
            u'Lietuvos respublikos': u'Lietuvos Respublikos',
            u'Lietuvos Savivaldybių': u'Lietuvos savivaldybių',
            u'LIETUVOS KARJERŲ ASOCIACIJA': u'Lietuvos karjerų asociacija',
            u'miškų savininkų asociacija': u'miško savininkų asociacija',
            u'asociacija LINAVA': u'asociacija „Linava“',
            u'asociacija „LINAVA“': u'asociacija „Linava“',
            u'vežėjų asociacija „Linava“': u'vežėjų automobiliais asociacija „Linava“',
            u"Lietuvos nealkoholinių gėrimų gamintojų ir importuotojų asociacija":
                u"Lietuvos nealkoholinių gėrimų gamintojų bei importuotojų asociacija",
            u'Konfederacija': u'konfederacija',
            u'vaiko teisių apsaugos kontrolės': u'vaiko teisių apsaugos kontrolieriaus',
            u'Vilnaius': u'Vilniaus',
            u' Universitetas': u' universitetas',
            u'VšĮ': u'VŠĮ',
            u'ministreijos': 'ministerijos',
            u'LR Seimo': u'Seimo',
            u'LRS Seimo': u'Seimo',
            u'LRS kanceliarijos': u'Seimo kanceliarijos',
            u'Seimo Kanceliarijos': u'Seimo kanceliarijos',
            u'Lietuvos Respublikos Seimo kanceliarijos': u'Seimo kanceliarijos',
            u'Seimo kanceliarijos teisės departamentas': u'Seimo kanceliarijos Teisės departamentas',
            u'Teisingum 0': u'Teisingumo',
            u'kanceliarij os': u'kanceliarijos',
            u'kancelarijos': u'kanceliarijos',
            u'Seimo Teisės departamentas': u'Seimo kanceliarijos Teisės departamentas',
            u'LRS Teisės departamentas': u'Seimo kanceliarijos Teisės departamentas',
            u'Teisės Departamentas': u'Teisės departamentas',
            u'prie LR': u'prie Lietuvos Respublikos',
            u'prie SM': u'prie Susisiekimo ministerijos',
            u'prie Lietuvos Respublikos vidaus reikalų ministerijos': u'prie Vidaus reikalų ministerijos',
            u'nusikaltimų tyrimų tarnyba': u'nusikaltimų tyrimo tarnyba',
            u'm. savivaldybė': u'miesto savivaldybė',
            u'Valstybės vaiko teisių ir įvaikinimo tarnyba': u'Valstybės vaiko teisių apsaugos ir įvaikinimo tarnyba',
            u'prie socialinės apsaugos ir darbo ministerijos': u'prie Socialinės apsaugos ir darbo ministerijos',
            u'Valstybinės teismo medicinos tarnyba': u'Valstybinė teismo medicinos tarnyba',
            u'Taryba': u'taryba',
            u'Lietuvos Vyriausiasis': u'Lietuvos vyriausiasis',
            u'Nacionalin ė': u'Nacionalinė',
            u'draudik ų': u'draudikų',
            u'profesinės sąjunga': u'profesinė sąjunga',
            u'Lietuvos nacionalinė sveikatos tarybos': u'Lietuvos nacionalinės sveikatos tarybos',
            u'LIETUVOS GEOGRAFŲ DRAUGIJA': u'Lietuvos geografų draugija',
            u'Lietuvos Nepriklausomybės Akt': u'Lietuvos nepriklausomybės akt',
        }
        for a, b in sorted(replacements.items()):
            submitter = submitter.replace(a, b)
        submitter = re.sub(ur'(departamento|departamentas)(,? [Pp]rie .*)?$', 'departamentas', submitter)
        submitter = re.sub(ur' \(JTVPK\)$', '', submitter)
        submitter = re.sub(ur'(„[\w\d ]+)$', ur'\1“', submitter, flags=re.UNICODE)
        submitter = re.sub(ur'^LR ', u'Lietuvos Respublikos ', submitter)
        submitter = re.sub(ur'^(?:LR|Lietuvos Respublikos) (.* ministerija)$', lambda m: m.group(1).capitalize(), submitter)
        submitter = re.sub(ur'prie (?:LR|Lietuvos Respublikos) (.* ministerijos)$', lambda m: u'prie ' + m.group(1).capitalize(), submitter)
        submitter = {
            u'(TD)': u'Seimo kanceliarijos Teisės departamentas',
            u'TD': u'Seimo kanceliarijos Teisės departamentas',
            u'Teisės departamentas': u'Seimo kanceliarijos Teisės departamentas',
            u'Informacinės visuomenės plėtros komitetas': u'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos',
            u'IVPK': u'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos',
            u'JTVPK': u'Jungtinių Tautų vyriausiojo pabėgėlių komisaro regioninis Šiaurės Europos biuras',
            u'LAEI': u'Lietuvos agrarinės ekonomikos institutas',
            u'LAWG': u'Local American Working Group (LAWG)',
            u'MARIJAMPOLĖS REGIONO PLĖTROS TARYBA': u'Marijampolės regiono plėtros taryba',
            u'ŽŪM': u'Žemės ūkio ministerija',
            u'Aukščiausiasis Teismas': u'Lietuvos Aukščiausiasis Teismas',
            u'Apeliacinis teismas': u'Lietuvos apeliacinis teismas',
            u'Konstitucinis Teismas': u'Lietuvos Respublikos Konstitucinis Teismas',
            u'LŽŪBA': u'Lietuvos žemės ūkio bendrovių asociacija',
            u'Kelių policijos tarnyba': u'Lietuvos kelių policijos tarnyba',
            u'Laisvosios rinkos institutas': u'Lietuvos laisvosios rinkos institutas',
            u'VŠĮ Lietuvos laisvosios rinkos institutas': u'Lietuvos laisvosios rinkos institutas',
        }.get(submitter, submitter)
        return submitter

    @staticmethod
    def _normalize_dates(s):
        return date_re.sub(lambda m: '%04d-%02d-%02d' % (
            int(m.group(1)), month_names_map[m.group(2)], int(m.group(3))), s)

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
