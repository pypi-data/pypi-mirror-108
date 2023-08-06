# -*- coding: utf-8 -*-

"""
Japanese Multilingual Named Entity Dictionary (JMnedict) in SQLite format

References:
    ENAMDICT/JMnedict - Japanese Proper Names Dictionary Files
        https://www.edrdg.org/enamdict/enamdict_doc.html
"""

# This code is a part of jamdict library: https://github.com/neocl/jamdict
# :copyright: (c) 2020 Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

import os
import logging
from typing import Sequence

from puchikarui import Schema
from . import __version__ as JAMDICT_VERSION, __url__ as JAMDICT_URL
from .jmdict import Meta, JMDEntry, KanjiForm, KanaForm, Translation, SenseGloss

# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

MY_FOLDER = os.path.dirname(os.path.abspath(__file__))
SCRIPT_FOLDER = os.path.join(MY_FOLDER, 'data')
JMNEDICT_SETUP_FILE = os.path.join(SCRIPT_FOLDER, 'setup_jmnedict.sql')
JMNEDICT_VERSION = '1.08'
JMNEDICT_URL = 'https://www.edrdg.org/enamdict/enamdict_doc.html'
JMNEDICT_DATE = '2020-05-29'
JMNEDICT_SETUP_SCRIPT = '''INSERT INTO meta VALUES ('jmnedict.version', '{jv}');
INSERT INTO meta VALUES ('jmnedict.url', '{ju}');
INSERT INTO meta VALUES ('jmnedict.date', '{jud}');
INSERT INTO meta SELECT 'generator', 'jamdict' WHERE NOT EXISTS (SELECT 1 FROM meta WHERE key = 'generator');
INSERT INTO meta SELECT 'generator_version', '{gv}' WHERE NOT EXISTS (SELECT 1 FROM meta WHERE key = 'generator_version');
INSERT INTO meta SELECT 'generator_url', '{gu}' WHERE NOT EXISTS (SELECT 1 FROM meta WHERE key = 'generator_url');'''.format(
    jv=JMNEDICT_VERSION,
    ju=JMNEDICT_URL,
    jud=JMNEDICT_DATE,
    gv=JAMDICT_VERSION,
    gu=JAMDICT_URL
)


def getLogger():
    return logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# Models
# -------------------------------------------------------------------------------

class JMNEDictSchema(Schema):

    def __init__(self, db_path, *args, **kwargs):
        super().__init__(db_path, *args, **kwargs)
        self.add_script(JMNEDICT_SETUP_SCRIPT)
        self.add_file(JMNEDICT_SETUP_FILE)
        # Meta
        self.add_table('meta', ['key', 'value'], proto=Meta).set_id('key')
        self.add_table('NEEntry', ['idseq'])
        # Kanji
        self.add_table('NEKanji', ['ID', 'idseq', 'text'])
        # Kana
        self.add_table('NEKana', ['ID', 'idseq', 'text', 'nokanji'])
        # Translation (~Sense of JMdict)
        self.add_table('NETranslation', ['ID', 'idseq'])
        self.add_table('NETransType', ['tid', 'text'])
        self.add_table('NETransXRef', ['tid', 'text'])
        self.add_table('NETransGloss', ['tid', 'lang', 'gend', 'text'])


