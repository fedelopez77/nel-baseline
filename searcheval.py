
import argparse
from model import Mention
from searcher import get_candidates as search_for_candidates
from disambiguator import get_wiki_urls


def get_gold_links(filename):
    golds = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.split("\t")
            if len(line) < 4: continue

            head_string, link = line[2], line[4]

            if link[4] != "s":
                link = link[:4] + "s" + link[4:]

            golds[head_string] = link

    return golds


def get_candidates(head_strings):
    mentions = [Mention(string, None, 0, 0, "PERSON") for string in head_strings]
    search_for_candidates(mentions)



    mentions_and_entries = disambiguate(mentions)

    return {mention.head_string: mention.candidates for mention in mentions_and_entries}


def eval(golds, candidates, at_n):
    nil_correct = 0
    nil_total = 0
    link_at_n_correct = 0
    link_at_all_correct = 0
    link_total = 0

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

    nil_precision = float(nil_correct) / nil_total if nil_total != 0 else 0
    link_at_n_precision = float(link_at_n_correct) / link_total
    link_at_all_precision = float(link_at_all_correct) / link_total
    total_at_n_precision = float(nil_correct + link_at_n_correct) / (nil_total + link_total)
    total_at_all_precision = float(nil_correct + link_at_all_correct) / (nil_total + link_total)

    print("Nil Precision:\t{}".format(nil_precision))
    print("Precision@{}:\t{}".format(at_n, link_at_n_precision))
    print("Precision@all:\t{}".format(link_at_all_precision))
    print("Total P@{}:\t{}".format(at_n, total_at_n_precision))
    print("Total P@all:\t{}".format(total_at_all_precision))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Executes Search evaluation. Computes precision@n')
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
