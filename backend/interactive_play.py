#!/usr/bin/env python3
"""
StoryPulse AI — Interactive Terminal Playthrough Demonstration
Allows judges and evaluators to play the complete interactive story
with real-time state transitions, clue discovery, and character voice simulation.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.core.database import init_db
from app.services.narrative.loader import story_loader
from app.services.narrative.engine import narrative_engine
from app.api.routes import sessions
from app.schemas.schemas import CreateSessionRequest, SessionActionRequest

# ANSI Color Codes for terminal styling
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    UNDERLINE = "\033[4m"

def print_banner():
    print(f"\n{C.PURPLE}{C.BOLD}" + "=" * 68)
    print("          STORYPULSE AI — CONVERSATIONAL STORY EXPERIENCE          ")
    print("                Your moments. Your mood. Your story.                ")
    print("=" * 68 + f"{C.RESET}\n")

def run_cli_session(story_id="mystery"):
    init_db()
    story = story_loader.get_story(story_id)
    if not story:
        print(f"Error: Story {story_id} not found.")
        return

    meta = story["meta"]
    print(f"{C.CYAN}{C.BOLD}TITLE:{C.RESET} {meta['title']}")
    print(f"{C.YELLOW}DOMAIN:{C.RESET} {meta['domain'].upper()} | {C.YELLOW}DURATION:{C.RESET} {meta['duration_min']} mins")
    print(f"{C.DARKCYAN}PREMISE:{C.RESET} {meta['tagline']}\n")
    print(f"{C.GREEN}[Starting new interactive session via Narrative Engine...]{C.RESET}\n")

    # Create session via API route handler
    req = CreateSessionRequest(story_id=story_id, duration_target=10, mood_selected="Curious")
    session_state = sessions.create_session(req)
    session_id = session_state.session_id

    turn = 1
    while not session_state.is_completed:
        scene = session_state.current_scene
        char = scene.active_character

        print(f"{C.PURPLE}━━━ [SCENE {turn}]: {scene.title.upper()} ━━━{C.RESET}")
        print(f"{C.BLUE}{C.BOLD}🗣️  {char.name}:{C.RESET}")
        print(f"   \"{scene.dialogue}\"\n")

        # Discovered Clues
        if session_state.discovered_clues:
            print(f"{C.YELLOW}🔍 CASE CLUES ON FILE ({len(session_state.discovered_clues)}):{C.RESET}")
            for c in session_state.discovered_clues:
                print(f"   • {c.title}: {c.description}")
            print()

        # Newly unlocked clue banner
        if session_state.newly_unlocked_clue:
            print(f"{C.GREEN}{C.BOLD}✨ NEW CLUE DISCOVERED: {session_state.newly_unlocked_clue.title}{C.RESET}\n")

        print(f"{C.CYAN}{C.BOLD}SUGGESTED NARRATIVE ACTIONS:{C.RESET}")
        for idx, act in enumerate(scene.suggested_actions, 1):
            print(f"  [{idx}] \"{act}\"")
        print(f"  [Q] Exit Playthrough\n")

        choice = input(f"{C.BOLD}Enter choice number or type your custom action: {C.RESET}").strip()
        if choice.lower() in ["q", "quit", "exit"]:
            print(f"\n{C.YELLOW}Session saved. Exiting playthrough.{C.RESET}\n")
            return

        # Determine action text
        action_text = choice
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(scene.suggested_actions):
                action_text = scene.suggested_actions[idx]

        print(f"\n{C.DARKCYAN}>>> Action: \"{action_text}\"{C.RESET}")
        print(f"{C.PURPLE}[Evaluating deterministic transitions & synthesizing voice...]{C.RESET}\n")
        time.sleep(0.4)

        # Dispatch action
        action_req = SessionActionRequest(action_text=action_text, input_modality="TEXT")
        session_state = sessions.perform_action(session_id, action_req)
        turn += 1

    # Story Completed
    print(f"\n{C.GREEN}{C.BOLD}" + "=" * 68)
    print("                     🎉 CHAPTER CONCLUDED! 🎉                      ")
    print("=" * 68 + f"{C.RESET}\n")
    print(f"{C.PURPLE}{C.BOLD}ENDING REACHED:{C.RESET} {session_state.ending_title}")
    print(f"\n{C.CYAN}{C.BOLD}EPILOGUE:{C.RESET}\n{session_state.ending_epilogue}\n")
    print(f"{C.YELLOW}TOTAL CLUES DISCOVERED:{C.RESET} {len(session_state.discovered_clues)}")
    print(f"{C.GREEN}Story successfully verified end-to-end!{C.RESET}\n")

if __name__ == "__main__":
    print_banner()
    run_cli_session("mystery")
