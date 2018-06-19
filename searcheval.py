
import argparse
from model import Mention
from searcher import get_candidates as search_for_candidates
from disambiguator import get_wiki_urls


def get_gold_links(filename):
    print("Getting gold links from: {}".format(filename))

    golds = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.split("\t")
            if len(line) < 4: continue

            head_string, link = line[2], line[4]

            if link[0:3] != "NIL" and link[4] != "s":
                link = link[:4] + "s" + link[4:]

            golds[head_string] = link

    return golds


def get_candidates(head_strings):
    mentions = [Mention(string, None, 0, 0, "PERSON") for string in head_strings]

    print("Searching for candidates on index")
    search_for_candidates(mentions)

    candidate_urls = {}

    wiki_ids = set()
    for mention in mentions:
        for cand in mention.candidates:
            wiki_ids.add(cand[1])

    print("Searching for IDs on Wikipedia")
    wiki_urls = get_wiki_urls(list(wiki_ids))

    for mention in mentions:
        candidate_urls[mention.head_string] = [wiki_urls[candidate[1]] for candidate in mention.candidates if candidate[1] in wiki_urls]

    return candidate_urls


def eval(golds, candidates, at_n):
    nil_correct = 0
    nil_total = 0               # total of *relevant*
    link_at_n_correct = 0
    link_at_all_correct = 0
    link_total = 0              # total of *relevant*
                                # since the denominator is the *relevant* links, then the metric is recall

    for string in golds:
        if string not in candidates:
            raise ValueError("String was not part of the search: {}".format(string))

        gold_link = golds[string]
        mention_candidates = candidates[string]

        if gold_link[0:3] == "NIL":
            nil_total += 1
            if len(mention_candidates) == 0:
                nil_correct += 1

        else:
            link_total += 1

            if gold_link in mention_candidates[:at_n]:
                link_at_n_correct += 1
                link_at_all_correct += 1
            elif gold_link in mention_candidates:
                link_at_all_correct += 1

    assert nil_total + link_total == len(golds)

    nil_recall = float(nil_correct) / nil_total if nil_total != 0 else 0
    link_at_n_recall = float(link_at_n_correct) / link_total
    link_at_all_recall = float(link_at_all_correct) / link_total
    total_at_n_recall = float(nil_correct + link_at_n_correct) / (nil_total + link_total)
    total_at_all_recall = float(nil_correct + link_at_all_correct) / (nil_total + link_total)

    print("Nil Recall:\t{0:.3f}".format(nil_recall))
    print("Recall@{a}:\t{b:.3f}".format(a=at_n, b=link_at_n_recall))
    print("Recall@all:\t{0:.3f}".format(link_at_all_recall))
    print("Total R@{a}:\t{b:.3f}".format(a=at_n, b=total_at_n_recall))
    print("Total R@all:\t{0:.3f}".format(total_at_all_recall))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Executes Search evaluation. Computes recall@n')
    parser.add_argument('-g', '--gold', help='File with gold links')
    parser.add_argument('-n', '--atn', help='n from precision@n', default=5)

    args = parser.parse_args()

    if args.gold is None:
        parser.print_usage()
        exit(0)

    golds = get_gold_links(args.gold)

    candidates = get_candidates(golds)

    if len(golds) != len(candidates):
        raise ValueError("Golds and candidates of different length")

    eval(golds, candidates, int(args.atn))
