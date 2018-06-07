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

from os import getcwd, remove, listdir
from os.path import join, basename, isfile
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
                   '-annotators tokenize,ssplit,pos,lemma,ner,parse -outputFormat {output_format} -filelist {file_list}'

TMP_FILE_LIST = "filelist.tmp.txt"


def write_filelist(files, stanford_ner_path):
    cwd = getcwd()
    with open(join(stanford_ner_path, TMP_FILE_LIST), 'w+') as f:
        for file_name in files:
            file_path = join(cwd, file_name) + "\n"
            f.write(file_path)


def detect(files, output_format="xml", output_dir=None):
    """
    :param files: <list>
    :param output_format:
    :return: list of files with NER result
    """
    stanford_ner_path = join(getcwd(), STANFORD_PATH)
    write_filelist(files, stanford_ner_path)

    print("Processing NER")
    command = STANFORD_COMMAND.format(output_format=output_format, file_list=TMP_FILE_LIST)
    subprocess.run(command, shell=True, stderr=subprocess.STDOUT, cwd=stanford_ner_path)
    remove(join(stanford_ner_path, TMP_FILE_LIST))

    output_files = [basename(file_name) + "." + output_format for file_name in files]
    print(output_files)
    all_output_files = " ".join(output_files)
    output_dir = getcwd() if output_dir is None else output_dir
    subprocess.run("mv -t {} {}".format(output_dir, all_output_files), shell=True, cwd=stanford_ner_path)

    return output_files


# dataset_path = join(getcwd(), "dataset/MSNBC/rawTexts/")
# files_to_process = []
# for file in [filename for filename in listdir(dataset_path) if isfile(join(dataset_path, filename))]:
#     files_to_process.append(join(dataset_path, file))
#
# detect(files_to_process, output_dir=join(getcwd(), "ner_results"))

# detect(["dataset/MSNBC/rawTexts/Bus16451112.txt"], output_dir=join(getcwd(), "ner_results"))

