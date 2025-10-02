from googleapiclient.discovery import build
from typing import Dict, List

from ..config import YOUTUBE_API_KEY

def get_client():
    if not YOUTUBE_API_KEY:
        raise RuntimeError("YOUTUBE_API_KEY is not set")
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def chunked(iterable, size):
    buf = []
    for x in iterable:
        buf.append(x)
        if len(buf) == size:
            yield buf
            buf = []
    if buf:
        yield buf

def discover_videos(category_id: str, region: str, start_iso: str, end_iso: str, pages: int = 1, q: str | None = None) -> List[str]:
    yt = get_client()
    out: List[str] = []
    page_token = None
    for _ in range(pages):
        res = yt.search().list(
            part="id",
            type="video",
            videoCategoryId=category_id,
            publishedAfter=start_iso,
            publishedBefore=end_iso,
            regionCode=region,
            order="viewCount",
            maxResults=50,
            pageToken=page_token,
            q=q
        ).execute()
        for it in res.get("items", []):
            vid = (it.get("id") or {}).get("videoId")
            if vid:
                out.append(vid)
        page_token = res.get("nextPageToken")
        if not page_token:
            break
    # de-dupe preserving order
    seen, uniq = set(), []
    for v in out:
        if v not in seen:
            uniq.append(v)
            seen.add(v)
    return uniq

def fetch_videos(video_ids: List[str]) -> List[dict]:
    yt = get_client()
    items: List[dict] = []
    for ids in chunked(video_ids, 50):
        res = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids)).execute()
        items.extend(res.get("items", []))
    return items

def fetch_channels(channel_ids: List[str]) -> Dict[str, dict]:
    yt = get_client()
    out: Dict[str, dict] = {}
    for ids in chunked(channel_ids, 50):
        res = yt.channels().list(part="snippet,statistics", id=",".join(ids)).execute()
        for it in res.get("items", []):
            out[it["id"]] = it
    return out
