"""
# https://en.wikipedia.org/w/api.php?action=query&format=jsonfm&formatversion=2&pageids=307|655&prop=info&inprop=url
# QUERY: en lugar de usar wptools q es lento y trae cosas de mas, le puedo pegar a la api directo y sacar las urls de ahi

La idea es que el disambiguator, por ahora, solo linkee el pageid a la url del artículo
"""

import requests
from model import Entry

REQUEST_URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&pageids={ids}" \
              "&prop=info&inprop=url"


def disambiguate(mentions):
    """
    :param mentions:
    :return: dict {mention: entry}
    """
    main_candidates_ids = [mention.candidates[0][1] for mention in mentions if len(mention.candidates) > 0]
    wiki_urls = get_wiki_urls(main_candidates_ids)

    mentions_and_entries = {}
    for mention in mentions:
        main_candidate_id = mention.candidates[0][1] if len(mention.candidates) > 0 else None

        if main_candidate_id is None or main_candidate_id not in wiki_urls:
            entry = Entry(None)
        else:
            entry = Entry(wiki_urls[main_candidate_id])

        mentions_and_entries[mention] = entry

    return mentions_and_entries


def get_wiki_urls(wiki_ids):
    # No limpio repetidos porq paja, y porq eventualmente coreference deberia resolverlo
    wiki_urls = {}

    batch_size = 50
    for i in range(0, len(wiki_ids), batch_size):
        candidates_ids_batch = wiki_ids[i:i + batch_size]
        request_url = REQUEST_URL.format(ids="|".join(candidates_ids_batch))

        r = requests.get(request_url)

        for page in r.json()["query"]["pages"]:
            wiki_urls[str(page["pageid"])] = page["canonicalurl"]

    return wiki_urls
