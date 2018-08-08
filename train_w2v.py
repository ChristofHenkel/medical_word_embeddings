import gensim
import logging
import os
import sys
from utils import CorpusSentences
logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



#config


def train_w2v(corpus_folder ='assets/corpus/', target ='models/w2v/', size = 300, window = 5, mincount = 100):


    sentences = CorpusSentences(corpus_folder)

    model = gensim.models.Word2Vec(sentences,
                                   size=size,
                                   window=window,
                                   min_count=mincount
                                   )

    # store model

    if not os.path.exists(target):
        os.makedirs(target)

    model_fn = target + 'med_model_dim{}_win{}_min{}.w2v'.format(size, window, mincount)

    model.save(model_fn)

    # test model
    model.most_similar('macrophages')

if __name__=='__main__':
    train_w2v()