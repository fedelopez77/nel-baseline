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

STANFORD_PATH = "stanford-ner"

THREE_CLASS_CLASSIFIER = "classifiers/english.all.3class.distsim.crf.ser.gz"
FOUR_CLASS_CLASSIFIER = "classifiers/english.conll.4class.distsim.crf.ser.gz"
SEVEN_CLASS_CLASSIFIER = "english.muc.7class.distsim.crf.ser.gz"

classifiers = {
    3: THREE_CLASS_CLASSIFIER,
    4: FOUR_CLASS_CLASSIFIER,
    7: SEVEN_CLASS_CLASSIFIER
}

NER_COMMAND = "java -mx600m -cp stanford-ner.jar:lib/* edu.stanford.nlp.ie.crf.CRFClassifier " \
              "-loadClassifier {classifier} -outputFormat {output_format} -textFile {text_file}"


def detect(source_file, target_file="output-ner", classes=3, output_format="tabbedEntities"):
    stanford_ner_path = os.path.join(os.getcwd(), STANFORD_PATH)
    file_path = os.path.join(os.getcwd(), source_file)

    command = NER_COMMAND.format(classifier=classifiers[classes], output_format=output_format, text_file=file_path)

    with open(target_file, 'w') as f:
        subprocess.run(command, shell=True, stdout=f, stderr=subprocess.DEVNULL, cwd=stanford_ner_path)
