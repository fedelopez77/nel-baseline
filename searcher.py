
import os.path
from six import u as unicode
from collections import OrderedDict
from whoosh.fields import Schema, TEXT, KEYWORD, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.query import *

# source: target
docs = {
    'AbacuS, foo, bar, baz': 'Abacus',
    'AbalonE': 'Abalone',
    'AccessibleComputing': 'Computer accessibility',
    'AfghanistanCommunications': 'Communications in Afghanistan',
    'AfghanistanGeography': 'Geography of Afghanistan',
    'AfghanistanHistory': 'History of Afghanistan',
    'AfghanistanMilitary': 'Afghan Armed Forces',
    'AfghanistanPeople': 'Demographics of Afghanistan',
    'AfghanistanTransnationalIssues': 'Foreign relations of Afghanistan',
    'AfghanistanTransportations': 'Transport in Afghanistan',
    'AfroAsiaticLanguages': 'Afroasiatic languages',
    'AlbaniaEconomy': 'Economy of Albania',
    'AlbaniaGovernment': 'Politics of Albania',
    'AlbaniaHistory': 'History of Albania',
    'AlbaniaPeople': 'Demographics of Albania',
    'AmoeboidTaxa': 'Amoeba',
    'ArtificalLanguages': 'Constructed language',
    'AsWeMayThink': 'As We May Think',
    'AssistiveTechnology': 'Assistive technology'
}

INDEX_PATH = "index"


def create_schema():
    # Possible Variations: redirects=TEXT
    return Schema(title=TEXT(stored=True),
                  redirects=KEYWORD(commas=True, scorable=True),
                  id=ID(stored=True))


def create_index(index_dir="index"):
    os.mkdir(index_dir)
    schema = create_schema()
    create_in(index_dir, schema)


def add_documents_to_index(documents, index_dir):
    ix = open_dir(index_dir)

    writer = ix.writer()

    for redirect, title in documents.items():
        # Falta write id
        writer.add_document(title=title, redirects=redirect)

    writer.commit()


def build_index():
    if not os.path.exists(INDEX_PATH):
        create_index(INDEX_PATH)
        add_documents_to_index(docs, INDEX_PATH)


def get_candidates_for_head_string(head_string, searcher, query_parsers):
    """
    Allow hierarchical search following the order of the query parsers
    :param head_string: from the mention
    :param searcher:
    :param query_parsers: <list>
    :return: *ordered* list of candidates, from most likely to less
    """

    # acá tengo para jugar con:
    # * Head string: Partirla si es más de una palabra, usar solo las iniciales, etc
    # * Búsquedas difusas (con * y ?), combinaciones de ANDs y/o ORs
    # * La jerarquía de los parsers
    # * el limite de candidatos que devuelvo

    candidates = OrderedDict()
    for parser in query_parsers:
        query = parser.parse(head_string)
        results = searcher.search(query)
        for hit in results:
            candidates[hit["title"]] = None    # ver si pongo titles, ids o que
    return list(candidates.keys())


def get_candidates(strings):
    """
    :param strings: <list> of head strings from mentions
    :return: dictionary of head_string:candidates<list>
    """
    ix = open_dir(INDEX_PATH)
    heads_and_candidates = {}
    with ix.searcher() as searcher:
        title_qp = QueryParser("title", schema=ix.schema)
        redirects_qp = QueryParser("redirects", schema=ix.schema)
        parsers = [title_qp, redirects_qp]
        for head_string in strings:
            heads_and_candidates[head_string] = get_candidates_for_head_string(head_string, searcher, parsers)

    return heads_and_candidates














































