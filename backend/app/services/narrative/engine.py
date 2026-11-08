import re
from typing import Dict, Any, Optional, Tuple, List
from app.models.domain import StorySession
from app.services.narrative.loader import story_loader

class NarrativeEngine:
    def evaluate_action(
        self,
        session: StorySession,
        action_text: str
    ) -> Tuple[StorySession, Dict[str, Any], Optional[Dict[str, Any]], bool]:
        """
        Evaluates a player's action against the deterministic story graph.
        Returns:
            (updated_session, next_scene_payload, newly_unlocked_clue, is_completed)
        """
        story = story_loader.get_story(session.story_id)
        if not story:
            raise ValueError(f"Story not found: {session.story_id}")

        current_scene_id = session.current_scene_id
        scene_data = story["scenes"].get(current_scene_id)
        if not scene_data:
            raise ValueError(f"Scene not found: {current_scene_id}")

        tokens = set(re.findall(r"\w+", action_text.lower()))
        valid_transitions = scene_data.get("valid_transitions", {})

        matched_transition = None
        for trans_key, trans_def in valid_transitions.items():
            keywords = trans_def.get("keywords", [])
            # If any keyword matches the user action
            if any(k.lower() in tokens or k.lower() in action_text.lower() for k in keywords):
                # Verify required clues
                required_clues = trans_def.get("required_clues", [])
                if all(rc in session.discovered_clues for rc in required_clues):
                    matched_transition = trans_def
                    break

        newly_unlocked_clue = None
        is_completed = False
        ending_id = None
        ending_data = None

        if matched_transition:
            target_scene_id = matched_transition.get("target_scene_id", current_scene_id)
            response_dialogue = matched_transition.get("response_dialogue")
            unlocks_clue_id = matched_transition.get("unlocks_clue")
            ending_trigger = matched_transition.get("ending_trigger")

            # Unlock clue if present and not already found
            if unlocks_clue_id and unlocks_clue_id not in session.discovered_clues:
                session.discovered_clues.append(unlocks_clue_id)
                clue_raw = story["clues"].get(unlocks_clue_id, {})
                newly_unlocked_clue = {
                    "id": unlocks_clue_id,
                    "title": clue_raw.get("title", "New Clue"),
                    "description": clue_raw.get("description", ""),
                    "thumbnail": clue_raw.get("thumbnail", ""),
                    "discovered": True
                }

            # Handle ending
            if ending_trigger:
                is_completed = True
                ending_id = ending_trigger
                session.ending_id = ending_id
                session.status = "COMPLETED"
                ending_data = story["endings"].get(ending_trigger)

            # Transition scene
            session.current_scene_id = target_scene_id
            target_scene = story["scenes"].get(target_scene_id)
            active_char_id = target_scene.get("active_character_id", "narrator")
            char_raw = story["characters"].get(active_char_id, {})

            scene_payload = {
                "scene_id": target_scene_id,
                "title": target_scene.get("title", ""),
                "background_image": target_scene.get("background_image", ""),
                "active_character": {
                    "id": active_char_id,
                    "name": char_raw.get("name", "Narrator"),
                    "avatar_url": char_raw.get("avatar_url", ""),
                },
                "dialogue": response_dialogue or target_scene.get("dialogue", ""),
                "suggested_actions": target_scene.get("suggested_actions", []),
                "voice_id": char_raw.get("voice_id", "Nalini"),
                "ending": ending_data
            }
        else:
            # In-character graceful redirection
            active_char_id = scene_data.get("active_character_id", "narrator")
            char_raw = story["characters"].get(active_char_id, {})
            redirect_msg = f"{char_raw.get('name', 'The character')} pauses, listening closely. '{action_text}' doesn't seem to help right now. Focus on what is directly before us."

            scene_payload = {
                "scene_id": current_scene_id,
                "title": scene_data.get("title", ""),
                "background_image": scene_data.get("background_image", ""),
                "active_character": {
                    "id": active_char_id,
                    "name": char_raw.get("name", "Narrator"),
                    "avatar_url": char_raw.get("avatar_url", ""),
                },
                "dialogue": redirect_msg,
                "suggested_actions": scene_data.get("suggested_actions", []),
                "voice_id": char_raw.get("voice_id", "Nalini"),
                "ending": None
            }

        return session, scene_payload, newly_unlocked_clue, is_completed

narrative_engine = NarrativeEngine()
