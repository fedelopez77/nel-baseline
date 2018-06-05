"""
The purpose of this script is to convert the gold standards of the Wikifier ACE 2004 dataset to the TAC15 format
in order to be able to calculate the metrics over this.

Expected format:
run_id  mention_id  mention_head    doc_id  kb_entry    entity_type mention_type(NAM)   confidence_value

OJO! El entity type no lo tengo...

VER TEMA DEL OFFSET:
alcanza con Offset : Offset + length? (Creería que sí)
"""

from os import listdir, remove
from os.path import join, isfile
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from model import Mention, LinkedMention


def transform(file_name):
    try:
        tree = ET.parse(file_name)
    except ParseError:
        print("NOT well-formed file: {}".format(file_name))
        return []
    root = tree.getroot()
    doc_id = root.find("ReferenceFileName").text.strip()
    linked_mentions = []
    for ref_instance in root.findall("ReferenceInstance"):
        mention = create_mention(doc_id, ref_instance)
        entry = ref_instance.find("ChosenAnnotation").text.strip()
        if entry == "*null*":
            entry = "NIL"
        linked_mentions.append(LinkedMention(mention, entry))

    return linked_mentions


def create_mention(doc_id, token):
    head_string = token.find("SurfaceForm").text.strip()
    begin = int(token.find("Offset").text.strip())
    end = begin + int(token.find("Length").text.strip()) - 1
    entity_type = "PERSON"                 # This dataset doesn't have Entity type
    return Mention(head_string, doc_id, begin, end, entity_type)


def export_linked_mentions(file_name, linked_mentions):
    run_id = "ACE2004"
    with open(file_name + ".tab", "w+") as f:
        for linked_mention in linked_mentions:
            line = "{}\t{}\n".format(run_id, str(linked_mention))
            f.write(line)


if __name__ == "__main__":

    path = "dataset/ACE2004_Coref_Turking/ProblemsNoTranscripts/"

    all_linked_mentions = []
    empty_files = []
    for file_name, file_name_not_path in [(join(path, f), f) for f in listdir(path) if isfile(join(path, f))]:
        linked_mentions = transform(file_name)
        if not linked_mentions:
            print("File '{}' is empty".format(file_name))
            # empty_files.append(file_name_not_path)
        else:
            all_linked_mentions.extend(linked_mentions)

    export_linked_mentions("MY_GOLD", all_linked_mentions)
    # print("Empty files:")
    # print(" ".join(empty_files))
