
import os.path
from six import u as unicode
from collections import OrderedDict
import codecs
from whoosh.fields import Schema, TEXT, KEYWORD, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.query import *


INDEX_PATH = "index"
ARTICLES_PATH = "wikidumps/articles.tsv"
REDIRECTS_PATH = "wikidumps/redirects.tsv"
REDIRECTS_KEY = "redirects"


def get_titles():
    titles = {}
    with codecs.open(ARTICLES_PATH, "r", "utf-8") as f:
        for line in f:
            art_id, title = line.split("\t")
            if title in titles:
                print("Repeated title: {}".format(title))

            titles[title] = {"id": id}

    return titles


def update_with_redirects(titles):
    with codecs.open(REDIRECTS_PATH, "r", "utf-8") as f:
        for line in f:
            redir_id, redirect, title = line.split("\t")

            if title in titles:
                value = titles[title]
                if REDIRECTS_KEY in value:
                    value[REDIRECTS_KEY].append(redirect)
                else:
                    value[REDIRECTS_KEY] = [redirect]
            else:
                print("Target title of redirect not present: {} -> {}".format(redirect, title))

    return titles


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

    for title in documents:
        value = documents[title]

        if REDIRECTS_KEY in value:
            redirects = ",".join(value[REDIRECTS_KEY])
            writer.add_document(title=title, id=value["id"], redirects=redirects)
        else:
            writer.add_document(title=title, id=value["id"])

    writer.commit()


def build_index():
    """
    *API call* to build the index
    """
    if os.path.exists(INDEX_PATH):
        raise FileExistsError("{} already exists".format(INDEX_PATH))

    create_index(INDEX_PATH)

    titles = get_titles()
    update_with_redirects(titles)
    add_documents_to_index(titles, INDEX_PATH)


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

    candidates = OrderedDict()      # I add the results to an ordered dict so I can filter repetitions
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


build_index()