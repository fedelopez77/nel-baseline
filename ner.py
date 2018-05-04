"""
Wrapper to use Stanford NER
https://nlp.stanford.edu/software/CRF-NER.shtml

Requires: java 1.8

This module assumes that the folder with the Stanford NER is located in STANFORD_PATH
(path/to/nel-baseline/stanford-ner by default)

The output format can be changed from the parameter -outputFormat
Available options in https://nlp.stanford.edu/software/crf-faq.html#j
"""

import os
import subprocess

STANFORD_PATH = "stanford-ner"
NER_COMMAND = "java -mx600m -cp stanford-ner.jar:lib/* edu.stanford.nlp.ie.crf.CRFClassifier " \
              "-loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -outputFormat inlineXML " \
              "-textFile {}"


def detect(source_file, target_file="output-ner.tsv"):
    stanford_ner_path = os.path.join(os.getcwd(), STANFORD_PATH)
    file_path = os.path.join(os.getcwd(), source_file)
    with open(target_file, 'w') as f:
        subprocess.run(NER_COMMAND.format(file_path), shell=True, stdout=f, stderr=subprocess.DEVNULL,
                       cwd=stanford_ner_path)
