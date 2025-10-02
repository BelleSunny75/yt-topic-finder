from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from dateutil import parser as dtparser

from app.db import SessionLocal
from app import models
from app.services.youtube import discover_videos, fetch_videos, fetch_channels
from app.config import REGION_CODES
from app.util_categories import CATEGORIES

def ensure_channel(session: Session, ch: dict):
    cid = ch["id"]
    stats = ch.get("statistics", {})
    snip = ch.get("snippet", {})
    hidden = stats.get("hiddenSubscriberCount", False)
    subs = int(stats.get("subscriberCount", 0)) if not hidden else None

    row = session.get(models.Channel, cid) or models.Channel(channel_id=cid)
    row.title = snip.get("title")
    row.hidden_subscriber_count = bool(hidden)
    row.subscriber_count = subs if subs is not None else None
    row.country = snip.get("country")
    row.last_checked_at = datetime.utcnow()
    session.merge(row)

def iso8601_to_secs(s: str) -> int:
    if not s or not s.startswith("PT"):
        return 0
    h = m = sec = 0
    num = ""
    for ch in s[2:]:
        if ch.isdigit():
            num += ch
        else:
            if ch == "H": h = int(num or 0); num = ""
            elif ch == "M": m = int(num or 0); num = ""
            elif ch == "S": sec = int(num or 0); num = ""
    return h * 3600 + m * 60 + sec

def upsert_video(session: Session, v: dict, ch_map: dict):
    stats = v.get("statistics", {})
    snip = v.get("snippet", {})
    cd = v.get("contentDetails", {})

    vid = v["id"]
    cid = snip.get("channelId")
    ch = ch_map.get(cid, {})
    ch_stats = ch.get("statistics", {})
    hidden = ch_stats.get("hiddenSubscriberCount", False)
    subs = int(ch_stats.get("subscriberCount", 0)) if not hidden else None

    views = int(stats.get("viewCount", 0))
    vsr = (views / subs) if (subs and subs > 0) else None
    meets = bool(vsr is not None and vsr >= 5.0)

    published_dt = dtparser.parse(snip.get("publishedAt")) if snip.get("publishedAt") else None

    row = session.get(models.Video, vid) or models.Video(video_id=vid, first_seen_at=datetime.utcnow())
    row.channel_id = cid
    row.title = snip.get("title")
    row.description = snip.get("description", "")
    row.category_id = snip.get("categoryId")
    row.published_at = published_dt
    row.duration_seconds = iso8601_to_secs(cd.get("duration"))
    row.view_count = views
    row.like_count = int(stats.get("likeCount", 0)) if stats.get("likeCount") else None
    row.comment_count = int(stats.get("commentCount", 0)) if stats.get("commentCount") else None
    row.tags = snip.get("tags") or []
    row.subscriber_count_at_fetch = subs if subs is not None else None
    row.view_sub_ratio = float(vsr) if vsr is not None else None
    row.meets_rule = meets
    row.last_checked_at = datetime.utcnow()
    session.merge(row)

def crawl(window_days: int = 30, pages: int = 2):
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=window_days)
    end = now

    with SessionLocal() as s:
        for cat_id in CATEGORIES.keys():
            for region in REGION_CODES:
                video_ids = discover_videos(cat_id, region, start.isoformat(), end.isoformat(), pages=pages)
                if not video_ids:
                    continue
                vids = fetch_videos(video_ids)
                channel_ids = list({v["snippet"]["channelId"] for v in vids if v.get("snippet")})
                ch_map = fetch_channels(channel_ids)
                for ch in ch_map.values():
                    ensure_channel(s, ch)
                for v in vids:
                    upsert_video(s, v, ch_map)
                s.commit()
                print(f"[{region}] cat {cat_id}: stored {len(vids)} videos")

if __name__ == "__main__":
    crawl(window_days=30, pages=2)
