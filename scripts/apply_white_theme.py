#!/usr/bin/env python3
"""
Aurora Neural OS - White / Light Mode Master Patcher
Author: Ved Raj | USN: 25BTRCL279 | JAIN FET
1. Changes background to pure crisp white [255, 255, 255]
2. Changes cards, terminal, bars to clean light theme
3. Sets high-contrast readable dark typography
4. Aligns all text strings to exact byte boundaries
"""

import sys, os, subprocess

IMG_SRC  = r"C:\Users\prath\OneDrive\Documents\OS mini project\CA6_Rust_Micro_OS_Project\target\micro-os-aurora.img"
VDI_OUT  = r"C:\Users\prath\OneDrive\Documents\OS mini project\micro-os-aurora.vdi"
VBOXMGR  = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
ELF_BASE = 0xbfa00

print("=" * 70)
print("  AURORA NEURAL OS - White / Light Theme Patcher")
print("  Author: Ved Raj | 25BTRCL279 | JAIN FET")
print("=" * 70)

# 1. Read disk image
with open(IMG_SRC, "rb") as f:
    data = bytearray(f.read())
print(f"[1] Loaded disk image ({len(data):,} bytes)")

# Helper: patch color in ELF machine code
# In x86_64:
# imm16 gets [r, g] (little endian)
# imm8 gets [b]
def set_color(imm8_off, imm16_off, r, g, b, label=""):
    data[ELF_BASE + imm8_off] = b
    data[ELF_BASE + imm16_off] = r
    data[ELF_BASE + imm16_off + 1] = g
    print(f"  [COLOR] {label:28} -> RGB=({r:3}, {g:3}, {b:3})")

# ─────────────────────────────────────────────────────────────────
# 2. Patch Surface & Background Colors (Light Theme)
# ─────────────────────────────────────────────────────────────────
print("\n[2] Applying White / Light Theme Surfaces...")

# Pure crisp white background for main desktop fill
set_color(0x66e8, 0x66f1, 255, 255, 255, "Desktop Background (Fill)")

# Clean Soft Pearl / Studio Gray for Top Menu Bar
set_color(0x6724, 0x672d, 241, 245, 249, "Top Menu Bar")

# Clean Soft Pearl / Studio Gray for Bottom Status Bar
set_color(0x721a, 0x7223, 241, 245, 249, "Bottom Status Bar")

# Pure crisp white for Card Backgrounds
set_color(0x8d4d, 0x8d53, 255, 255, 255, "Card Background")

# Clean Platinum Slate for Card Borders
set_color(0x8d83, 0x8d89, 203, 213, 225, "Card Border (Top)")
set_color(0x8e06, 0x8e0c, 203, 213, 225, "Card Border (Bottom)")
set_color(0x8e45, 0x8e4e, 203, 213, 225, "Card Border (Left)")
set_color(0x8edf, 0x8ee8, 203, 213, 225, "Card Border (Right)")

# Pure crisp white for Terminal Background
set_color(0x5b50, 0x5b59, 255, 255, 255, "Terminal Background")

# ─────────────────────────────────────────────────────────────────
# 3. Patch Typography Colors (High Contrast on White)
# ─────────────────────────────────────────────────────────────────
print("\n[3] Applying High-Contrast Dark Typography...")

# Title text "AURORA NEURAL OS" -> Bold Royal Blue
set_color(0x6767, 0x6770, 30, 64, 175, "Desktop Title (Royal Blue)")

# Menu bar labels -> Steel Slate
set_color(0x67bd, 0x67c6, 71, 85, 105, "Menu Bar Labels (Slate)")
set_color(0x6848, 0x6851, 5, 150, 105, "Menu Bar Accent (Emerald)")
set_color(0x68d4, 0x68dd, 194, 65, 12, "WiFi / Live Status (Amber)")

