# -*- coding: utf-8 -*-
"""
Update scripts/generate_all_assets.py to render macOS Glassmorphism design system.
"""
import os

path = os.path.join("CA6_Rust_Micro_OS_Engineering_Project", "scripts", "generate_all_assets.py")

with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Update color palette definitions
old_palette_def = '''# Modern Obsidian Glass Theme Palette
BG_DARK = (10, 16, 26)
TOP_BAR = (17, 24, 39)
CARD_BG = (15, 23, 42)
CARD_BORDER = (30, 41, 59)
TEXT_CYAN = (56, 189, 248)
TEXT_GREEN = (52, 211, 153)
TEXT_YELLOW = (251, 191, 36)
TEXT_PURPLE = (167, 139, 250)
TEXT_RED = (248, 113, 113)
TEXT_GRAY = (148, 163, 184)
TEXT_WHITE = (241, 245, 249)'''

new_palette_def = '''# macOS Glassmorphic Frosted Slate Palette
BG_DARK = (15, 17, 26)              # macOS Midnight Charcoal
TOP_BAR = (24, 27, 40)              # Frosted translucent menu bar
TOP_BAR_BORDER = (36, 42, 60)       # Menu bar divider
CARD_BG = (22, 26, 38)              # Frosted dark glass surface
CARD_HEADER = (30, 35, 52)          # Window titlebar surface
CARD_BORDER = (45, 52, 75)          # Glass border outline
DOCK_BG = (28, 32, 48)              # Floating dock pill
DOCK_BORDER = (58, 66, 96)          # Floating dock outline

MAC_RED = (255, 95, 87)             # Window close button (●)
MAC_YELLOW = (254, 188, 46)         # Window minimize button (●)
MAC_GREEN = (40, 201, 64)           # Window zoom button (●)
MAC_BLUE = (10, 132, 255)           # macOS System Blue
MAC_CYAN = (100, 210, 255)          # macOS System Teal
MAC_MINT = (48, 209, 88)            # macOS Spring Mint
MAC_ORANGE = (255, 159, 10)         # macOS Vibrant Orange
MAC_PURPLE = (191, 90, 242)         # macOS Deep Violet

TEXT_CYAN = MAC_CYAN
TEXT_GREEN = MAC_MINT
TEXT_YELLOW = MAC_ORANGE
TEXT_PURPLE = MAC_PURPLE
TEXT_RED = MAC_RED
TEXT_GRAY = (152, 162, 179)
TEXT_WHITE = (245, 247, 250)'''

code = code.replace(old_palette_def, new_palette_def)

# Helper to draw macOS window header with traffic lights
helper = '''
def draw_traffic_lights(draw, x, y, r=4):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=MAC_RED)
    draw.ellipse([x + 12 - r, y - r, x + 12 + r, y + r], fill=MAC_YELLOW)
    draw.ellipse([x + 24 - r, y - r, x + 24 + r, y + r], fill=MAC_GREEN)

def draw_glass_card(draw, x, y, w, h, title="", title_color=MAC_CYAN, badge="", badge_color=MAC_ORANGE):
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_BORDER)
    draw.rectangle([x + 1, y + 1, x + w - 1, y + 22], fill=CARD_HEADER)
    draw.line([(x, y + 22), (x + w, y + 22)], fill=CARD_BORDER)
    draw_traffic_lights(draw, x + 12, y + 11)
    if title:
        draw.text((x + 48, y + 4), title, font=FONT_BOLD, fill=title_color)
    if badge:
        draw.text((x + w - 85, y + 4), badge, font=FONT_BOLD, fill=badge_color)
'''

code = code.replace("def render_terminal_window(", helper + "\ndef render_terminal_window(")

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated generate_all_assets.py successfully with macOS Glassmorphic helpers!")
