import numpy as np
import pandas as pd
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


common_data = pd.read_json('common.json', orient='records').head(1000)
review_data = pd.concat([pd.read_json('apple.json', orient='records').sample(20),
                         pd.read_json('google.json', orient='records').sample(20)])
common_corpus = [('. '.join(filter(None, t))).strip('. ') for t in common_data.itertuples(index=False, name=None)]
review_corpus = [('. '.join(filter(None, t))).strip('. ') for t in review_data.itertuples(index=False, name=None)]

tfidf = NewTfidfVectorizer(stop_words=stopwords, tokenizer=tokenizer, ngram_range=(1, 3))
tfidf.fit(common_corpus)
X = tfidf.transform(review_corpus)
feature_names = tfidf.get_feature_names()


# http://stackoverflow.com/questions/16078015/
def get_top_tf_idf_words(response, top_n=5):
    sorted_nzs = np.argsort(response.data)[:-(top_n+1):-1]
    return [feature_names[response.indices[i]] for i in sorted_nzs]


for i, x in enumerate(X[:30]):
    print("{0:70} Words: {1}".format(review_corpus[i][:60].replace('\n', ' '), get_top_tf_idf_words(x)))
