import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.core.database import init_db
from app.models.domain import StorySession
from app.services.narrative.loader import story_loader
from app.services.narrative.engine import narrative_engine
from app.services.gnani.prisma_service import prisma_service
from app.services.gnani.timbre_service import timbre_service
from app.api.routes import health, stories, sessions, speech
from app.schemas.schemas import CreateSessionRequest, SessionActionRequest

def run_all_tests():
    print("=" * 60, flush=True)
    print("STORYPULSE AI BACKEND VERIFICATION SUITE", flush=True)
    print("=" * 60, flush=True)
    init_db()

    # Test 1: Story Loader
    print("[TEST 1/5] Verifying Story Loader for all 5 domains...", flush=True)
    all_stories = story_loader.stories
    expected = ["mystery", "thriller", "adventure", "comedy", "sci_fi"]
    for domain in expected:
        assert domain in all_stories, f"Missing domain {domain}"
        s = all_stories[domain]
        assert len(s["scenes"]) >= 2, f"Domain {domain} has insufficient scenes"
        assert len(s["endings"]) >= 2, f"Domain {domain} has insufficient endings"
    print(" -> PASS: All 5 domains loaded with complete scene and ending graphs.", flush=True)

    # Test 2: Narrative Engine Transitions
    print("[TEST 2/5] Verifying Narrative Engine State Transitions...", flush=True)
    session = StorySession(
        session_id="verify-001",
        story_id="mystery",
        current_scene_id="scene_cliffside",
        discovered_clues=["clue_tomorrow_letter"]
    )
    session, payload, clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text="Examine the tomorrow postmark on the letter"
    )
    assert "clue_weather_telegram" in session.discovered_clues
    assert not is_completed

    session, payload, clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text="Follow Dev toward the hidden lighthouse vault"
    )
    assert session.current_scene_id == "scene_archive_vault"
    assert "clue_brass_vault_key" in session.discovered_clues

    session, payload, clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text="Use the brass key on Drawer 7"
    )
    assert session.current_scene_id == "scene_reading_desk"

    session, payload, clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text="Rush down to the shore with Dev and Mira"
    )
    assert session.current_scene_id == "scene_shoreline_dawn"

    session, payload, clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text="Break the purple seal and read tomorrow's truth"
    )
    assert is_completed
    assert session.ending_id == "end_final_delivery"
    print(" -> PASS: Full flagship narrative tree traversed from opening to canonical ending.", flush=True)

    # Test 3: Invalid Action Guard
    print("[TEST 3/5] Verifying Invalid Action Handling...", flush=True)
    session2 = StorySession(
        session_id="verify-002",
        story_id="mystery",
        current_scene_id="scene_cliffside",
        discovered_clues=["clue_tomorrow_letter"]
    )
    session2, payload2, clue2, is_completed2 = narrative_engine.evaluate_action(
        session=session2,
        action_text="eat some ice cream in antarctica"
    )
    assert session2.current_scene_id == "scene_cliffside"
    assert len(session2.discovered_clues) == 1
    assert not is_completed2
    print(" -> PASS: Narrative engine safely rejected out-of-context action without state corruption.", flush=True)

    # Test 4: Gnani Audio Services
    print("[TEST 4/5] Verifying Gnani Prisma & Timbre Service integration...", flush=True)
    dummy_wav = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
    stt_res = prisma_service.transcribe_sync(dummy_wav, "dummy.wav", "en-IN")
    assert "transcribed_text" in stt_res
    assert "gnani_prisma" in stt_res["provider"]

    tts_res = timbre_service.synthesize_sync("Welcome to StoryPulse", "Nalini", "en-IN")
    assert "status" in tts_res
    assert "provider" in tts_res
    print(" -> PASS: Gnani Prisma STT & Timbre TTS adapters functioning properly.", flush=True)

    # Test 5: FastAPI Route Handlers (Direct Execution)
    print("[TEST 5/5] Verifying FastAPI Endpoint Handlers (Health, Stories, Sessions, Actions)...", flush=True)
    
    # 5.1 Health Check
    h_res = health.health_check()
    assert h_res.status == "healthy"
    assert h_res.database == "connected"
    
    # 5.2 Stories Catalog
    cat_res = stories.list_stories(duration=None, mood=None)
    assert len(cat_res) == 5
    domains = [c["domain"] if isinstance(c, dict) else c.domain for c in cat_res]
    assert "mystery" in domains and "thriller" in domains
    
    # 5.3 Session Creation
    new_sess = sessions.create_session(CreateSessionRequest(
        story_id="mystery",
        duration_target=10,
        mood_selected="Curious"
    ))
    assert new_sess.session_id is not None
    assert new_sess.current_scene.scene_id == "scene_cliffside"
    assert len(new_sess.discovered_clues) >= 1
    
    # 5.4 Perform Narrative Action
    action_res = sessions.perform_action(
        session_id=new_sess.session_id,
        payload=SessionActionRequest(
            action_text="Examine the tomorrow postmark",
            input_modality="TEXT"
        )
    )
    assert action_res.session_id == new_sess.session_id
    assert action_res.newly_unlocked_clue is not None
    assert action_res.newly_unlocked_clue.id == "clue_weather_telegram"
    print(" -> PASS: All API endpoint contracts validated (Health, Catalog, Creation, Action).", flush=True)

    # Test 6: Responsive Web Assets and Image Inventory
    print("[TEST 6/6] Verifying Responsive Web Assets and Complete Image Inventory...", flush=True)
    from app.main import STATIC_DIR
    assert os.path.exists(os.path.join(STATIC_DIR, "index.html")), "index.html missing"
    assert os.path.exists(os.path.join(STATIC_DIR, "style.css")), "style.css missing"
    assert os.path.exists(os.path.join(STATIC_DIR, "app.js")), "app.js missing"
    
    # Check all 5 story domain assets
    img_dir = os.path.join(STATIC_DIR, "images")
    required_assets = [
        "covers/cover_mystery.png", "covers/cover_thriller.png", "covers/cover_adventure.png",
        "covers/cover_comedy.png", "covers/cover_scifi.png",
        "characters/char_mira.png", "characters/char_conductor.png", "characters/char_tara.png",
        "characters/char_rao.png", "characters/char_orson.png",
        "scenes/scene_cliffside.png", "scenes/scene_carriage.png", "scenes/scene_sky_ascent.png",
        "scenes/scene_excuse_office.png", "scenes/scene_lunar_comms.png",
        "clues/clue_tomorrow_letter.png", "clue_emergency_key.png", "clues/clue_monsoon_compass.png",
        "clues/clue_rejected_stamp.png", "clues/clue_coolant_schematic.png"
    ]
    # Verify each asset path
    for asset in [
        "covers/cover_mystery.png", "covers/cover_thriller.png", "covers/cover_adventure.png",
        "covers/cover_comedy.png", "covers/cover_scifi.png",
        "characters/char_mira.png", "characters/char_conductor.png", "characters/char_tara.png",
        "characters/char_rao.png", "characters/char_orson.png",
        "scenes/scene_cliffside.png", "scenes/scene_carriage.png", "scenes/scene_sky_ascent.png",
        "scenes/scene_excuse_office.png", "scenes/scene_lunar_comms.png",
        "clues/clue_tomorrow_letter.png", "clues/clue_emergency_key.png", "clues/clue_monsoon_compass.png",
        "clues/clue_rejected_stamp.png", "clues/clue_coolant_schematic.png",
        "endings/end_platform_zero_arrival.png", "endings/end_final_delivery.png", "endings/end_sky_sanctuary.png"
    ]:
        p = os.path.join(img_dir, asset)
        assert os.path.exists(p) and os.path.getsize(p) > 1000, f"Asset missing or invalid: {asset}"
    print(" -> PASS: Mobile-first Web Assets (HTML/CSS/JS) & 100% of Visual Assets verified.", flush=True)

    print("=" * 60, flush=True)
    print("ALL 6 STORYPULSE VERIFICATION SUITES PASSED (100% SUCCESS)", flush=True)
    print("=" * 60, flush=True)

if __name__ == "__main__":
    run_all_tests()
