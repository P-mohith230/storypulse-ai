from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db

init_db()
client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "gnani_stt_status" in data
    assert "gnani_tts_status" in data

def test_stories_catalog_endpoint():
    response = client.get("/api/v1/stories")
    assert response.status_code == 200
    stories = response.json()
    assert len(stories) == 5
    domains = [s["domain"] for s in stories]
    assert "mystery" in domains
    assert "thriller" in domains
    assert "adventure" in domains
    assert "comedy" in domains
    assert "sci_fi" in domains

def test_session_lifecycle():
    # 1. Create a session
    resp = client.post(
        "/api/v1/sessions",
        json={
            "story_id": "mystery",
            "duration_target": 10,
            "mood_selected": "Curious",
            "preferred_lang": "en-IN"
        }
    )
    assert resp.status_code == 201
    session_data = resp.json()
    session_id = session_data["session_id"]
    assert session_id is not None
    assert session_data["current_scene"]["scene_id"] == "scene_cliffside"
    assert len(session_data["discovered_clues"]) >= 1

    # 2. Perform an action
    action_resp = client.post(
        f"/api/v1/sessions/{session_id}/action",
        json={
            "action_text": "Examine the tomorrow postmark",
            "input_modality": "TEXT"
        }
    )
    assert action_resp.status_code == 200
    action_data = action_resp.json()
    assert action_data["session_id"] == session_id
    assert action_data["newly_unlocked_clue"] is not None
    assert action_data["newly_unlocked_clue"]["id"] == "clue_weather_telegram"
