from fastapi import FastAPI
from analyze import get_sentiment

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}