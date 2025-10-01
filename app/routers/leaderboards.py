from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from datetime import datetime

router = APIRouter(prefix="/api/leaderboards", tags=["leaderboards"])

@router.get("/category", response_model=schemas.LeaderboardResponse)
def category_leaderboard(categoryId: str, limit: int = 10, db: Session = Depends(get_db)):
    row = db.query(models.Leaderboard).filter(
        models.Leaderboard.board_scope == "category_12m",
        models.Leaderboard.scope_key == categoryId
    ).order_by(models.Leaderboard.computed_at.desc()).first()
    if not row:
        return {"scope": "category_12m", "scope_key": categoryId, "computed_at": datetime.utcnow(), "entries": []}
    return {"scope": "category_12m", "scope_key": categoryId, "computed_at": row.computed_at, "entries": row.entries[:limit]}

@router.get("/overall-30d", response_model=schemas.LeaderboardResponse)
def overall_30d(limit: int = 10, db: Session = Depends(get_db)):
    row = db.query(models.Leaderboard).filter(
        models.Leaderboard.board_scope == "overall_30d",
        models.Leaderboard.scope_key == "global"
    ).order_by(models.Leaderboard.computed_at.desc()).first()
    if not row:
        return {"scope": "overall_30d", "scope_key": "global", "computed_at": datetime.utcnow(), "entries": []}
    return {"scope": "overall_30d", "scope_key": "global", "computed_at": row.computed_at, "entries": row.entries[:limit]}
