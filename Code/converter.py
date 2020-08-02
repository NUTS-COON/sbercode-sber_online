from deeppavlov import build_model
import json
import pandas as pd
import os

from sentiment_analysis import settings


def convert_apple():
    data = pd.read_csv('AppStore (за год).csv')
    res = []
    for i, row in data.iterrows():
        res.append({
            'title': row['Title'],
            'text': row['Review']
        })

    model = build_model(settings, download=False)
    for i in range(0, len(res), 1000):
        end_i = min(i + 1000, len(res))
        texts = [('. '.join(filter(None, [t['title'], t['text']]))).strip('. ') for t in res[i:end_i]]
        classes = model(texts)
        for j, cl in enumerate(classes):
            res[i + j]['emotion'] = 1 - 2 * cl[-1]

    with open('apple.json', 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)


def convert_google():
    res = []
    for f in sorted(os.listdir('Google Play. Оценки и отзывы (за год)')):
        data = pd.read_csv(os.path.join('Google Play. Оценки и отзывы (за год)', f), encoding='utf16')
        for i, row in data.iterrows():
            if isinstance(row['Review Title'], str) or isinstance(row['Review Text'], str):
                res.append({
                    'title': row['Review Title'] if isinstance(row['Review Title'], str) else None,
                    'text': row['Review Text'] if isinstance(row['Review Text'], str) else None
                })
        print(f)

    with open('google.json', 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)


def convert_common():
    res = []

    data = pd.read_csv('labeled.csv')
    for i, row in data.iterrows():
        res.append({
            'title': '',
            'text': row['comment'],
        })

    for filename in os.listdir('Telegram'):
        with open(os.path.join('Telegram', filename), 'r') as f:
            data = json.load(f)
        for row in data:
            res.append({
                'title': '',
                'text': row['text']
            })

    with open('common.json', 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)


def call_google_emotions():
    with open('google.json', 'r') as f:
        res = json.load(f)

    model = build_model(settings, download=False)
    for i in range(0, len(res), 1000):
        end_i = min(i + 1000, len(res))
        texts = [('. '.join(filter(None, [t['title'], t['text']]))).strip('. ') for t in res[i:end_i]]
        classes = model(texts)
        for j, cl in enumerate(classes):
            res[i + j]['emotion'] = 1 - 2 * cl[-1]

    with open('google.json', 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)


def calc_emotion_stat():
    res = {}
    for file in ['apple', 'google']:
        review_data = pd.read_json(file + '.json', orient='records')
        positive = 0
        negative = 0
        neutral = 0
        for i, row in review_data.iterrows():
            if row['emotion'] < -0.25:
                negative += 1
            elif row['emotion'] > 0.25:
                positive += 1
            else:
                neutral += 1

        res[file] = {'negative': negative, 'positive': positive, 'neutral': neutral}

    with open('emotion_stat2.json', 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

# convert_apple()
# convert_google()
# convert_common()
# call_google_emotions()
calc_emotion_stat()