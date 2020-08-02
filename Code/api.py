from deeppavlov import build_model
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from text_analyzer import classify_reviews
from sentiment_analysis import settings
from repository import save_comment


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = build_model(settings, download=False)


@app.get('/CommentCommandAndMood')
async def search(comment):
    res = list(classify_reviews([comment]))
    emotion_cl = model([comment])[0][-1]
    emotion = None
    if emotion_cl < 0.5:
        emotion = 1
    if emotion_cl > 0.5:
        emotion = 0
    try:
        save_comment(comment, res[0] if res else None, emotion)
    except Exception as e:
        pass
    return {'command': res[0] if len(res) > 0 else None, 'mood': emotion}


uvicorn.run(app, host="0.0.0.0", port=3001)
