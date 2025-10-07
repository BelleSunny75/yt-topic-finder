from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..db import get_db
from .. import models

# main.py already adds prefix="/leaderboards", so we keep this router unprefixed
router = APIRouter(tags=["Leaderboards"])

@router.get("/category")
def category_leaderboard(categoryId: str, limit: int = 10, db: Session = Depends(get_db)):
    row = (
        db.query(models.Leaderboard)
        .filter(
            models.Leaderboard.board_scope == "category_12m",
            models.Leaderboard.scope_key == categoryId,
        )
        .order_by(models.Leaderboard.computed_at.desc())
        .first()
    )
    if not row:
        return {
            "scope": "category_12m",
            "scope_key": categoryId,
            "computed_at": datetime.utcnow(),
            "entries": [],
        }
    return {
        "scope": "category_12m",
        "scope_key": categoryId,
        "computed_at": row.computed_at,
        "entries": row.entries[:limit] if row.entries else [],
    }

@router.get("/overall-30d")
def overall_30d(limit: int = 10, db: Session = Depends(get_db)):
    row = (
        db.query(models.Leaderboard)
        .filter(
            models.Leaderboard.board_scope == "overall_30d",
            models.Leaderboard.scope_key == "global",
        )
        .order_by(models.Leaderboard.computed_at.desc())
        .first()
    )
    if not row:
        return {
            "scope": "overall_30d",
            "scope_key": "global",
            "computed_at": datetime.utcnow(),
            "entries": [],
        }
    return {
        "scope": "overall_30d",
        "scope_key": "global",
        "computed_at": row.computed_at,
        "entries": row.entries[:limit] if row.entries else [],
    }
