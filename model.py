
from enum import Enum


class EntityType(Enum):
    PERSON = "PER"
    ORGANIZATION = "ORG"
    LOCATION = "LOC"


class EntityTypeBuilder:

    _entities = {entity.name: entity for entity in list(EntityType)}

    @classmethod
    def get(cls, type_name):
        return cls._entities[type_name]


class Mention:

    def __init__(self, id, head_string, doc_id, begin, end, entity_type, mention_type="NAM"):
        """
        :param id: mention (query) ID: unique for each entity name mention
        :param head_string: mention head string: the full head string of the entity name mention
        :param doc_id:
        :param begin:
        :param end:
        :param entity_type:
        :param mention_type:
        """
        self.id = id
        self.head_string = head_string
        self.doc_id = doc_id
        self.begin = begin
        self.end = end
        self.entity_type = EntityTypeBuilder.get(entity_type)
        self.mention_type = mention_type

    # def __str__(self):
    #     return "{}:{}: {} - '{}'".format(self.ini_line_number, self.end_line_number, self.cls, self.string)
    #
    # def __repr__(self):
    #     return "{}:{}: {} - '{}'".format(self.ini_line_number, self.end_line_number, self.cls, self.string)
    #
    # def add_word_to_mention(self, word):
    #     self.string += " " + word
    #     self.end_line_number += 1


class Entry:
    """
    It models the entry in a given knowledge base. For now it is just a wrapper for wptools.page.WPToolsPage
    """

    def __init__(self, page):
        self.page = page

    def is_nil(self):
        return not self.page


class LinkedMention:

    def __init__(self, mention, entry, confidence=1.0):
        """
        :param mention:
        :param entry: Entry in a KB
        """
        self.mention = mention
        self.entry = entry
        self.confidence = confidence

    def __str__(self):
        if not self.entry.is_nil():
            return "{} - {}".format(self.mention.head_string, self.entry.data["url"])
        return "{} - NIL".format(self.mention.head_string)

    def __repr__(self):
        if not self.entry.is_nil():
            return "{} - {}".format(self.mention.head_string, self.entry.data["url"])
        return "{} - NIL".format(self.mention.head_string)

