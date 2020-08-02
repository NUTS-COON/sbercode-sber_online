import json
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from joblib import load, dump
import numpy as np
import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from core import tokenizer, stopwords


class NewTfidfVectorizer(TfidfVectorizer):
    def _valid_ngram(self, ngram, stop_words):
        if len(ngram) == 1 and ngram[0] in stop_words:
            return False
        for w in ngram[1:]:
            if w in stop_words:
                return False
        return True

    def _word_ngrams(self, tokens, stop_words=None):
        tokens = super(TfidfVectorizer, self)._word_ngrams(tokens, None)

        if stop_words is not None:
            new_tokens = []
            for token in tokens:
                if self._valid_ngram(token.split(' '), stop_words):
                    new_tokens.append(token)
            return new_tokens

        return tokens


common_data = pd.read_json('common.json', orient='records')
review_data = pd.concat([pd.read_json('apple.json', orient='records'),
                         pd.read_json('google.json', orient='records')])
common_corpus = list(set([('. '.join(filter(None, t))).strip('. ') for t in common_data.itertuples(index=False, name=None)]))
review_corpus = list(set([('. '.join(filter(None, t))).strip('. ') for t in review_data.itertuples(index=False, name=None)]))
print('load data', len(common_data), 'common corpus', len(review_corpus), 'review corpus')

tfidf_file = '1/tfidf.joblib'
if os.path.exists(tfidf_file):
    tfidf = load(tfidf_file)
else:
    tfidf = NewTfidfVectorizer(stop_words=stopwords, tokenizer=tokenizer, ngram_range=(1, 3))
    tfidf.fit(common_corpus + review_corpus)
    dump(tfidf, tfidf_file)
print('fit tdidf')

train = list([TaggedDocument(tokenizer(t, True), [i]) for i, t in enumerate(review_corpus)])

for size in [50, 100]:
    for window in [5, 10]:
        model_file = '1/doc2vec_s%s_w_%s.model' % (size, window)
        if os.path.exists(model_file):
            model = Doc2Vec.load(model_file)
        else:
            model = Doc2Vec(train, vector_size=size, window=window)
            model.save(model_file)
        X = model.docvecs.vectors_docs
        print('fit doc2vec', size, window)

        for n_clusters in [100]:
            clf = KMeans(n_clusters=n_clusters)
            clf.fit(X)
            dump(clf, '1/kmeans_s%s_w%s_cl%s.joblib' % (size, window, n_clusters))
            print('fit kmeans', size, window, n_clusters)

            d = {}
            for i in range(len(clf.labels_)):
                if clf.labels_[i] in d:
                    d[clf.labels_[i]].append(review_corpus[i])
                else:
                    d[clf.labels_[i]] = [review_corpus[i]]

            all_res = []
            for cluster, texts in sorted(d.items(), key=lambda x: -len(x[1])):
                X = tfidf.transform(texts)
                feature_names = tfidf.get_feature_names()
                scores = zip(tfidf.get_feature_names(), np.asarray(X.sum(axis=0)).ravel())
                sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

                res = {
                    'cluster': int(cluster),
                    'size': len(texts),
                    'reviews': [],
                    'ngrams': []
                }

                for text in texts[:20]:
                    res['reviews'].append(text)
                for item in sorted_scores[:10]:
                    res['ngrams'].append({'ngram': item[0], 'score': item[1]})
                all_res.append(res)

            with open('1/kmeans_s%s_w%s_cl%s.json' % (size, window, n_clusters), 'w') as f:
                json.dump(all_res, f, ensure_ascii=False, indent=2)

            print('Done', size, window, n_clusters)
