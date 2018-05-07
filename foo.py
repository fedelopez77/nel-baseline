
import wptools


IGNORED_ENTITY_TYPES = {"ORDINAL", "NUMBER"}


class Mention:

    def __init__(self, string, cls, ini_line_number, end_line_number=-1):
        self.string = string
        self.cls = cls
        self.ini_line_number = ini_line_number
        self.end_line_number = end_line_number if end_line_number != -1 else ini_line_number

    def __str__(self):
        return "{}:{}: {} - '{}'".format(self.ini_line_number, self.end_line_number, self.cls, self.string)

    def __repr__(self):
        return "{}:{}: {} - '{}'".format(self.ini_line_number, self.end_line_number, self.cls, self.string)

    def add_word_to_mention(self, word):
        self.string += " " + word
        self.end_line_number += 1


class Entry:
    """
    It models the entry in a given knowledge base. For now it is just a wrapper for wptools.page.WPToolsPage
    """

    def __init__(self, page):
        self.page = page


class LinkedMention:

    def __init__(self, mention, entry):
        """
        :param mention:
        :param entry: Entry in a KB
        """
        self.mention = mention
        self.entry = entry

    def __str__(self):
        if self.entry:
            return "{} - {}".format(self.mention.string, self.entry.data["url"])
        return "{} - NIL".format(self.mention.string)

    def __repr__(self):
        if self.entry:
            return "{} - {}".format(self.mention.string, self.entry.data["url"])
        return "{} - NIL".format(self.mention.string)


def get_mentions_from_file(file_name):
    result = []
    i = 0
    previous_type = None
    with open(file_name, "r") as f:
        for line in f:
            if not line.strip():
                previous_type = None
                continue

            line = line.split('\t')
            entity_type = line[4]
            if entity_type != 'O' and entity_type not in IGNORED_ENTITY_TYPES:

                if entity_type == previous_type:
                    result[-1].add_word_to_mention(line[1])
                else:
                    result.append(Mention(line[1], line[4], i))

            i += 1
            previous_type = entity_type

    return result


def link_mentions(mentions):
    result = []
    for mention in mentions:
        try:
            page = wptools.page(mention.string).get_query()
        except LookupError:
            page = None

        result.append(LinkedMention(mention, page))

    return result