# Card 1 (Hardware Architecture)
set_color(0x69e3, 0x69ec, 29, 78, 216, "Card 1 Title (Sapphire)")
set_color(0x6a1e, 0x6a27, 29, 78, 216, "Card 1 Header Line")
set_color(0x6a94, 0x6a9d, 17, 24, 39,  "Card 1 Host Line (Charcoal)")
set_color(0x6aef, 0x6af8, 22, 163, 74, "Card 1 Net Line (Forest Green)")
set_color(0x6b4a, 0x6b53, 51, 65, 85,  "Card 1 Intr Line (Slate)")
set_color(0x6b95, 0x6b9e, 185, 28, 28, "Card 1 Boot Waterfall (Ruby)")

# Card 2 (Research: Page Replacement)
set_color(0x6c6d, 0x6c76, 109, 40, 217, "Card 2 Title (Royal Violet)")
set_color(0x6ce5, 0x6cee, 109, 40, 217, "Card 2 Header Line")
set_color(0x6d68, 0x6d71, 17, 24, 39,   "Card 2 Algos Line (Charcoal)")
set_color(0x6deb, 0x6df4, 30, 64, 175,  "Card 2 Results Line (Blue)")
set_color(0x6e6e, 0x6e77, 185, 28, 28,  "Card 2 Belady Line (Ruby)")
set_color(0x6ef1, 0x6efa, 22, 163, 74,  "Card 2 Commands Line (Green)")

# Card 3 / Terminal Window
set_color(0x702f, 0x7038, 15, 23, 42,   "Terminal Title (Deep Navy)")
set_color(0x70bf, 0x70c8, 180, 83, 9,   "Terminal Subtitle (Amber)")
set_color(0x7110, 0x7119, 17, 24, 39,   "Terminal Welcome Line 1")
set_color(0x7150, 0x7159, 51, 65, 85,   "Terminal Welcome Line 2")
set_color(0x7190, 0x7199, 22, 163, 74,  "Terminal Welcome Line 3")

# Terminal dynamic prompt & text
set_color(0x5c79, 0x5c82, 17, 24, 39,   "Terminal Body Text (Charcoal)")
set_color(0x5ec3, 0x5ecc, 29, 78, 216,  "Terminal Prompt (Royal Blue)")

# Bottom status bar text
set_color(0x7291, 0x729a, 51, 65, 85,   "Footer Text (Slate)")
set_color(0x7349, 0x7352, 5, 150, 105,  "Footer Status (Emerald)")

# ─────────────────────────────────────────────────────────────────
# 4. Patch Exact String Slices in .rodata
# ─────────────────────────────────────────────────────────────────
print("\n[4] Writing Exact-Width UI String Slices...")

