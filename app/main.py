from fastapi import FastAPI
from .routers import leaderboards, search

app = FastAPI(title="YT Topic Finder API")

app.include_router(search.router)
app.include_router(leaderboards.router)

@app.get("/")
def root():
    return {"ok": True, "service": "yt-topic-finder"}
