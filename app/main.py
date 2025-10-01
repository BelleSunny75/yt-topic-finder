from fastapi import FastAPI
from app.routers import leaderboards, search

app = FastAPI(title="YT Topic Finder")

# Include routers
app.include_router(leaderboards.router, prefix="/leaderboards", tags=["Leaderboards"])
app.include_router(search.router, prefix="/search", tags=["Search"])

@app.get("/")
def root():
    return {"message": "Welcome to YT Topic Finder API"}
