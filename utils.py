"""
script for getting Abtract element of zipped xml files and writing the texts as lines in a .txt file
"""
import os
from gzip import GzipFile
from xml.etree import ElementTree as etree

def xml_gz2txt(raw_data='assets/pubmed/',processed_data = 'assets/raw_abstract_texts/'):


    fns = [f for f in os.listdir(raw_data) if f.endswith('.xml.gz')]


    def getelements(filename_or_file, tag):
        """Yield *tag* elements from *filename_or_file* xml incrementaly."""
        context = iter(etree.iterparse(filename_or_file, events=('start', 'end')))
        _, root = next(context) # get root element
        for event, elem in context:
            if event == 'end' and elem.tag == tag:
                yield elem
                root.clear()

    for k, fn in enumerate(fns):
        print(k)
        texts = []
        with GzipFile(raw_data + fn) as xml_file:
            for elem in getelements(xml_file, 'AbstractText'):
                texts.append(elem.text)
        try:
            with open(processed_data + fn[:-7] + '.txt', 'w') as f:
                f.write('\n'.join(texts))
        except TypeError:
            pass

class CorpusSentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in [fn for fn in os.listdir(self.dirname) if not fn.startswith('.')]:
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()