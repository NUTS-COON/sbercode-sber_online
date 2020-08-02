import pandas as pd
import pymorphy2
from core import tokenizer
morph = pymorphy2.MorphAnalyzer()


review_data = pd.read_json('apple.json', orient='records', encoding="utf-8")
LABELS = {
    "messenger": {"диалог", "сообщение", "мессенджер", "чат"},
    "notification": {"push", "уведомление"},
    "release": {"весит", "гигабайт", "мб", "мегабайт"},
    "transaction": {"перевод", "карта", "камера"},
    "payments": {"платеж", "платить", "оплата"}
}


def add_to_dict(d, k, v):
    if k in d:
        d[k].append(v)
    else:
        d[k] = [v]


def normalize_labels():
    for k, v in LABELS.items():
        forms = set(v)
        for w in v:
            forms.update([p.normal_form for p in morph.parse(w)])

        LABELS[k] = forms


def find_label(tokens, min_w=1):
    labels = []
    for k, v in LABELS.items():
        i = set.intersection(v, set(tokens))
        if len(i) > min_w:
            labels.append(k)

    return labels


def classify_reviews(reviews):
    res = {}
    for i in reviews:
        tokens = tokenizer(i, True)
        if not tokens:
            continue
        normal_tokens = [morph.parse(t)[0].normal_form for t in tokens]
        match_labels = find_label(normal_tokens)
        if match_labels:
            for l in match_labels:
                add_to_dict(res, l, i + "\n\n")

    return res


normalize_labels()
# review_corpus = list(set([('. '.join(filter(None, t))).strip('. ') for t in review_data.itertuples(index=False, name=None)]))
# classes = classify_reviews(review_corpus)

# with open("res.json", "w") as fp:
#     json.dump(classes, fp)
