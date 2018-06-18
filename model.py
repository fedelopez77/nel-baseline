
class EntityTypeBuilder:

    PERSON = "PER"
    ORGANIZATION = "ORG"
    LOCATION = "LOC"
    GEO_POLITICAL_ENTITY = "GPE"
    FACILITY = "FAC"

    _entities = {
        "PERSON": PERSON,
        "TITLE": PERSON,
        "ORGANIZATION": ORGANIZATION,
        "MISC": FACILITY,               ## QUE ES MISC?
        "LOCATION": LOCATION,
        "CITY": GEO_POLITICAL_ENTITY,
        "STATE_OR_PROVINCE": GEO_POLITICAL_ENTITY,
        "COUNTRY": GEO_POLITICAL_ENTITY,
        "NATIONALITY": GEO_POLITICAL_ENTITY        ## QUE ES NATIONALITY? GPE???
    }


    @classmethod
    def get(cls, type_name):
        return cls._entities[type_name]


class Mention:

    _id = 0

    def __init__(self, head_string, doc_id, begin, end, entity_type, mention_type="NAM"):
        """
        :param id: mention (query) ID: unique for each entity name mention
        :param head_string: mention head string: the full head string of the entity name mention
        :param doc_id:
        :param begin:
        :param end:
        :param entity_type:
        :param mention_type:
        """
        self.head_string = head_string
        self.doc_id = doc_id
        self.begin = int(begin)
        self.end = int(end)
        self.entity_type = EntityTypeBuilder.get(entity_type)
        self.mention_type = mention_type
        self.candidates = []

        self.id = "EL-" + str(Mention._id)
        Mention._id += 1

    def add(self, other_head_string, other_end):
        self.head_string += " " + other_head_string
        self.end = other_end

    def __str__(self):
        return "{id}\t{head}\t{doc_id}:{begin}-{end}\t{entity}\t{mention}".format(
            id=self.id, head=self.head_string, doc_id=self.doc_id, begin=self.begin, end=self.end,
            entity=self.entity_type, mention=self.mention_type)

    def __repr__(self):
        return "{id}\t{head}\t{doc_id}:{begin}-{end}\t{entity}\t{mention}".format(
            id=self.id, head=self.head_string, doc_id=self.doc_id, begin=self.begin, end=self.end,
            entity=self.entity_type, mention=self.mention_type)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Entry:
    """
    It models the entry in a given knowledge base. For now it is just a wrapper for wptools.page.WPToolsPage
    """

    _id = 0

    def __init__(self, page, https=True):
        self.page = page
        self.https = https
        self.id = Entry._id
        Entry._id += 1

    def is_nil(self):
        return not self.page

    def __str__(self):
        if self.is_nil():
            return "NIL" + str(self.id)
        url = self.page.data["url"]
        if self.https:
            return url
        return url[:4] + url[5:]    # removes s from https


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
        return "{mention_id}\t{mention_head}\t{doc_id}:{begin}-{end}\t{entry_ref}\t{entity_type}\t{mention_type}" \
               "\t{confidence_value}".format(
            mention_id=self.mention.id,
            mention_head=self.mention.head_string,
            doc_id=self.mention.doc_id,
            begin=self.mention.begin,
            end=self.mention.end,
            entry_ref=str(self.entry),
            entity_type=self.mention.entity_type,
            mention_type=self.mention.mention_type,
            confidence_value=self.confidence
        )

    def __repr__(self):
        return "{} - {}".format(self.mention.head_string, self.entry)
