from pydantic import BaseModel
from typing import List
from datetime import datetime

class LeaderboardEntry(BaseModel):
    rank: int
    video_id: str
    title: str
    channel_id: str
    channel_title: str
    vsr: float
    views: int
    subs: int
    published_at: datetime | None

class LeaderboardResponse(BaseModel):
    scope: str
    scope_key: str
    computed_at: datetime
    entries: List[LeaderboardEntry]

class SearchItem(BaseModel):
    video_id: str
    title: str
    channel_id: str
    channel_title: str
    published_at: datetime | None
    views: int
    subs: int
    vsr: float
    tags: List[str] = []

class SearchResponse(BaseModel):
    total: int
    items: List[SearchItem]

class Category(BaseModel):
    id: str
    name: str

class CategoriesResponse(BaseModel):
    categories: List[Category]