class JMNEDictSQLite(JMNEDictSchema):

    def __init__(self, db_path, *args, **kwargs):
        super().__init__(db_path, *args, **kwargs)

    def all_ne_type(self, ctx=None):
        if ctx is None:
            return self.all_ne_type(ctx=self.ctx())
        else:
            return [x['text'] for x in ctx.execute("SELECT DISTINCT text FROM NETransType")]

    def _build_ne_search_query(self, query):
        _is_wildcard_search = '_' in query or '@' in query or '%' in query
        if _is_wildcard_search:
            where = "idseq IN (SELECT idseq FROM NEKanji WHERE text like ?) OR idseq IN (SELECT idseq FROM NEKana WHERE text like ?) OR idseq IN (SELECT idseq FROM NETranslation JOIN NETransGloss ON NETranslation.ID == NETransGloss.tid WHERE NETransGloss.text like ?) OR idseq IN (SELECT idseq FROM NETranslation JOIN NETransType ON NETranslation.ID == NETransType.tid WHERE NETransType.text like ?)"
        else:
            where = "idseq IN (SELECT idseq FROM NEKanji WHERE text == ?) OR idseq IN (SELECT idseq FROM NEKana WHERE text == ?) OR idseq IN (SELECT idseq FROM NETranslation JOIN NETransGloss ON NETranslation.ID == NETransGloss.tid WHERE NETransGloss.text == ?) or idseq in (SELECT idseq FROM NETranslation JOIN NETransType ON NETranslation.ID == NETransType.tid WHERE NETransType.text == ?)"
        params = [query, query, query, query]
        try:
            if query.startswith('id#'):
                query_int = int(query[3:])
                if query_int >= 0:
                    where = "idseq = ?"
                    params = [query_int]
        except Exception:
            pass
        getLogger().debug(f"where={where} | params={params}")
        return where, params

    def search_ne(self, query, ctx=None, **kwargs) -> Sequence[JMDEntry]:
        if ctx is None:
            with self.ctx() as ctx:
                return self.search_ne(query, ctx=ctx)
        where, params = self._build_ne_search_query(query)
        where = 'SELECT idseq FROM NEEntry WHERE ' + where
        entries = []
        for (idseq,) in ctx.conn.cursor().execute(where, params):
            entries.append(self.get_ne(idseq, ctx=ctx))
        return entries

    def search_ne_iter(self, query, ctx=None, **kwargs):
        if ctx is None:
            with self.ctx() as ctx:
                return self.search_ne(query, ctx=ctx)
        where, params = self._build_ne_search_query(query)
        where = 'SELECT idseq FROM NEEntry WHERE ' + where
        for (idseq,) in ctx.conn.cursor().execute(where, params):
            yield self.get_ne(idseq, ctx=ctx)

    def get_ne(self, idseq, ctx=None) -> JMDEntry:
        # ensure context
        if ctx is None:
            with self.ctx() as new_context:
                return self.get_entry(idseq, new_context)
        # else (a context is provided)
        # select entry & info
        entry = JMDEntry(idseq)
        # select kanji
        kanjis = ctx.NEKanji.select('idseq=?', (idseq,))
        for dbkj in kanjis:
            kj = KanjiForm(dbkj.text)
            entry.kanji_forms.append(kj)
        # select kana
        kanas = ctx.NEKana.select('idseq=?', (idseq,))
        for dbkn in kanas:
            kn = KanaForm(dbkn.text, dbkn.nokanji)
            entry.kana_forms.append(kn)
        # select senses
        senses = ctx.NETranslation.select('idseq=?', (idseq,))
        for dbs in senses:
            s = Translation()
            # name_type
            nts = ctx.NETransType.select('tid=?', (dbs.ID,))
            for nt in nts:
                s.name_type.append(nt.text)
            # xref
            xs = ctx.NETransXRef.select('tid=?', (dbs.ID,))
            for x in xs:
                s.xref.append(x.text)
            # SenseGloss
            gs = ctx.NETransGloss.select('tid=?', (dbs.ID,))
            for g in gs:
                s.gloss.append(SenseGloss(g.lang, g.gend, g.text))
            entry.senses.append(s)
        return entry

    def insert_name_entities(self, entries, ctx=None):
        # ensure context
        if ctx is None:
            with self.ctx() as new_context:
                return self.insert_name_entities(entries, ctx=new_context)
        # else
        for entry in entries:
            self.insert_name_entity(entry, ctx)

    def insert_name_entity(self, entry, ctx=None):
        # ensure context
        if ctx is None:
            with self.ctx() as ctx:
                return self.insert_name_entity(entry, ctx=ctx)
        # else (a context is provided)
        self.NEEntry.insert(entry.idseq, ctx=ctx)
        # insert kanji
        for kj in entry.kanji_forms:
            ctx.NEKanji.insert(entry.idseq, kj.text)
        # insert kana
        for kn in entry.kana_forms:
            ctx.NEKana.insert(entry.idseq, kn.text, kn.nokanji)
        # insert translations
        for s in entry.senses:
            tid = ctx.NETranslation.insert(entry.idseq)
            # insert name_type
            for nt in s.name_type:
                ctx.NETransType.insert(tid, nt)
            # xref
            for xr in s.xref:
                ctx.NETransXRef.insert(tid, xr)
            # Gloss
            for g in s.gloss:
                ctx.NETransGloss.insert(tid, g.lang, g.gend, g.text)
