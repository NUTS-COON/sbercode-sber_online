from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import pandas as pd

from core import tokenizer


review_data = pd.concat([pd.read_json('apple.json', orient='records'),
                         pd.read_json('google.json', orient='records')])
review_corpus = set([('. '.join(filter(None, t))).strip('. ') for t in review_data.itertuples(index=False, name=None)])

train = list([TaggedDocument(tokenizer(t, True), [i]) for i, t in enumerate(review_corpus)])

for size in [50, 100]:
    for window in [5, 10]:
        model = Doc2Vec(train, vector_size=size, window=window)
        X = model.docvecs.vectors_docs
        pass