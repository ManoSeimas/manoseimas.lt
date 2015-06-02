# coding: utf-8

from __future__ import unicode_literals

import re
import difflib
import datetime
import operator

clean_words_re = re.compile(r'ir|svarstymas|pateikimas|priėmimas')
clean_title_re = re.compile(r'[()[\]„“",  ]+')


def get_voting_for_stenogram(votings, title, dt):
    """Find voting for stenogram by stenogram topic title and datetime

    Parameters:
    - votings: list of dicts, each dict iscouchdb document with doc_type=voting
    - title: str, stenogram topic title
    - dt: datetime.datetime, stenogram tipic date and time

    Returns: str, voting _id, that matches given title and datetime

    """

    def clean_title(title):
        result = title.lower()
        result = clean_words_re.sub(' ', result)
        result = clean_title_re.sub(' ', result)
        return result

    title = clean_title(title)
    votings_by_ratio = []
    for doc in votings:
        _dt = datetime.datetime.strptime(doc['created'], '%Y-%m-%dT%H:%M:%SZ')
        _title = clean_title(' '.join([d['name'] for d in doc['documents']]))
        ratio = difflib.SequenceMatcher(None, title, _title).ratio()
        votings_by_ratio.append((ratio, abs(_dt - dt), doc['_id']))

    allowed_time_delta = datetime.timedelta(minutes=10)
    if votings_by_ratio:
        # Sort by delta asc and ratio desc
        votings_by_ratio.sort()
        votings_by_ratio.sort(key=operator.itemgetter(0), reverse=True)

        for ratio, delta, doc_id in votings_by_ratio:
            if ratio > 0.9 and delta < allowed_time_delta:
                return doc_id

            # If both ratio and delta are out of range, do not check the
            # others.
            if not (ratio > 0.9 or delta < allowed_time_delta):
                return None
