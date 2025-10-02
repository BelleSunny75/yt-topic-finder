from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class VideoBase(BaseModel):
    video_id: str
    title: str
    description: Optional[str]
    category_id: str
    published_at: datetime
    duration_seconds: Optional[int]
    view_count: int
    like_count: Optional[int]
    comment_count: Optional[int]
    tags: Optional[List[str]]
    view_sub_ratio: Optional[float]
    meets_rule: bool

    class Config:
        orm_mode = True

class ChannelBase(BaseModel):
    channel_id: str
    title: str
    subscriber_count: int
    hidden_subscriber_count: Optional[bool]
    country: Optional[str]

    class Config:
        orm_mode = True

class LeaderboardEntry(BaseModel):
    video_id: str
    title: str
    channel_title: str
    view_count: int
    subscriber_count: int
    view_sub_ratio: float

class Leaderboard(BaseModel):
    board_scope: str
    scope_key: str
    computed_at: datetime
    entries: List[LeaderboardEntry]
