import os
import json
from typing import Dict, Any, List

class StoryDataLoader:
    _instance = None

    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "story_data"))
        self.stories: Dict[str, Dict[str, Any]] = {}
        self.load_all_stories()

    def load_all_stories(self):
        if not os.path.exists(self.base_dir):
            return

        for domain in os.listdir(self.base_dir):
            domain_path = os.path.join(self.base_dir, domain)
            if not os.path.isdir(domain_path):
                continue

            try:
                story_file = os.path.join(domain_path, "story.json")
                scenes_file = os.path.join(domain_path, "scenes.json")
                chars_file = os.path.join(domain_path, "characters.json")
                clues_file = os.path.join(domain_path, "clues.json")
                endings_file = os.path.join(domain_path, "endings.json")

                if not (os.path.exists(story_file) and os.path.exists(scenes_file)):
                    continue

                with open(story_file, "r", encoding="utf-8") as f:
                    story_meta = json.load(f)
                with open(scenes_file, "r", encoding="utf-8") as f:
                    scenes = json.load(f)
                with open(chars_file, "r", encoding="utf-8") as f:
                    characters = json.load(f)
                with open(clues_file, "r", encoding="utf-8") as f:
                    clues = json.load(f)
                with open(endings_file, "r", encoding="utf-8") as f:
                    endings = json.load(f)

                story_id = story_meta.get("id", domain)
                self.stories[story_id] = {
                    "meta": story_meta,
                    "scenes": scenes,
                    "characters": characters,
                    "clues": clues,
                    "endings": endings,
                }
            except Exception as e:
                print(f"[StoryDataLoader] Error loading {domain}: {e}")

    def get_story(self, story_id: str) -> Dict[str, Any]:
        return self.stories.get(story_id)

    def get_catalog(self, duration_filter: int = None, mood_filter: str = None) -> List[Dict[str, Any]]:
        results = []
        for sid, story in self.stories.items():
            meta = story["meta"]
            if duration_filter and meta.get("duration_min") != duration_filter:
                pass  # Keep in catalog or prioritize
            if mood_filter and mood_filter not in meta.get("moods", []):
                pass
            results.append({
                "id": meta.get("id"),
                "title": meta.get("title"),
                "domain": meta.get("domain"),
                "tagline": meta.get("tagline"),
                "duration_min": meta.get("duration_min", 5),
                "moods": meta.get("moods", []),
                "cover_image": meta.get("cover_image"),
                "character_count": len(story.get("characters", {})),
                "scene_count": len(story.get("scenes", {})),
                "clue_count": len(story.get("clues", {})),
                "featured": meta.get("featured", False),
            })
        return results

story_loader = StoryDataLoader()

