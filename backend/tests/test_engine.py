import pytest
from app.models.domain import StorySession
from app.services.narrative.loader import story_loader
from app.services.narrative.engine import narrative_engine

def test_story_loader_all_domains():
    stories = story_loader.stories
    expected_domains = ["mystery", "thriller", "adventure", "comedy", "sci_fi"]
    for domain in expected_domains:
        assert domain in stories, f"Expected domain '{domain}' not found in story loader"
        story = stories[domain]
        assert "meta" in story
        assert "scenes" in story
        assert "characters" in story
        assert "clues" in story
        assert "endings" in story
        assert len(story["scenes"]) >= 2
        assert len(story["endings"]) >= 2

def test_mystery_narrative_flow():
    # 1. Create a simulated mystery session
    session = StorySession(
        session_id="test-session-001",
        story_id="mystery",
        current_scene_id="scene_cliffside",
        discovered_clues=["clue_tomorrow_letter"]
    )

    # 2. Examine postmark -> should unlock clue_weather_telegram
    session, payload, clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text="Examine the tomorrow postmark on the letter"
    )
    assert session.current_scene_id == "scene_cliffside"
    assert "clue_weather_telegram" in session.discovered_clues
    assert not is_completed

    # 3. Enter vault -> transitions to scene_archive_vault, unlocks clue_brass_vault_key
    session, payload, clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text="Follow Dev toward the hidden lighthouse vault"
    )
    assert session.current_scene_id == "scene_archive_vault"
    assert "clue_brass_vault_key" in session.discovered_clues

    # 4. Inspect reading desk -> transitions to scene_reading_desk
    session, payload, clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text="Use the brass key on the reading desk drawer"
    )
    assert session.current_scene_id == "scene_reading_desk"

    # 5. Rush to shore -> transitions to scene_shoreline_dawn
    session, payload, clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text="Rush down to the shore with Dev and Mira"
    )
    assert session.current_scene_id == "scene_shoreline_dawn"
    assert not is_completed

    # 6. Choose truth ending -> triggers end_final_delivery
    session, payload, clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text="Break the purple seal and read tomorrow's truth"
    )
    assert is_completed
    assert session.ending_id == "end_final_delivery"
    assert payload["ending"] is not None

def test_invalid_action_graceful_handling():
    session = StorySession(
        session_id="test-session-002",
        story_id="mystery",
        current_scene_id="scene_cliffside",
        discovered_clues=["clue_tomorrow_letter"]
    )
    original_scene = session.current_scene_id
    original_clue_count = len(session.discovered_clues)

    # Gibberish input
    session, payload, clue, is_completed = narrative_engine.evaluate_action(
        session=session,
        action_text="fly to mars on a skateboard and eat pizza"
    )

    # State must not be corrupted
    assert session.current_scene_id == original_scene
    assert len(session.discovered_clues) == original_clue_count
    assert not is_completed
    assert "doesn't seem to help" in payload["dialogue"]

