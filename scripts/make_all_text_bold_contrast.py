#!/usr/bin/env python3
"""
High-Contrast Typography Overhaul for White Background
Author: Ved Raj | USN: 25BTRCL279 | JAIN FET
Transforms all 34 command output colors and header bars to bold, dark, high-contrast colors!
"""

import sys, os, subprocess, struct

IMG_SRC  = r"C:\Users\prath\OneDrive\Documents\OS mini project\CA6_Rust_Micro_OS_Engineering_Project\target\micro-os-aurora.img"
VDI_OUT  = r"C:\Users\prath\OneDrive\Documents\OS mini project\micro-os-aurora.vdi"
VBOXMGR  = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
ELF_BASE = 0xbfa00

with open(IMG_SRC, "rb") as f:
    data = bytearray(f.read())

print("[1] Loaded micro-os-aurora.img")

# 1. Color mapping for white background:
# Convert pastels/whites to bold, high-contrast, deeply readable colors
COLOR_MAP = {
    # Near-white (241, 245, 249) -> Rich Charcoal Black (17, 24, 39)
    (241, 245, 249): (17, 24, 39),

    # Light Yellow (251, 191, 36) -> Deep Amber / Burnt Orange (180, 83, 9)
    (251, 191, 36): (180, 83, 9),

    # Light Mint (74, 222, 128) -> Deep Forest Emerald (5, 150, 105)
    (74, 222, 128): (5, 150, 105),

    # Light Cyan (56, 189, 248) -> Deep Cobalt Blue (29, 78, 216)
    (56, 189, 248): (29, 78, 216),

    # Light Purple (192, 132, 252) -> Deep Royal Violet (109, 40, 217)
    (192, 132, 252): (109, 40, 217),

    # Light Slate (148, 163, 184) -> Dark Steel Slate (51, 65, 85)
    (148, 163, 184): (51, 65, 85),
}

exec_start = 0x73a0
exec_end = 0x8110
patched_count = 0

for i in range(exec_start, exec_end - 20):
    if data[ELF_BASE+i] == 0xc6 and data[ELF_BASE+i+1] == 0x84 and data[ELF_BASE+i+2] == 0x24:
        disp_b = struct.unpack_from('<I', data, ELF_BASE+i+3)[0]
        b = data[ELF_BASE+i+7]
        nxt = i + 8
        if nxt < exec_end - 10 and data[ELF_BASE+nxt] == 0x66 and data[ELF_BASE+nxt+1] == 0xc7 and data[ELF_BASE+nxt+2] == 0x84 and data[ELF_BASE+nxt+3] == 0x24:
            disp_rg = struct.unpack_from('<I', data, ELF_BASE+nxt+4)[0]
            if disp_b == disp_rg + 2:
                r = data[ELF_BASE+nxt+8]
                g = data[ELF_BASE+nxt+9]
                old_rgb = (r, g, b)
                if old_rgb in COLOR_MAP:
                    new_rgb = COLOR_MAP[old_rgb]
                    # Patch b
                    data[ELF_BASE+i+7] = new_rgb[2]
                    # Patch r, g
                    data[ELF_BASE+nxt+8] = new_rgb[0]
                    data[ELF_BASE+nxt+9] = new_rgb[1]
                    patched_count += 1
                    print(f"  [COLOR {patched_count:2}] at 0x{nxt+8:x}: {old_rgb} -> {new_rgb}")

print(f"\n[2] Patched {patched_count} output colors to bold high-contrast!")

# 2. Terminal header title text "INTERACTIVE TERMINAL CONSOLE" -> Deep Slate / White
# Keep header bar stable from kernel ELF

# 3. Terminal header title text "INTERACTIVE TERMINAL CONSOLE" -> Bold Royal Blue
# At 0x702f: imm8=0x702f, imm16=0x7038
data[ELF_BASE + 0x702f] = 175 # B
data[ELF_BASE + 0x7038] = 30  # R
data[ELF_BASE + 0x7039] = 64  # G

# 4. Terminal header hint "TYPE COMMAND HIT ENTER" -> Deep Amber [180, 83, 9]
# At 0x70bf: imm8=0x70bf, imm16=0x70c8
data[ELF_BASE + 0x70bf] = 9   # B
data[ELF_BASE + 0x70c8] = 180 # R
data[ELF_BASE + 0x70c9] = 83  # G

with open(IMG_SRC, "wb") as f:
    f.write(data)
print("[3] Image written.")

# 5. Power off VM cleanly
subprocess.run([VBOXMGR, "controlvm", "Micro-OS-64", "poweroff"], capture_output=True)

# 6. Re-generate VDI
if os.path.exists(VDI_OUT):
    try: os.remove(VDI_OUT)
    except: pass

res = subprocess.run([VBOXMGR, "convertfromraw", IMG_SRC, VDI_OUT, "--format", "VDI"], capture_output=True, text=True)
if res.returncode == 0:
    print(f"[4] VDI re-generated: {os.path.getsize(VDI_OUT):,} bytes")
    # Restore UUID
    subprocess.run([VBOXMGR, "internalcommands", "sethduuid", VDI_OUT, "0f2ea5af-32ed-4525-aa38-a0b2a95984fa"], capture_output=True)
    subprocess.run([VBOXMGR, "storageattach", "Micro-OS-64", "--storagectl", "IDE", "--port", "0", "--device", "0", "--type", "hdd", "--medium", VDI_OUT], capture_output=True)
    subprocess.run([VBOXMGR, "modifyvm", "Micro-OS-64", "--mouse", "usbtablet"], capture_output=True)
    subprocess.run([VBOXMGR, "startvm", "Micro-OS-64", "--type", "gui"], capture_output=True)
    print("[5] VM restarted in GUI mode with bold, crystal-clear typography!")
else:
    print("VBoxManage convert error:", res.stderr)
