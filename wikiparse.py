# Simple example of streaming a Wikipedia 
# Copyright 2017 by Jeff Heaton, released under the The GNU Lesser General Public License (LGPL).
# https://www.heatonresearch.com/2017/03/03/python-basic-wikipedia-parsing.html
# -----------------------------
import xml.etree.ElementTree as etree
import codecs
import csv
import time
import os

PATH_WIKI_XML = '/data/nlp/lopezfo/'
FILENAME_WIKI = 'enwiki-20180520-pages-articles.xml'
FILENAME_ARTICLES = 'articles.tsv'
FILENAME_REDIRECT = 'redirects.tsv'


# Nicely formatted time string
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


def strip_tag_name(t):
    t = elem.tag
    idx = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t


pathWikiXML = os.path.join(PATH_WIKI_XML, FILENAME_WIKI)
pathArticles = os.path.join(PATH_WIKI_XML, FILENAME_ARTICLES)
pathArticlesRedirect = os.path.join(PATH_WIKI_XML, FILENAME_REDIRECT)

totalCount = 0
articleCount = 0
redirectCount = 0
title = None
start_time = time.time()

buffer_size = 20 * (1024**2)


with open(pathArticles, "w", buffering=buffer_size) as articlesFH, \
        open(pathArticlesRedirect, "w", buffering=buffer_size) as redirectFH:
    articlesFH.write("id\ttitle\n")
    redirectFH.write("id\ttitle\tredirect\n")

    print("Files open")

    for event, elem in etree.iterparse(pathWikiXML, events=('start', 'end')):
        tname = strip_tag_name(elem.tag)

        if event == 'start':
            if tname == 'page':
                title = ''
                id = -1
                redirect = ''
                inrevision = False
                ns = 0
            elif tname == 'revision':
                # Do not pick up on revision id's
                inrevision = True
        else:
            if tname == 'title':
                title = elem.text
            elif tname == 'id' and not inrevision:
                id = int(elem.text)
            elif tname == 'redirect':
                redirect = elem.attrib['title']
            elif tname == 'ns':
                ns = int(elem.text)
            elif tname == 'page':
                if len(redirect) > 0:
                    redirectCount += 1
                    redirectFH.write("{}\t{}\t{}\n".format(id, title, redirect))
                    # print("RED: {}\t{}\t{}\n".format(id, title, redirect))

                elif ns == 0:   # "pure" articles
                    articleCount += 1
                    articlesFH.write("{}\t{}\n".format(id, title))
                    # print("ART: {}\t{}\n".format(id, title))


                totalCount += 1

                if totalCount % 100000 == 0:
                    print("{:,}".format(totalCount))

            elem.clear()

elapsed_time = time.time() - start_time

print("Total pages: {:,}".format(totalCount))
print("Article pages: {:,}".format(articleCount))
print("Redirect pages: {:,}".format(redirectCount))
print("Elapsed time: {}".format(hms_string(elapsed_time)))
