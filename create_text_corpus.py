import os
import nltk.data
from nltk.corpus import stopwords
import re
import logging
import sys
from utils import xml_gz2txt

# configuration

DATA_PATH = 'assets/raw_abstract_texts/'
TARGET_FOLDER = 'assets/corpus/'
REMOVE_PUNCT = True
REMOVE_STOPWORDS = True
LOWERCASE = True
XML2TXT = True

if XML2TXT:
    xml_gz2txt(raw_data='assets/pubmed/',processed_data = DATA_PATH)


target = TARGET_FOLDER + 'pubmed18.'
if REMOVE_PUNCT:
    target += 'p'
if LOWERCASE:
    target += 'l'
if REMOVE_STOPWORDS:
    target += 's'
target += '.txt'


sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
punctuation_tokens = ['.', '..', '...', ',', ';', ':', '(', ')', '"', '\'', '[', ']', '{', '}', '?', '!', '-', u'–',
                      '+', '*', '--', '\'\'', '``', "'"]
punctuation = '?.!/;:()&+'


logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# get stopwords
stop_words = stopwords.words('english')

fns = [fn for fn in os.listdir(DATA_PATH) if not fn.startswith('.')]
num_files = len(fns)

if not os.path.exists(TARGET_FOLDER):
    os.makedirs(TARGET_FOLDER)

output = open(target, 'a')
for k, fn in enumerate(fns):
    i = 1
    with open(DATA_PATH + fn, 'r') as infile:
        for line in infile:

            words = nltk.word_tokenize(line)
            if LOWERCASE:
                words = [x.lower() for x in words]
            # filter punctuation and stopwords
            if REMOVE_PUNCT:
                words = [x for x in words if x not in punctuation_tokens]
                words = [re.sub('[' + punctuation + ']', '', x) for x in words]
            if REMOVE_STOPWORDS:
                words = [x for x in words if x not in stop_words]
            # write one sentence per line in output file, if sentence has more than 1 word
            if len(words) > 1:
                output.write(' '.join(words) + '\n')
                    # process each sentence
        if i % 1000 == 0:
            logging.info('file %s of %s : preprocessing sentence %s ',k+1, num_files, i)
        i += 1
output.close()
logging.info('preprocessing finished!')
