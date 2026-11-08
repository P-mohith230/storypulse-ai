from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas.schemas import StoryCatalogItem
from app.services.narrative.loader import story_loader

router = APIRouter()

@router.get("", response_model=List[StoryCatalogItem])
def list_stories(
    duration: Optional[int] = Query(None, description="Target session duration (2, 5, 10, 15)"),
    mood: Optional[str] = Query(None, description="User mood filter")
):
    catalog = story_loader.get_catalog(duration_filter=duration, mood_filter=mood)
    return catalog

@router.get("/{story_id}")
def get_story_details(story_id: str):
    story = story_loader.get_story(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

