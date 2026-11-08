import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.core.database import get_db
from app.models.domain import StorySession, SessionAction

class SessionRepository:
    def create_session(self, session: StorySession) -> StorySession:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO story_sessions (
                    session_id, user_id, story_id, current_scene_id,
                    status, duration_target, mood_selected, ending_id,
                    discovered_clues_json, character_memory_json,
                    started_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session.session_id,
                    session.user_id,
                    session.story_id,
                    session.current_scene_id,
                    session.status,
                    session.duration_target,
                    session.mood_selected,
                    session.ending_id,
                    json.dumps(session.discovered_clues),
                    json.dumps(session.character_memory),
                    session.started_at.isoformat(),
                    session.updated_at.isoformat(),
                ),
            )
            return session

    def get_session(self, session_id: str) -> Optional[StorySession]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM story_sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return StorySession(
                session_id=row["session_id"],
                user_id=row["user_id"],
                story_id=row["story_id"],
                current_scene_id=row["current_scene_id"],
                status=row["status"],
                duration_target=row["duration_target"],
                mood_selected=row["mood_selected"],
                ending_id=row["ending_id"],
                discovered_clues=json.loads(row["discovered_clues_json"] or "[]"),
                character_memory=json.loads(row["character_memory_json"] or "{}"),
                started_at=datetime.fromisoformat(row["started_at"]) if row["started_at"] else datetime.utcnow(),
                updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else datetime.utcnow(),
                completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
            )

    def update_session(self, session: StorySession) -> StorySession:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE story_sessions SET
                    current_scene_id = ?,
                    status = ?,
                    ending_id = ?,
                    discovered_clues_json = ?,
                    character_memory_json = ?,
                    updated_at = ?,
                    completed_at = ?
                WHERE session_id = ?
                """,
                (
                    session.current_scene_id,
                    session.status,
                    session.ending_id,
                    json.dumps(session.discovered_clues),
                    json.dumps(session.character_memory),
                    datetime.utcnow().isoformat(),
                    session.completed_at.isoformat() if session.completed_at else None,
                    session.session_id,
                ),
            )
            return session

    def log_action(self, action: SessionAction) -> SessionAction:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO session_actions (
                    action_id, session_id, scene_id, actor_type,
                    character_id, action_text, input_modality, audio_url, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    action.action_id,
                    action.session_id,
                    action.scene_id,
                    action.actor_type,
                    action.character_id,
                    action.action_text,
                    action.input_modality,
                    action.audio_url,
                    action.created_at.isoformat(),
                ),
            )
            return action

    def count_active_sessions(self) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM story_sessions WHERE status = 'ACTIVE'")
            row = cursor.fetchone()
            return row["cnt"] if row else 0

session_repo = SessionRepository()

