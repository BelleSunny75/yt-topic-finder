from datetime import datetime, timedelta, timezone
from app.db import SessionLocal
from app import models

def compute_category_12m(session):
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=365)

    from app.util_categories import CATEGORIES
    for cat_id in CATEGORIES.keys():
        q = (session.query(models.Video, models.Channel)
             .join(models.Channel, models.Video.channel_id == models.Channel.channel_id)
             .filter(models.Video.meets_rule == True)
             .filter(models.Video.category_id == cat_id)
             .filter(models.Video.published_at >= cutoff)
             .order_by(models.Video.view_sub_ratio.desc(), models.Video.view_count.desc())
             .limit(10))
        entries = []
        for rank, (v, c) in enumerate(q.all(), start=1):
            if v.view_sub_ratio is None:
                continue
            entries.append({
                "rank": rank,
                "video_id": v.video_id,
                "title": v.title,
                "channel_id": v.channel_id,
                "channel_title": c.title,
                "vsr": float(v.view_sub_ratio),
                "views": int(v.view_count or 0),
                "subs": int(c.subscriber_count or 0),
                "published_at": v.published_at.isoformat() if v.published_at else None
            })
        lb = models.Leaderboard(
            board_scope="category_12m",
            scope_key=cat_id,
            computed_at=now,
            entries=entries
        )
        session.add(lb)

def compute_overall_30d(session):
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=30)

    q = (session.query(models.Video, models.Channel)
         .join(models.Channel, models.Video.channel_id == models.Channel.channel_id)
         .filter(models.Video.meets_rule == True)
         .filter(models.Video.published_at >= cutoff)
         .order_by(models.Video.view_sub_ratio.desc(), models.Video.view_count.desc())
         .limit(10))
    entries = []
    for rank, (v, c) in enumerate(q.all(), start=1):
        if v.view_sub_ratio is None:
            continue
        entries.append({
            "rank": rank,
            "video_id": v.video_id,
            "title": v.title,
            "channel_id": v.channel_id,
            "channel_title": c.title,
            "vsr": float(v.view_sub_ratio),
            "views": int(v.view_count or 0),
            "subs": int(c.subscriber_count or 0),
            "published_at": v.published_at.isoformat() if v.published_at else None
        })
    lb = models.Leaderboard(
        board_scope="overall_30d",
        scope_key="global",
        computed_at=now,
        entries=entries
    )
    session.add(lb)

def main():
    with SessionLocal() as s:
        compute_category_12m(s)
        compute_overall_30d(s)
        s.commit()
        print("Leaderboards computed.")

if __name__ == "__main__":
    main()
