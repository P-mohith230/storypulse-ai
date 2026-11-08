import sqlite3
import os
from contextlib import contextmanager
from typing import Generator
from app.core.config import settings

DB_FILE = os.path.abspath(settings.DATABASE_URL.replace("sqlite:///", ""))

def get_db_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            device_id TEXT UNIQUE,
            preferred_lang TEXT DEFAULT 'en-IN',
            audio_mode TEXT DEFAULT 'auto_tts',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS story_sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT,
            story_id TEXT NOT NULL,
            current_scene_id TEXT NOT NULL,
            status TEXT DEFAULT 'ACTIVE',
            duration_target INTEGER DEFAULT 5,
            mood_selected TEXT DEFAULT 'Curious',
            ending_id TEXT,
            discovered_clues_json TEXT DEFAULT '[]',
            character_memory_json TEXT DEFAULT '{}',
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS session_actions (
            action_id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            scene_id TEXT NOT NULL,
            actor_type TEXT NOT NULL,
            character_id TEXT,
            action_text TEXT NOT NULL,
            input_modality TEXT DEFAULT 'TEXT',
            audio_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES story_sessions(session_id)
        );

        CREATE TABLE IF NOT EXISTS session_clues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            clue_id TEXT NOT NULL,
            discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES story_sessions(session_id)
        );

        CREATE INDEX IF NOT EXISTS idx_sessions_user ON story_sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_story ON story_sessions(story_id);
        CREATE INDEX IF NOT EXISTS idx_actions_session ON session_actions(session_id);
        """)

