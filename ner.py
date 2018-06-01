"""
Wrapper to use Stanford NER
https://nlp.stanford.edu/software/CRF-NER.shtml

Requires: java 1.8

This module assumes that the folder with the Stanford NER is located in STANFORD_PATH
(path/to/nel-baseline/stanford-ner by default)

The output format can be changed from the parameter -outputFormat
Available options are: inlineXML, xml, tsv, tabbedEntities, slashTags
See https://nlp.stanford.edu/software/crf-faq.html#j
"""

import os
import subprocess

STANFORD_PATH = "stanford-core"

# THREE_CLASS_CLASSIFIER = "classifiers/english.all.3class.distsim.crf.ser.gz"
# FOUR_CLASS_CLASSIFIER = "classifiers/english.conll.4class.distsim.crf.ser.gz"
# SEVEN_CLASS_CLASSIFIER = "english.muc.7class.distsim.crf.ser.gz"
#
# classifiers = {
#     3: THREE_CLASS_CLASSIFIER,
#     4: FOUR_CLASS_CLASSIFIER,
#     7: SEVEN_CLASS_CLASSIFIER
# }
#
# NER_COMMAND = "java -mx600m -cp stanford-ner.jar:lib/* edu.stanford.nlp.ie.crf.CRFClassifier " \
#               "-loadClassifier {classifier} -outputFormat {output_format} -textFile {text_file}"

STANFORD_COMMAND = 'java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP ' \
                   '-annotators tokenize,ssplit,pos,lemma,ner,parse -outputFormat {output_format} -file {text_file}'


def detect(source_file, output_format="conll"):
    stanford_ner_path = os.path.join(os.getcwd(), STANFORD_PATH)
    file_path = os.path.join(os.getcwd(), source_file)
    output_file = source_file + "." + output_format

    command = STANFORD_COMMAND.format(output_format=output_format, text_file=file_path)

    subprocess.run(command, shell=True, stderr=subprocess.DEVNULL, cwd=stanford_ner_path)

    subprocess.run("mv {} {}".format(output_file, os.getcwd()), shell=True, cwd=stanford_ner_path)


# detect("sample.txt")