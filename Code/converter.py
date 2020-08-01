import json
import pandas as pd
import os


def convert_apple():
    data = pd.read_csv('AppStore (за год).csv')
    res = []
    for i, row in data.iterrows():
        res.append({
            'title': row['Title'],
            'text': row['Review']
        })
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


convert_apple()
convert_google()
convert_common()