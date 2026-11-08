import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

STATIC_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "app", "static", "images"))
MOBILE_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mobile", "assets", "images"))

def save_to_both(img, rel_path):
    for base in [STATIC_BASE, MOBILE_BASE]:
        full_path = os.path.join(base, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        img.convert("RGB").save(full_path, "PNG", optimize=True)
    print(f"[OK] Generated: {rel_path}")

def make_gradient(width, height, c1, c2, vertical=True):
    base = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(base)
    steps = height if vertical else width
    for i in range(steps):
        t = i / float(steps)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        if vertical:
            draw.line([(0, i), (width, i)], fill=(r, g, b, 255))
        else:
            draw.line([(i, 0), (i, height)], fill=(r, g, b, 255))
    return base

def draw_vignette(img, intensity=120):
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rectangle([0, 0, w, h], fill=(0, 0, 0, intensity))
    mask = Image.new("L", (w, h), 255)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([int(w * 0.1), int(h * 0.1), int(w * 0.9), int(h * 0.9)], fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(int(min(w, h) * 0.2)))
    overlay.putalpha(mask)
    return Image.alpha_composite(img, overlay)

# ----------------- SCENE GENERATOR -----------------
def generate_cinematic_scene(rel_path, c_top, c_bottom, title, subtitle, theme_acc, draw_elements_fn):
    w, h = 900, 1200
    canvas = make_gradient(w, h, c_top, c_bottom)
    
    # Custom vector art elements for each scene
    canvas = draw_elements_fn(canvas)
    
    # Atmospheric vignette
    canvas = draw_vignette(canvas, 140)
    
    # Cinematic lower text card
    draw = ImageDraw.Draw(canvas)
    
    # Subtitle / title glassmorphism lower banner
    card_h = 240
    card_y = h - card_h - 40
    card = Image.new("RGBA", (w - 80, card_h), (10, 14, 26, 215))
    cdraw = ImageDraw.Draw(card)
    cdraw.rectangle([0, 0, w - 80, card_h], outline=theme_acc, width=2)
    cdraw.line([(30, 2), (w - 110, 2)], fill=(255, 255, 255, 120), width=1)
    
    # Text in card
    cdraw.text(((w - 80) // 2, 50), title.upper(), fill=(255, 255, 255), anchor="mm")
    cdraw.text(((w - 80) // 2, 105), subtitle, fill=(180, 195, 215), anchor="mm")
    cdraw.text(((w - 80) // 2, 160), "STORYPULSE CINEMATIC FICTION • GNANI AI", fill=theme_acc, anchor="mm")
    
    canvas.alpha_composite(card, (40, card_y))
    save_to_both(canvas, rel_path)

# ----------------- CHARACTER GENERATOR -----------------
def generate_character_portrait(rel_path, bg_color, rim_color, char_name, role_title, symbol, draw_char_fn):
    size = 600
    canvas = Image.new("RGBA", (size, size), bg_color)
    
    # Radial background aura
    aura = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    adraw = ImageDraw.Draw(aura)
    adraw.ellipse([100, 100, 500, 500], fill=(*rim_color[:3], 45))
    aura = aura.filter(ImageFilter.GaussianBlur(60))
    canvas = Image.alpha_composite(canvas, aura)
    
    # Custom character silhouettes/features
    canvas = draw_char_fn(canvas, rim_color)
    
    # Outer circular frame & rings
    draw = ImageDraw.Draw(canvas)
    draw.ellipse([20, 20, size - 20, size - 20], outline=rim_color, width=4)
    draw.ellipse([30, 30, size - 30, size - 30], outline=(255, 255, 255, 40), width=2)
    
    # Character name badge
    badge_w, badge_h = 440, 90
    badge_y = size - 110
    badge = Image.new("RGBA", (badge_w, badge_h), (12, 16, 28, 230))
    bdraw = ImageDraw.Draw(badge)
    bdraw.rectangle([0, 0, badge_w, badge_h], outline=rim_color, width=2)
    bdraw.text((badge_w // 2, 28), char_name.upper(), fill=(255, 255, 255), anchor="mm")
    bdraw.text((badge_w // 2, 60), role_title, fill=rim_color, anchor="mm")
    
    canvas.alpha_composite(badge, ((size - badge_w) // 2, badge_y))
    save_to_both(canvas, rel_path)

# ----------------- CLUE BADGE GENERATOR -----------------
def generate_clue_artifact(rel_path, bg_c, acc_c, title, category, draw_clue_fn):
    size = 500
    canvas = Image.new("RGBA", (size, size), bg_c)
    
    # Background texture & glow
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([80, 80, 420, 420], fill=(*acc_c[:3], 50))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    canvas = Image.alpha_composite(canvas, glow)
    
    # Draw clue illustration
    canvas = draw_clue_fn(canvas, acc_c)
    
    # Double ring frame
    draw = ImageDraw.Draw(canvas)
    draw.ellipse([25, 25, size - 25, size - 25], outline=acc_c, width=4)
    draw.ellipse([35, 35, size - 35, size - 35], outline=(255, 255, 255, 50), width=1)
    
    # Label plate
    plate_h = 90
    plate_y = size - 115
    plate = Image.new("RGBA", (400, plate_h), (10, 14, 24, 225))
    pdraw = ImageDraw.Draw(plate)
    pdraw.rectangle([0, 0, 400, plate_h], outline=acc_c, width=2)
    pdraw.text((200, 30), title.upper(), fill=(255, 255, 255), anchor="mm")
    pdraw.text((200, 62), category.upper(), fill=(16, 185, 129), anchor="mm")
    
    canvas.alpha_composite(plate, (50, plate_y))
    save_to_both(canvas, rel_path)

# ----------------- ENDING GENERATOR -----------------
def generate_ending_scene(rel_path, c_top, c_bottom, title, epilogue, acc_c, draw_end_fn):
    w, h = 900, 1100
    canvas = make_gradient(w, h, c_top, c_bottom)
    canvas = draw_end_fn(canvas, acc_c)
    canvas = draw_vignette(canvas, 130)
    
    draw = ImageDraw.Draw(canvas)
    card_h = 240
    card_y = h - card_h - 40
    card = Image.new("RGBA", (w - 80, card_h), (8, 12, 20, 220))
    cdraw = ImageDraw.Draw(card)
    cdraw.rectangle([0, 0, w - 80, card_h], outline=acc_c, width=3)
    cdraw.text(((w - 80) // 2, 45), "STORYPULSE CHAPTER ENDING", fill=acc_c, anchor="mm")
    cdraw.text(((w - 80) // 2, 95), title.upper(), fill=(255, 255, 255), anchor="mm")
    cdraw.text(((w - 80) // 2, 150), epilogue[:65], fill=(203, 213, 225), anchor="mm")
    cdraw.text(((w - 80) // 2, 185), epilogue[65:], fill=(203, 213, 225), anchor="mm")
    
    canvas.alpha_composite(card, (40, card_y))
    save_to_both(canvas, rel_path)

print("[INFO] Template generators loaded. Defining specific artwork...")

# ==============================================================================
# SPECIFIC ARTWORK IMPLEMENTATIONS
# ==============================================================================

# ----------------- 1. SCENES -----------------

# Scene: Midnight Carriage 104 (Thriller)
def draw_scene_carriage(canvas):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Train perspective vanishing lines
    vanish_x, vanish_y = w // 2, 420
    # Window panes with red neon reflection
    d.polygon([(60, 200), (w//2 - 40, 380), (w//2 - 40, 520), (60, 680)], fill=(30, 10, 15, 230), outline=(239, 68, 68, 150))
    d.polygon([(w - 60, 200), (w//2 + 40, 380), (w//2 + 40, 520), (w - 60, 680)], fill=(30, 10, 15, 230), outline=(239, 68, 68, 150))
    # Ceiling lights (red glow bars)
    for y in [120, 200, 280, 350]:
        cw = int((y / 400.0) * 160)
        d.line([(w//2 - cw, y), (w//2 + cw, y)], fill=(239, 68, 68, 220), width=4)
    # Floor tracks & emergency brake box glow
    d.line([(w//2, vanish_y), (80, h)], fill=(120, 20, 20, 200), width=3)
    d.line([(w//2, vanish_y), (w - 80, h)], fill=(120, 20, 20, 200), width=3)
    d.rectangle([w//2 - 40, 560, w//2 + 40, 640], fill=(185, 28, 28), outline=(255, 255, 255), width=2)
    d.text((w//2, 600), "BRAKE", fill=(255, 255, 255), anchor="mm")
    return canvas

# Scene: Department of Excuses (Comedy)
def draw_scene_excuse_office(canvas):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Stacks of parchment paper folders
    for i in range(12):
        bx = 80 + (i % 4) * 190
        by = 280 + (i // 4) * 160
        d.rectangle([bx, by, bx + 150, by + 120], fill=(234, 179, 8, 200), outline=(161, 98, 7), width=2)
        d.rectangle([bx + 15, by + 15, bx + 135, by + 105], fill=(254, 240, 138, 240))
        d.text((bx + 75, by + 60), "FILE #" + str(1024 + i * 37), fill=(133, 77, 14), anchor="mm")
    # Spinning ceiling fan
    cx, cy = w // 2, 160
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle + 25)
        ex = cx + int(140 * math.cos(rad))
        ey = cy + int(140 * math.sin(rad))
        d.line([(cx, cy), (ex, ey)], fill=(120, 70, 30), width=8)
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(90, 50, 20))
    return canvas

# Scene: Lunar Relay Station (Sci-Fi)
def draw_scene_lunar_comms(canvas):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Starfield
    random.seed(42)
    for _ in range(80):
        sx, sy = random.randint(20, w - 20), random.randint(20, 500)
        d.point((sx, sy), fill=(255, 255, 255, random.randint(100, 255)))
    # Earth crescent in sky
    d.ellipse([w - 240, 80, w - 80, 240], fill=(6, 182, 212))
    d.ellipse([w - 210, 60, w - 50, 260], fill=(10, 15, 30)) # shadow for crescent
    # Lunar crater horizon
    d.polygon([(0, 550), (w * 0.3, 500), (w * 0.7, 530), (w, 480), (w, h), (0, h)], fill=(20, 26, 40))
    # Parabolic antenna wireframe
    d.arc([w//2 - 180, 340, w//2 + 180, 620], start=180, end=360, fill=(6, 182, 212), width=4)
    d.line([(w//2, 480), (w//2, 300)], fill=(168, 85, 247), width=3)
    d.ellipse([w//2 - 12, 290, w//2 + 12, 314], fill=(255, 255, 255))
    return canvas

# Scene: Sky Ascent (Adventure)
def draw_scene_sky_ascent(canvas):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Floating mountain peaks
    d.polygon([(80, 500), (220, 280), (360, 520)], fill=(30, 41, 59))
    d.polygon([(w - 380, 540), (w - 220, 320), (w - 60, 560)], fill=(30, 41, 59))
    # Cloud billows
    for cx, cy, rad in [(150, 560, 140), (320, 580, 160), (w - 200, 570, 180), (w//2, 620, 200)]:
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(240, 249, 255, 70))
    # Airship Galleon silhouette
    gx, gy = w // 2, 440
    d.ellipse([gx - 180, gy - 60, gx + 180, gy + 30], fill=(16, 185, 129)) # hull
    d.line([(gx - 120, gy - 60), (gx - 120, gy - 200)], fill=(251, 191, 36), width=4) # masts
    d.line([(gx + 60, gy - 60), (gx + 60, gy - 220)], fill=(251, 191, 36), width=4)
    # Billowing solar sails
    d.polygon([(gx - 120, gy - 190), (gx - 20, gy - 130), (gx - 120, gy - 70)], fill=(254, 240, 138, 200))
    d.polygon([(gx + 60, gy - 210), (gx + 170, gy - 140), (gx + 60, gy - 80)], fill=(254, 240, 138, 200))
    return canvas

# Scene: Weather Bazaar (Adventure)
def draw_scene_weather_bazaar(canvas):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Hanging lanterns with lightning glow
    for lx, ly, col in [(160, 280, (234, 179, 8)), (w//2, 220, (168, 85, 247)), (w - 160, 290, (6, 182, 212))]:
        d.line([(lx, 100), (lx, ly)], fill=(200, 200, 200), width=2)
        d.ellipse([lx - 45, ly - 45, lx + 45, ly + 45], fill=(*col, 60))
        d.rectangle([lx - 25, ly - 35, lx + 25, ly + 35], fill=col, outline=(255, 255, 255), width=2)
    # Bazaar canopies
    d.polygon([(40, 480), (w//2, 400), (40, 420)], fill=(16, 185, 129, 210))
    d.polygon([(w - 40, 480), (w//2, 400), (w - 40, 420)], fill=(245, 158, 11, 210))
    return canvas

# ----------------- 2. CHARACTERS -----------------

def draw_char_conductor(canvas, rim):
    d = ImageDraw.Draw(canvas)
    cx, cy = 300, 280
    # Peak cap
    d.ellipse([cx - 80, cy - 100, cx + 80, cy - 30], fill=(20, 20, 25))
    d.rectangle([cx - 100, cy - 50, cx + 100, cy - 25], fill=(185, 28, 28))
    # Glowing disembodied eyes / mic grille
    d.rectangle([cx - 50, cy - 10, cx + 50, cy + 40], fill=(239, 68, 68), outline=(255, 255, 255), width=2)
    for ly in range(cy, cy + 35, 8):
        d.line([(cx - 40, ly), (cx + 40, ly)], fill=(15, 15, 20), width=2)
    # Coat collar
    d.polygon([(cx - 120, 460), (cx, 350), (cx + 120, 460), (cx + 150, 520), (cx - 150, 520)], fill=(28, 30, 40))
    return canvas

def draw_char_stranger(canvas, rim):
    d = ImageDraw.Draw(canvas)
    cx, cy = 300, 280
    # Wide brim fedora / coat
    d.ellipse([cx - 130, cy - 70, cx + 130, cy - 10], fill=(50, 55, 65))
    d.rectangle([cx - 90, cy - 110, cx + 90, cy - 50], fill=(35, 40, 50))
    # Dark glasses & slate collar
    d.rectangle([cx - 55, cy - 5, cx + 55, cy + 25], fill=(15, 20, 25), outline=(239, 68, 68), width=2)
    d.polygon([(cx - 140, 480), (cx, 340), (cx + 140, 480), (cx + 160, 530), (cx - 160, 530)], fill=(71, 85, 105))
    return canvas

def draw_char_tara(canvas, rim):
    d = ImageDraw.Draw(canvas)
    cx, cy = 300, 270
    # Aviator goggles
    d.ellipse([cx - 65, cy - 60, cx - 10, cy - 5], fill=(217, 119, 6), outline=(251, 191, 36), width=3)
    d.ellipse([cx + 10, cy - 60, cx + 65, cy - 5], fill=(217, 119, 6), outline=(251, 191, 36), width=3)
    d.line([(cx - 10, cy - 32), (cx + 10, cy - 32)], fill=(251, 191, 36), width=4)
    # Wind-swept scarf & green leather coat
    d.polygon([(cx - 50, cy + 40), (cx + 90, cy + 90), (cx + 150, cy + 40)], fill=(16, 185, 129))
    d.polygon([(cx - 130, 480), (cx, 340), (cx + 130, 480), (cx + 150, 530), (cx - 150, 530)], fill=(5, 150, 105))
    return canvas

def draw_char_lumi(canvas, rim):
    d = ImageDraw.Draw(canvas)
    cx, cy = 300, 270
    # Glowing ethereal orb sprite with wings
    d.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], fill=(6, 182, 212, 190), outline=(255, 255, 255), width=3)
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(255, 255, 255))
    # Gossamer wings
    d.ellipse([cx - 160, cy - 100, cx - 60, cy + 40], fill=(16, 185, 129, 120), outline=(255, 255, 255, 160))
    d.ellipse([cx + 60, cy - 100, cx + 160, cy + 40], fill=(16, 185, 129, 120), outline=(255, 255, 255, 160))
    return canvas

def draw_char_rao(canvas, rim):
    d = ImageDraw.Draw(canvas)
    cx, cy = 300, 270
    # Round spectacles
    d.ellipse([cx - 65, cy - 40, cx - 10, cy + 15], fill=(254, 240, 138, 120), outline=(133, 77, 14), width=4)
    d.ellipse([cx + 10, cy - 40, cx + 65, cy + 15], fill=(254, 240, 138, 120), outline=(133, 77, 14), width=4)
    d.line([(cx - 10, cy - 12), (cx + 10, cy - 12)], fill=(133, 77, 14), width=3)
    # Bureaucrat Nehru jacket with pen in pocket
    d.polygon([(cx - 120, 480), (cx, 340), (cx + 120, 480), (cx + 140, 530), (cx - 140, 530)], fill=(180, 83, 9))
    d.rectangle([cx + 40, 390, cx + 55, 430], fill=(239, 68, 68)) # red pen
    return canvas

def draw_char_sharma(canvas, rim):
    d = ImageDraw.Draw(canvas)
    cx, cy = 300, 270
    # Flamboyant floral bindi & earrings
    d.ellipse([cx - 10, cy - 60, cx + 10, cy - 40], fill=(239, 68, 68))
    d.ellipse([cx - 80, cy + 10, cx - 60, cy + 30], fill=(251, 191, 36))
    d.ellipse([cx + 60, cy + 10, cx + 80, cy + 30], fill=(251, 191, 36))
    # Saree drape over shoulder
    d.polygon([(cx - 130, 490), (cx - 30, 330), (cx + 130, 490), (cx + 150, 530), (cx - 150, 530)], fill=(217, 70, 239))
    return canvas

def draw_char_orson(canvas, rim):
    d = ImageDraw.Draw(canvas)
    cx, cy = 300, 270
    # Space engineer helmet / visor
    d.ellipse([cx - 90, cy - 90, cx + 90, cy + 60], fill=(15, 23, 42), outline=(6, 182, 212), width=3)
    d.ellipse([cx - 70, cy - 45, cx + 70, cy + 30], fill=(6, 182, 212, 180), outline=(255, 255, 255), width=2)
    # Telemetry HUD line across visor
    d.line([(cx - 60, cy - 5), (cx + 60, cy - 5)], fill=(255, 255, 255), width=2)
    # Space suit collar
    d.polygon([(cx - 140, 480), (cx, 350), (cx + 140, 480), (cx + 160, 530), (cx - 160, 530)], fill=(30, 41, 59))
    return canvas

def draw_char_bot(canvas, rim):
    d = ImageDraw.Draw(canvas)
    cx, cy = 300, 270
    # Drone chassis (hexagonal / rounded tech box)
    d.rectangle([cx - 80, cy - 70, cx + 80, cy + 70], fill=(30, 41, 59), outline=(168, 85, 247), width=4)
    # Central optical sensor eye
    d.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], fill=(6, 182, 212), outline=(255, 255, 255), width=3)
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(255, 255, 255))
    # Antennas & thrusters
    d.line([(cx - 50, cy - 70), (cx - 70, cy - 120)], fill=(168, 85, 247), width=3)
    d.line([(cx + 50, cy - 70), (cx + 70, cy - 120)], fill=(168, 85, 247), width=3)
    return canvas

# ----------------- 3. CLUES -----------------

def draw_clue_emergency_key(canvas, acc):
    d = ImageDraw.Draw(canvas)
    cx, cy = 250, 220
    # Heavy notched key
    d.ellipse([cx - 50, cy - 80, cx + 50, cy + 20], fill=(234, 179, 8), outline=(255, 255, 255), width=2)
    d.ellipse([cx - 20, cy - 50, cx + 20, cy - 10], fill=(20, 25, 35))
    d.rectangle([cx - 15, cy + 20, cx + 15, cy + 150], fill=(234, 179, 8))
    # Notches
    d.rectangle([cx + 15, cy + 90, cx + 45, cy + 115], fill=(234, 179, 8))
    d.rectangle([cx + 15, cy + 125, cx + 55, cy + 145], fill=(234, 179, 8))
    # Crimson tag
    d.polygon([(cx - 70, cy + 60), (cx - 20, cy + 60), (cx - 35, cy + 130), (cx - 85, cy + 130)], fill=(239, 68, 68))
    return canvas

def draw_clue_ghost_ticket(canvas, acc):
    d = ImageDraw.Draw(canvas)
    # Metro ticket card
    d.rectangle([110, 140, 390, 290], fill=(241, 245, 249), outline=(239, 68, 68), width=3)
    d.rectangle([110, 140, 390, 180], fill=(239, 68, 68))
    d.text((250, 160), "METRO PASS - PLATFORM ZERO", fill=(255, 255, 255), anchor="mm")
    d.text((250, 220), "DESTINATION: UNKNOWN", fill=(15, 23, 42), anchor="mm")
    # Barcode
    for x in range(140, 360, 12):
        d.line([(x, 250), (x, 275)], fill=(15, 23, 42), width=random.choice([2, 4, 6]))
    return canvas

def draw_clue_intercom_log(canvas, acc):
    d = ImageDraw.Draw(canvas)
    # Audio cassette tape
    d.rectangle([110, 140, 390, 300], fill=(30, 41, 59), outline=(239, 68, 68), width=3)
    d.rectangle([140, 180, 360, 260], fill=(248, 250, 252))
    # Tape spools
    d.ellipse([180, 205, 220, 245], fill=(15, 23, 42), outline=(239, 68, 68), width=2)
    d.ellipse([280, 205, 320, 245], fill=(15, 23, 42), outline=(239, 68, 68), width=2)
    d.text((250, 160), "PRECOGNITION TAPE #7", fill=(239, 68, 68), anchor="mm")
    return canvas

def draw_clue_monsoon_compass(canvas, acc):
    d = ImageDraw.Draw(canvas)
    cx, cy = 250, 210
    # Brass compass ring
    d.ellipse([cx - 100, cy - 100, cx + 100, cy + 100], fill=(30, 41, 59), outline=(251, 191, 36), width=4)
    d.ellipse([cx - 85, cy - 85, cx + 85, cy + 85], outline=(16, 185, 129), width=2)
    # Dial needle (North/South)
    d.polygon([(cx, cy - 75), (cx - 15, cy), (cx + 15, cy)], fill=(239, 68, 68)) # North needle
    d.polygon([(cx, cy + 75), (cx - 15, cy), (cx + 15, cy)], fill=(148, 163, 184)) # South needle
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(251, 191, 36))
    return canvas

def draw_clue_weather_vial(canvas, acc):
    d = ImageDraw.Draw(canvas)
    cx, cy = 250, 210
    # Glass bottle with stopper
    d.rectangle([cx - 20, cy - 110, cx + 20, cy - 80], fill=(180, 83, 9)) # cork
    d.polygon([(cx - 40, cy - 80), (cx + 40, cy - 80), (cx + 70, cy + 90), (cx - 70, cy + 90)], fill=(6, 182, 212, 160), outline=(255, 255, 255), width=2)
    # Trapped lightning spark inside
    d.line([(cx, cy - 40), (cx + 20, cy), (cx - 15, cy + 20), (cx + 10, cy + 60)], fill=(251, 191, 36), width=4)
    return canvas

def draw_clue_rejected_stamp(canvas, acc):
    d = ImageDraw.Draw(canvas)
    cx, cy = 250, 210
    # Wooden stamp handle
    d.ellipse([cx - 25, cy - 110, cx + 25, cy - 70], fill=(133, 77, 14))
    d.rectangle([cx - 15, cy - 70, cx + 15, cy + 10], fill=(161, 98, 7))
    d.rectangle([cx - 90, cy + 10, cx + 90, cy + 60], fill=(70, 30, 20), outline=(234, 179, 8), width=2)
    # Crimson stamped impression
    d.rectangle([cx - 80, cy + 80, cx + 80, cy + 130], outline=(239, 68, 68), width=3)
    d.text((cx, cy + 105), "REJECTED", fill=(239, 68, 68), anchor="mm")
    return canvas

def draw_clue_coolant_schematic(canvas, acc):
    d = ImageDraw.Draw(canvas)
    # Sci-fi holographic grid & circuit lines
    d.rectangle([100, 110, 400, 310], fill=(10, 18, 32), outline=(6, 182, 212), width=2)
    for x in range(120, 390, 30):
        d.line([(x, 110), (x, 310)], fill=(6, 182, 212, 60), width=1)
    for y in range(130, 300, 30):
        d.line([(100, y), (400, y)], fill=(6, 182, 212, 60), width=1)
    # Core reactor blueprint
    d.ellipse([210, 170, 290, 250], outline=(239, 68, 68), width=3)
    d.line([(150, 210), (350, 210)], fill=(6, 182, 212), width=3)
    d.text((250, 290), "COOLANT MANIFOLD v4", fill=(6, 182, 212), anchor="mm")
    return canvas

def draw_clue_future_audio(canvas, acc):
    d = ImageDraw.Draw(canvas)
    cx, cy = 250, 210
    # Holographic data crystal
    d.polygon([(cx, cy - 90), (cx + 60, cy - 20), (cx, cy + 90), (cx - 60, cy - 20)], fill=(168, 85, 247, 180), outline=(255, 255, 255), width=2)
    # Audio waveform rings
    d.ellipse([cx - 85, cy - 85, cx + 85, cy + 85], outline=(6, 182, 212), width=2)
    return canvas

def draw_clue_quantum_dog(canvas, acc):
    d = ImageDraw.Draw(canvas)
    cx, cy = 250, 210
    # Atomic orbital rings
    d.ellipse([cx - 90, cy - 40, cx + 90, cy + 40], outline=(6, 182, 212), width=2)
    d.ellipse([cx - 40, cy - 90, cx + 40, cy + 90], outline=(168, 85, 247), width=2)
    # Pet collar tag
    d.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], fill=(251, 191, 36), outline=(255, 255, 255), width=2)
    d.text((cx, cy), "ψ", fill=(15, 23, 42), anchor="mm")
    return canvas

# ----------------- 4. ENDINGS -----------------

def draw_end_platform_zero(canvas, acc):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Empty misty subway platform with glowing 0
    d.polygon([(80, h), (w - 80, h), (w * 0.7, 450), (w * 0.3, 450)], fill=(20, 24, 34))
    d.ellipse([w//2 - 90, 300, w//2 + 90, 480], outline=(239, 68, 68), width=8)
    d.text((w//2, 390), "0", fill=(239, 68, 68), anchor="mm")
    return canvas

def draw_end_emergency_override(canvas, acc):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Train screeching to halt, sunlight beams
    for angle in range(-45, 45, 12):
        rad = math.radians(angle)
        d.line([(w//2, 200), (w//2 + int(600 * math.sin(rad)), int(600 * math.cos(rad)))], fill=(254, 240, 138, 90), width=6)
    d.polygon([(w//2 - 120, 520), (w//2 + 120, 520), (w//2 + 180, h), (w//2 - 180, h)], fill=(40, 50, 65))
    return canvas

def draw_end_sky_sanctuary(canvas, acc):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Celestial temple on cloud peak
    d.polygon([(w//2 - 140, 440), (w//2, 300), (w//2 + 140, 440)], fill=(251, 191, 36))
    for cx, cy, rad in [(w//2 - 120, 520, 140), (w//2 + 120, 520, 140), (w//2, 540, 180)]:
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(240, 249, 255, 90))
    return canvas

def draw_end_restore_monsoon(canvas, acc):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Rainbow arc over verdant hills
    d.arc([w//2 - 350, 200, w//2 + 350, 800], start=180, end=360, fill=(239, 68, 68), width=6)
    d.arc([w//2 - 340, 210, w//2 + 340, 790], start=180, end=360, fill=(234, 179, 8), width=6)
    d.arc([w//2 - 330, 220, w//2 + 330, 780], start=180, end=360, fill=(16, 185, 129), width=6)
    d.arc([w//2 - 320, 230, w//2 + 320, 770], start=180, end=360, fill=(6, 182, 212), width=6)
    # Rolling green hills
    d.ellipse([-100, 500, 500, 900], fill=(5, 150, 105))
    d.ellipse([400, 520, 1000, 900], fill=(4, 120, 87))
    return canvas

def draw_end_honest_day(canvas, acc):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Sun rays streaming over clean office desk
    for angle in range(-30, 30, 8):
        rad = math.radians(angle)
        d.line([(w//2, 100), (w//2 + int(700 * math.sin(rad)), int(700 * math.cos(rad)))], fill=(254, 240, 138, 120), width=8)
    d.rectangle([150, 500, w - 150, 580], fill=(133, 77, 14), outline=(234, 179, 8), width=3)
    return canvas

def draw_end_bootstrap_paradox(canvas, acc):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Mobius / infinity vortex
    cx, cy = w // 2, 400
    d.ellipse([cx - 160, cy - 70, cx, cy + 70], outline=(6, 182, 212), width=6)
    d.ellipse([cx, cy - 70, cx + 160, cy + 70], outline=(168, 85, 247), width=6)
    return canvas

def draw_end_paradox_reboot(canvas, acc):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Earth glowing peacefully through spacecraft dome
    d.ellipse([w//2 - 160, 260, w//2 + 160, 580], fill=(6, 182, 212), outline=(255, 255, 255), width=4)
    d.arc([100, 200, w - 100, 800], start=180, end=360, fill=(148, 163, 184), width=10)
    return canvas

def draw_end_timeline_prevented(canvas, acc):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    # Serene starfield with quiet station
    d.ellipse([w//2 - 20, 380, w//2 + 20, 420], fill=(255, 255, 255))
    d.line([(w//2 - 100, 400), (w//2 + 100, 400)], fill=(6, 182, 212), width=3)
    return canvas

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("[1/4] Generating Scenes...")
    generate_cinematic_scene("scenes/scene_carriage.png", (25, 10, 15), (60, 15, 20), "Midnight Carriage 104", "Next Station: Platform Zero • Temporal Transit", (239, 68, 68), draw_scene_carriage)
    generate_cinematic_scene("scenes/scene_excuse_office.png", (45, 30, 10), (100, 60, 15), "Department of Excuses", "Cabinet Room 4B • Fabrications on Record", (234, 179, 8), draw_scene_excuse_office)
    generate_cinematic_scene("scenes/scene_lunar_comms.png", (8, 12, 24), (20, 30, 60), "Lunar Relay Station", "Crater Rim Sector 9 • Tachyon Transmission", (6, 182, 212), draw_scene_lunar_comms)
    generate_cinematic_scene("scenes/scene_sky_ascent.png", (12, 35, 60), (16, 90, 80), "The Cloud Galleon", "Ascending into Monsoon Peaks • Celestial Altitude", (16, 185, 129), draw_scene_sky_ascent)
    generate_cinematic_scene("scenes/scene_weather_bazaar.png", (30, 20, 45), (15, 60, 75), "The Weather Bazaar", "Floating Docks of Nimbus • Storm Merchants", (245, 158, 11), draw_scene_weather_bazaar)

    print("[2/4] Generating Characters...")
    generate_character_portrait("characters/char_conductor.png", (20, 10, 15, 255), (239, 68, 68), "The Conductor", "Midnight Train Overseer", "🎫", draw_char_conductor)
    generate_character_portrait("characters/char_stranger.png", (25, 28, 35, 255), (239, 68, 68), "The Woman in Grey", "Carriage 104 Passenger", "🕵️", draw_char_stranger)
    generate_character_portrait("characters/char_tara.png", (10, 30, 25, 255), (16, 185, 129), "Captain Tara", "Sky Galleon Commander", "🧭", draw_char_tara)
    generate_character_portrait("characters/char_lumi.png", (10, 35, 45, 255), (6, 182, 212), "Lumi", "Bioluminescent Sprite", "✨", draw_char_lumi)
    generate_character_portrait("characters/char_rao.png", (35, 25, 10, 255), (234, 179, 8), "Inspector Rao", "Chief Excuse Verifier", "📋", draw_char_rao)
    generate_character_portrait("characters/char_sharma.png", (35, 15, 30, 255), (217, 70, 239), "Mrs. Sharma", "Master Fabricator", "🌸", draw_char_sharma)
    generate_character_portrait("characters/char_orson.png", (12, 20, 35, 255), (6, 182, 212), "Engineer Orson", "Lunar Operations Lead", "🛰️", draw_char_orson)
    generate_character_portrait("characters/char_bot.png", (15, 18, 30, 255), (168, 85, 247), "Unit 7 Maintenance Bot", "Autonomous AI Technician", "🤖", draw_char_bot)

    print("[3/4] Generating Clues...")
    generate_clue_artifact("clues/clue_emergency_key.png", (25, 12, 16, 255), (239, 68, 68), "Cabin 104 Override Key", "Thriller Evidence", draw_clue_emergency_key)
    generate_clue_artifact("clues/clue_ghost_ticket.png", (20, 15, 20, 255), (239, 68, 68), "Ghost Train Ticket", "Precognition Item", draw_clue_ghost_ticket)
    generate_clue_artifact("clues/clue_intercom_log.png", (20, 18, 26, 255), (239, 68, 68), "Precognition Tape #7", "Audio Evidence", draw_clue_intercom_log)
    generate_clue_artifact("clues/clue_monsoon_compass.png", (15, 30, 25, 255), (16, 185, 129), "Monsoon Compass", "Navigational Relic", draw_clue_monsoon_compass)
    generate_clue_artifact("clues/clue_weather_vial.png", (10, 30, 35, 255), (6, 182, 212), "Captured Storm Vial", "Elemental Sample", draw_clue_weather_vial)
    generate_clue_artifact("clues/clue_rejected_stamp.png", (35, 25, 10, 255), (234, 179, 8), "Bureaucratic Stamp", "Official Seal", draw_clue_rejected_stamp)
    generate_clue_artifact("clues/clue_coolant_schematic.png", (10, 20, 35, 255), (6, 182, 212), "Fusion Coolant Grid", "Schematic Hologram", draw_clue_coolant_schematic)
    generate_clue_artifact("clues/clue_future_audio.png", (20, 15, 35, 255), (168, 85, 247), "Quantum Waveform", "Tachyon Recording", draw_clue_future_audio)
    generate_clue_artifact("clues/clue_quantum_dog.png", (15, 20, 35, 255), (6, 182, 212), "Quantum State Collar", "Temporal Pet Collar", draw_clue_quantum_dog)

    print("[4/4] Generating Endings...")
    generate_ending_scene("endings/end_platform_zero_arrival.png", (20, 10, 15), (50, 15, 20), "Arrival at Platform Zero", "You step onto the mist-veiled platform, discovering the conductors who orchestrate the unwritten journeys.", (239, 68, 68), draw_end_platform_zero)
    generate_ending_scene("endings/end_emergency_override.png", (30, 20, 15), (80, 50, 20), "Emergency Override", "You insert the bypass key and trip the brake, bringing Carriage 104 screaming back to the sunlit real world.", (239, 68, 68), draw_end_emergency_override)
    generate_ending_scene("endings/end_sky_sanctuary.png", (15, 35, 55), (20, 80, 70), "The Celestial Sanctuary", "Captain Tara docks the Cloud Galleon at the forgotten high temple, securing the storm core.", (16, 185, 129), draw_end_sky_sanctuary)
    generate_ending_scene("endings/end_restore_monsoon.png", (10, 40, 30), (15, 90, 60), "The Monsoon Restored", "Breaking the storm vial releases rejuvenating rains across the continent, ending three decades of drought.", (16, 185, 129), draw_end_restore_monsoon)
    generate_ending_scene("endings/end_honest_day.png", (45, 30, 10), (100, 65, 20), "A Day of Confession", "Inspector Rao stamps your file APPROVED as you reveal the simple truth, setting off applause across the office.", (234, 179, 8), draw_end_honest_day)
    generate_ending_scene("endings/end_bootstrap_paradox.png", (15, 10, 30), (45, 25, 75), "The Closed Loop", "The tachyon transmission reaches your past self, locking the causality cycle in an eternal feedback loop.", (168, 85, 247), draw_end_bootstrap_paradox)
    generate_ending_scene("endings/end_paradox_reboot.png", (8, 20, 35), (20, 50, 80), "Temporal Reboot", "Unit 7 safely vents the coolant manifold, restoring linear chronology across the lunar relay network.", (6, 182, 212), draw_end_paradox_reboot)
    generate_ending_scene("endings/end_timeline_prevented.png", (10, 15, 30), (25, 35, 60), "Timeline Preserved", "The transmission shuts down before resonance occurs. Earth shines undisturbed across the lunar horizon.", (6, 182, 212), draw_end_timeline_prevented)

    print("[SUCCESS] All StoryPulse visual assets have been generated and mirrored to both backend and mobile assets!")
