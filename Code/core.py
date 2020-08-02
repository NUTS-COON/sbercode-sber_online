import nltk
import re
import string


#nltk.download('punkt')
#nltk.download('stopwords')
stopwords = list(nltk.corpus.stopwords.words("russian")) + [
    'вс', 'все', 'всё', 'супер', 'прекрасно', 'отлично', 'очень', 'удобно', 'хорошо',
    'классно', 'молодцы', 'отлично', 'ок', 'нормально', 'спасибо', 'класс', 'норм',
    'приложение', 'быстро', 'просто', 'удобное', 'отзыв', 'сбербанк', 'онлайн',
    'лучшее', 'полезное', 'good', 'ok', 'отличное', 'банк'
]
punkt = string.punctuation + '«»'


def tokenizer(text, remove_stopwords=False):
    def _is_valid(x):
        if len(x) == 0:
            return False
        if remove_stopwords and x in stopwords:
            return False
        return True

    #words = nltk.word_tokenize(text.lower(), language="russian")
    text = text.lower()
    for ch in punkt:
        text = text.replace(ch, ' ')
    words = text.split()
    res = list(filter(_is_valid, words))
    return res
