import nltk
import string


#nltk.download('punkt')
#nltk.download('stopwords')
stopwords = list(nltk.corpus.stopwords.words("russian")) + [
    'вс', 'все', 'всё', 'супер', 'прекрасно', 'отлично', 'очень', 'удобно', 'хорошо',
    'классно', 'молодцы', 'отлично', 'ок', 'нормально', 'спасибо', 'класс', 'норм'
]
punkt = string.punctuation + '«»'


def tokenizer(text, remove_stopwords=False):
    def _is_valid(x):
        if x in punkt:
            return  False
        if remove_stopwords and x in stopwords:
            return False
        return True

    res = nltk.word_tokenize(text.lower(), language="russian")
    return list(filter(_is_valid, res))
