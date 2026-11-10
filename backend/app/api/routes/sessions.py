import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from app.schemas.schemas import (
    CreateSessionRequest,
    SessionActionRequest,
    SessionStateResponse,
    SceneResponse,
    ClueSummary,
    ActiveCharacterInfo,
    SessionHistoryItem
)
from app.models.domain import StorySession, SessionAction
from app.repositories.session_repo import session_repo
from app.services.narrative.loader import story_loader
from app.services.narrative.engine import narrative_engine
from app.services.gnani.timbre_service import timbre_service

router = APIRouter()

@router.get("", response_model=List[SessionHistoryItem])
def list_sessions(limit: int = 20):
    sessions = session_repo.list_recent_sessions(limit=limit)
    history = []
    for s in sessions:
        history.append(SessionHistoryItem(
            session_id=s.session_id,
            story_id=s.story_id,
            status=s.status,
            current_scene_id=s.current_scene_id,
            duration_target=s.duration_target,
            mood_selected=s.mood_selected,
            discovered_clues_count=len(s.discovered_clues),
            started_at=s.started_at.isoformat(),
            is_completed=(s.status == "COMPLETED")
        ))
    return history

@router.post("", response_model=SessionStateResponse, status_code=201)
def create_session(payload: CreateSessionRequest):
    story = story_loader.get_story(payload.story_id)
    if not story:
        raise HTTPException(status_code=404, detail=f"Story '{payload.story_id}' not found")

    meta = story["meta"]
    initial_scene_id = meta.get("initial_scene_id")
    initial_scene = story["scenes"].get(initial_scene_id)
    if not initial_scene:
        raise HTTPException(status_code=500, detail="Initial scene missing in story definition")

    initial_clues = list(meta.get("initial_clues", []))
    session_id = str(uuid.uuid4())

    new_session = StorySession(
        session_id=session_id,
        user_id=payload.user_id,
        story_id=payload.story_id,
        current_scene_id=initial_scene_id,
        status="ACTIVE",
        duration_target=payload.duration_target,
        mood_selected=payload.mood_selected,
        discovered_clues=initial_clues,
        started_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session_repo.create_session(new_session)

    # Initial character voice line synthesis
    active_char_id = initial_scene.get("active_character_id", "narrator")
    char_raw = story["characters"].get(active_char_id, {})
    dialogue_text = initial_scene.get("dialogue", "")
    tts_result = timbre_service.synthesize_sync(
        text=dialogue_text,
        voice_id=char_raw.get("voice_id", "Nalini"),
        language=payload.preferred_lang
    )

    # Log initial opening action
    session_repo.log_action(SessionAction(
        action_id=str(uuid.uuid4()),
        session_id=session_id,
        scene_id=initial_scene_id,
        actor_type="CHARACTER",
        character_id=active_char_id,
        action_text=dialogue_text,
        audio_url=tts_result.get("audio_url")
    ))

    # Build response clues
    clues_summary = []
    for cid in initial_clues:
        c_raw = story["clues"].get(cid, {})
        clues_summary.append(ClueSummary(
            id=cid,
            title=c_raw.get("title", cid),
            description=c_raw.get("description", ""),
            thumbnail=c_raw.get("thumbnail", ""),
            discovered=True
        ))

    return SessionStateResponse(
        session_id=session_id,
        story_id=payload.story_id,
        current_scene=SceneResponse(
            scene_id=initial_scene_id,
            title=initial_scene.get("title", ""),
            background_image=initial_scene.get("background_image", ""),
            active_character=ActiveCharacterInfo(
                id=active_char_id,
                name=char_raw.get("name", "Narrator"),
                avatar_url=char_raw.get("avatar_url", "")
            ),
            dialogue=dialogue_text,
            audio_url=tts_result.get("audio_url"),
            suggested_actions=initial_scene.get("suggested_actions", []),
            audio_status=tts_result.get("status", "READY")
        ),
        discovered_clues=clues_summary,
        status="ACTIVE"
    )

@router.get("/{session_id}", response_model=SessionStateResponse)
def get_session_state(session_id: str):
    session = session_repo.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    story = story_loader.get_story(session.story_id)
    scene = story["scenes"].get(session.current_scene_id)
    active_char_id = scene.get("active_character_id", "narrator")
    char_raw = story["characters"].get(active_char_id, {})

    clues_summary = []
    for cid in session.discovered_clues:
        c_raw = story["clues"].get(cid, {})
        clues_summary.append(ClueSummary(
            id=cid,
            title=c_raw.get("title", cid),
            description=c_raw.get("description", ""),
            thumbnail=c_raw.get("thumbnail", ""),
            discovered=True
        ))

    return SessionStateResponse(
        session_id=session.session_id,
        story_id=session.story_id,
        current_scene=SceneResponse(
            scene_id=session.current_scene_id,
            title=scene.get("title", ""),
            background_image=scene.get("background_image", ""),
            active_character=ActiveCharacterInfo(
                id=active_char_id,
                name=char_raw.get("name", "Narrator"),
                avatar_url=char_raw.get("avatar_url", "")
            ),
            dialogue=scene.get("dialogue", ""),
            suggested_actions=scene.get("suggested_actions", [])
        ),
        discovered_clues=clues_summary,
        is_completed=(session.status == "COMPLETED"),
        ending_id=session.ending_id,
        status=session.status
    )

@router.post("/{session_id}/action", response_model=SessionStateResponse)
def perform_action(session_id: str, payload: SessionActionRequest):
    session = session_repo.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status == "COMPLETED":
        raise HTTPException(status_code=400, detail="Story session already completed")

    previous_scene_id = session.current_scene_id

    # 1. Log user action
    session_repo.log_action(SessionAction(
        action_id=str(uuid.uuid4()),
        session_id=session_id,
        scene_id=previous_scene_id,
        actor_type="USER",
        action_text=payload.action_text,
        input_modality=payload.input_modality
    ))

    # 2. Evaluate state transition deterministically
    session, scene_payload, newly_unlocked_clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text=payload.action_text
    )

    # 3. Update session in repository
    session_repo.update_session(session)

    # 4. Synthesize character voice line
    dialogue_text = scene_payload.get("dialogue", "")
    tts_result = timbre_service.synthesize_sync(
        text=dialogue_text,
        voice_id=scene_payload.get("voice_id", "Nalini"),
        language="en-IN"
    )

    # 5. Log character response
    session_repo.log_action(SessionAction(
        action_id=str(uuid.uuid4()),
        session_id=session_id,
        scene_id=session.current_scene_id,
        actor_type="CHARACTER",
        character_id=scene_payload["active_character"]["id"],
        action_text=dialogue_text,
        audio_url=tts_result.get("audio_url")
    ))

    # 6. Build clue list
    story = story_loader.get_story(session.story_id)
    all_clues = []
    for cid in session.discovered_clues:
        c_raw = story["clues"].get(cid, {})
        all_clues.append(ClueSummary(
            id=cid,
            title=c_raw.get("title", cid),
            description=c_raw.get("description", ""),
            thumbnail=c_raw.get("thumbnail", ""),
            discovered=True
        ))

    unlocked_summary = None
    if newly_unlocked_clue:
        unlocked_summary = ClueSummary(**newly_unlocked_clue)

    ending_info = scene_payload.get("ending")

    return SessionStateResponse(
        session_id=session.session_id,
        story_id=session.story_id,
        previous_scene_id=previous_scene_id,
        current_scene=SceneResponse(
            scene_id=scene_payload["scene_id"],
            title=scene_payload["title"],
            background_image=scene_payload["background_image"],
            active_character=ActiveCharacterInfo(**scene_payload["active_character"]),
            dialogue=dialogue_text,
            audio_url=tts_result.get("audio_url"),
            suggested_actions=scene_payload.get("suggested_actions", []),
            audio_status=tts_result.get("status", "READY")
        ),
        discovered_clues=all_clues,
        newly_unlocked_clue=unlocked_summary,
        is_completed=is_completed,
        ending_id=session.ending_id,
        ending_title=ending_info.get("title") if ending_info else None,
        ending_epilogue=ending_info.get("epilogue") if ending_info else None,
        ending_image=ending_info.get("image_url") if ending_info else None,
        status=session.status
    )
