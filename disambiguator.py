"""
# https://en.wikipedia.org/w/api.php?action=query&format=jsonfm&formatversion=2&pageids=307|655&prop=info&inprop=url
# QUERY: en lugar de usar wptools q es lento y trae cosas de mas, le puedo pegar a la api directo y sacar las urls de ahi

La idea es que el disambiguator, por ahora, solo linkee el pageid a la url del artículo
"""

import requests
from model import Entry

def disambiguate(heads_and_mentions):
