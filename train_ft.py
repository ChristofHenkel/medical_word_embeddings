from gensim.models import FastText
import logging
import os
import sys
from utils import CorpusSentences
logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



#config


def train_fasttext(corpus_folder ='assets/corpus/', target ='models/ft/', size = 300, window = 5, mincount = 100):


    sentences = CorpusSentences(corpus_folder)

    model = FastText(window=window,min_count=mincount,size=size)
    model.build_vocab(sentences)
    model.train(sentences,total_examples=model.corpus_count,epochs = 5)
    # store model

    if not os.path.exists(target):
        os.makedirs(target)

    model_fn = target + 'med_model_dim{}_win{}_min{}.bin'.format(size, window, mincount)

    model.save(model_fn)

    # test model
    model.most_similar('transglutaminase')

if __name__=='__main__':
    train_fasttext()