from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()

@router.get("/search")
def search_videos(
    query: str = Query(..., description="Search term for videos"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(10, description="Number of results to return")
):
    # Placeholder logic for now
    # Later we’ll hook this into YouTube Data API or stored results
    return {
        "query": query,
        "category": category,
        "limit": limit,
        "results": [
            {"title": "Sample Video 1", "views": 10000},
            {"title": "Sample Video 2", "views": 25000},
        ]
    }