strings_exact = [
    # (rodata_offset, exact_length, byte_string, label)
    (0x2960, 16, b'AURORA NEURAL OS', "Desktop Title"),
    (0x2980, 30, b'SYSTEM  NEURAL  RESEARCH  HELP', "Top Menu Items"),
    (0x299e, 17, b'WIFI-6: MT7921   ', "WiFi Indicator"),
    (0x29af,  7, b'ONLINE ', "Online Badge"),
    (0x29b6, 21, b'HARDWARE ADAPTATION  ', "Card 1 Header"),
    (0x29cb, 50, b'HOST: ASUS VIVOBOOK 15 (INTEL I5-12500H 12C/16T)  ', "Card 1 Line 1"),
    (0x29fd, 51, b'NET: MEDIATEK MT7921 WIFI-6 + GBE LAN (10.0.2.15)  ', "Card 1 Line 2"),
    (0x2a30, 52, b'INTERRUPT: IDT 256-ENTRY + PIT 20 HZ + PS/2 KEYBOARD', "Card 1 Line 3"),
    (0x2a64, 53, b'BOOT WATERFALL: 11.4MS -> 27.2MS -> 66.8MS -> 275.7MS', "Card 1 Line 4"),
    (0x2a99, 25, b'RESEARCH: PAGE REPLACEMNT', "Card 2 Header"),
    (0x2ab2, 48, b'PAGE ALGORITHMS: FIFO, LRU, OPTIMAL (VED RAJ)   ', "Card 2 Line 1"),
    (0x2ae2, 49, b'RESULTS: FIFO=34.8% LRU=24.1% OPT=14.7% (10K REF)', "Card 2 Line 2"),
    (0x2b13, 46, b'BELADY ANOMALY: CONFIRMED (FIFO 3F=9 -> 4F=10)', "Card 2 Line 3"),
    (0x2b41, 48, b'TRY COMMANDS: HELP, RESEARCH, TOP, HWINFO, CLEAR', "Card 2 Line 4"),
    (0x2b71, 52, b'INTERACTIVE TERMINAL CONSOLE // PS/2 KEYBOARD ACTIVE', "Terminal Header"),
    (0x2ba5, 24, b'TYPE COMMAND & HIT ENTER', "Terminal Hint"),
    (0x2bbd, 60, b'Welcome to Aurora Neural OS v2.6! (Ved Raj / 25BTRCL279 JGI)', "Terminal Welcome 1"),
    (0x2bf9, 66, b'Host: ASUS Vivobook 15 | Intel i5-12500H | WiFi-6 | Page Replace  ', "Terminal Welcome 2"),
    (0x2c3b, 62, b"Type 'research' for paper results, 'fault' for Belady anomaly.", "Terminal Welcome 3"),
    (0x2c79, 53, b'AURORA NEURAL OS READY / PS/2 SCANCODE DECODER ONLINE', "Footer Left"),
    (0x2cae, 30, b'STATUS: LIGHT THEME ACTIVE OK ', "Footer Right"),
    (0x291d, 17, b'vedraj@aurora:~$ ', "Shell Prompt"),
]

for rodata_off, expected_len, s, label in strings_exact:
    assert len(s) == expected_len, f"Length mismatch on {label}: expected {expected_len}, got {len(s)}"
    dest = ELF_BASE + rodata_off
    data[dest:dest+expected_len] = s
    print(f"  [STR] {label:24} ({expected_len:2}b) at 0x{rodata_off:04x} -> {s.decode()[:35]}...")

# 5. Write patched image
print(f"\n[5] Writing patched disk image: {IMG_SRC}")
with open(IMG_SRC, "wb") as f:
    f.write(data)
print("  [OK] Image written successfully")

# 6. Power off VM if running
print("\n[6] Ensuring VM is powered off...")
subprocess.run([VBOXMGR, "controlvm", "Micro-OS-64", "poweroff"], capture_output=True)

# 7. Convert to VDI
print(f"\n[7] Converting to VDI: {VDI_OUT}")
if os.path.exists(VDI_OUT):
    try:
        os.remove(VDI_OUT)
    except Exception as e:
        print(f"  [WARN] Could not remove old VDI: {e}")

res = subprocess.run(
    [VBOXMGR, "convertfromraw", IMG_SRC, VDI_OUT, "--format", "VDI"],
    capture_output=True, text=True
)
if res.returncode == 0:
    print(f"  [OK] VDI created successfully: {os.path.getsize(VDI_OUT):,} bytes")
else:
    print(f"  [ERROR] VBoxManage failed:\n{res.stderr}")
    sys.exit(1)

# 8. Re-attach and Start VM
print("\n[8] Re-attaching VDI and launching VM...")
subprocess.run([VBOXMGR, "storageattach", "Micro-OS-64", "--storagectl", "IDE",
                "--port", "0", "--device", "0", "--type", "hdd", "--medium", VDI_OUT],
               capture_output=True)
subprocess.run([VBOXMGR, "modifyvm", "Micro-OS-64", "--firmware", "bios"], capture_output=True)
res_start = subprocess.run([VBOXMGR, "startvm", "Micro-OS-64", "--type", "gui"], capture_output=True, text=True)
if res_start.returncode == 0:
    print("  [OK] VM started in VirtualBox GUI mode!")
else:
    print(f"  [NOTICE] VM start output: {res_start.stdout} / {res_start.stderr}")

print("\n" + "=" * 70)
print("  AURORA NEURAL OS - WHITE / LIGHT THEME APPLIED SUCCESSFULLY!")
print("=" * 70)
