from sqlalchemy import Column, String, BigInteger, Boolean, Integer, TIMESTAMP, Numeric, Text, ARRAY, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .db import Base

class Channel(Base):
    __tablename__ = "channels"
    channel_id = Column(String, primary_key=True)
    title = Column(String)
    subscriber_count = Column(BigInteger)
    hidden_subscriber_count = Column(Boolean, default=False)
    country = Column(String)
    last_checked_at = Column(TIMESTAMP)
    videos = relationship("Video", back_populates="channel")

class Video(Base):
    __tablename__ = "videos"
    video_id = Column(String, primary_key=True)
    channel_id = Column(String, ForeignKey("channels.channel_id"))
    title = Column(Text)
    description = Column(Text)
    category_id = Column(String)
    published_at = Column(TIMESTAMP)
    duration_seconds = Column(Integer)
    view_count = Column(BigInteger)
    like_count = Column(BigInteger)
    comment_count = Column(BigInteger)
    tags = Column(ARRAY(String))

    subscriber_count_at_fetch = Column(BigInteger)
    view_sub_ratio = Column(Numeric)
    meets_rule = Column(Boolean, default=False)

    first_seen_at = Column(TIMESTAMP)
    last_checked_at = Column(TIMESTAMP)

    channel = relationship("Channel", back_populates="videos")

class Leaderboard(Base):
    __tablename__ = "leaderboards"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    board_scope = Column(String)      # 'category_12m' or 'overall_30d'
    scope_key = Column(String)        # categoryId or 'global'
    computed_at = Column(TIMESTAMP)
    entries = Column(JSON)            # list of dicts
