import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "app", "static", "images"))

def create_gradient_scene(filename, color_top, color_bottom, title, subtitle, icon="📖"):
    width, height = 800, 1000
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)

    # Vertical gradient
    for y in range(height):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * (y / height))
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * (y / height))
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Add atmospheric radial vignette
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([-100, -100, width + 100, height + 100], fill=(255, 255, 255, 20))
    overlay = overlay.filter(ImageFilter.GaussianBlur(80))
    img = Image.alpha_composite(img, overlay)

    # Frame border
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, width - 20, height - 20], outline=(255, 255, 255, 40), width=2)
    draw.rectangle([26, 26, width - 26, height - 26], outline=(255, 255, 255, 20), width=1)

    # Title & Subtitle box
    box_top = height - 260
    draw.rectangle([30, box_top, width - 30, height - 30], fill=(10, 13, 20, 210))
    draw.rectangle([30, box_top, width - 30, height - 30], outline=(139, 92, 246, 120), width=2)

    # Text
    draw.text((width // 2, box_top + 50), title.upper(), fill=(248, 250, 252), anchor="mm")
    draw.text((width // 2, box_top + 100), subtitle, fill=(148, 163, 184), anchor="mm")
    draw.text((width // 2, box_top + 150), "STORYPULSE CINEMATIC FICTION", fill=(167, 139, 250), anchor="mm")

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.convert("RGB").save(filename, "PNG")
    print(f"Saved: {filename}")

def create_clue_badge(filename, color_main, title, lore, symbol="🔍"):
    size = 400
    img = Image.new("RGBA", (size, size), (18, 23, 34, 255))
    draw = ImageDraw.Draw(img)

    # Background gradient
    for y in range(size):
        ratio = y / size
        r = int(18 + (color_main[0] - 18) * 0.3 * ratio)
        g = int(23 + (color_main[1] - 23) * 0.3 * ratio)
        b = int(34 + (color_main[2] - 34) * 0.3 * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Inner circular medallion
    draw.ellipse([40, 40, size - 40, size - 40], outline=color_main, width=4)
    draw.ellipse([50, 50, size - 50, size - 50], outline=(255, 255, 255, 40), width=2)

    # Text label
    draw.text((size // 2, size - 80), title.upper(), fill=(248, 250, 252), anchor="mm")
    draw.text((size // 2, size - 50), "DISCOVERED EVIDENCE", fill=(16, 185, 129), anchor="mm")

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.convert("RGB").save(filename, "PNG")
    print(f"Saved Clue: {filename}")

# Generate Scenes
create_gradient_scene(
    os.path.join(STATIC_DIR, "scenes", "scene_reading_desk.png"),
    color_top=(30, 20, 50),
    color_bottom=(16, 27, 44),
    title="The Reading Desk of Secrets",
    subtitle="Drawer 7 Unlocked • Salt Air and Faded Ledger Ink",
    icon="🗝️"
)

create_gradient_scene(
    os.path.join(STATIC_DIR, "scenes", "scene_shoreline_dawn.png"),
    color_top=(15, 23, 42),
    color_bottom=(90, 40, 70),
    title="The Shoreline of Dawn",
    subtitle="Mist Over the Sea Pier • Breaking Tomorrow's Seal",
    icon="🌊"
)

# Generate Clues
create_clue_badge(
    os.path.join(STATIC_DIR, "clues", "clue_archivist_log.png"),
    color_main=(245, 158, 11),
    title="The Archivist's Logbook",
    lore="Tracking memories confiscated from town residents"
)

create_clue_badge(
    os.path.join(STATIC_DIR, "clues", "clue_silver_locket.png"),
    color_main=(148, 163, 184),
    title="The Blank Paper Locket",
    lore="Tarnished silver pendant with glowing hidden script"
)

create_clue_badge(
    os.path.join(STATIC_DIR, "clues", "clue_weather_telegram.png"),
    color_main=(6, 182, 212),
    title="Meteorological Telegram",
    lore="Faded telegram warning of temporal tide fluctuations"
)

# Generate Endings
create_gradient_scene(
    os.path.join(STATIC_DIR, "endings", "end_archivist_secret.png"),
    color_top=(16, 16, 38),
    color_bottom=(88, 28, 135),
    title="Ending 1: The Keeper of Sorrows",
    subtitle="The Archive Remains Silent Beneath the Waves",
    icon="🛡️"
)

create_gradient_scene(
    os.path.join(STATIC_DIR, "endings", "end_final_delivery.png"),
    color_top=(67, 20, 7),
    color_bottom=(245, 158, 11),
    title="Ending 2: Tomorrow's Truth",
    subtitle="The Seal Broken • Lost Memories Restored at Dawn",
    icon="✨"
)

create_gradient_scene(
    os.path.join(STATIC_DIR, "endings", "end_memory_erased.png"),
    color_top=(15, 23, 42),
    color_bottom=(30, 41, 59),
    title="Ending 3: The Tide Takes All",
    subtitle="The Ocean Claims Tomorrow • Solitary Serenity",
    icon="🌊"
)
print("All visual assets completed successfully!")
