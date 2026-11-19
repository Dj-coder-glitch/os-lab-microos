#!/usr/bin/env python3
"""
Fix typing visibility (Black text on White) and mouse capture in VirtualBox
Author: Ved Raj | USN: 25BTRCL279 | JAIN FET
"""

import sys, os, subprocess

IMG_SRC  = r"C:\Users\prath\OneDrive\Documents\OS mini project\CA6_Rust_Micro_OS_Engineering_Project\target\micro-os-aurora.img"
VDI_OUT  = r"C:\Users\prath\OneDrive\Documents\OS mini project\micro-os-aurora.vdi"
VBOXMGR  = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
ELF_BASE = 0xbfa00

with open(IMG_SRC, "rb") as f:
    data = bytearray(f.read())

print("[1] Loaded micro-os-aurora.img")

# 1. Patch input text color from [255, 255, 255] (white) to [17, 24, 39] (Charcoal Black)
# In redraw_term:
# 0x5e08: r
# 0x5e10: g
# 0x5e18: b
print(f"Original input text color bytes: {data[ELF_BASE+0x5e08]}, {data[ELF_BASE+0x5e10]}, {data[ELF_BASE+0x5e18]}")
data[ELF_BASE + 0x5e08] = 17  # R = 17
data[ELF_BASE + 0x5e10] = 24  # G = 24
data[ELF_BASE + 0x5e18] = 39  # B = 39
print("Patched input text color to Charcoal Black [17, 24, 39]!")

# 2. Patch cursor color to Bold Royal Blue [29, 78, 216]
# In redraw_term:
# 0x5ec3: b (imm8)
# 0x5ecc: r (imm16 low)
# 0x5ecd: g (imm16 high)
data[ELF_BASE + 0x5ec3] = 216 # B
data[ELF_BASE + 0x5ecc] = 29  # R
data[ELF_BASE + 0x5ecd] = 78  # G
print("Patched cursor color to Bold Royal Blue [29, 78, 216]!")

with open(IMG_SRC, "wb") as f:
    f.write(data)
print("[2] Image saved.")

# 3. Power off VM cleanly
subprocess.run([VBOXMGR, "controlvm", "Micro-OS-64", "poweroff"], capture_output=True)

# 4. Configure VirtualBox mouse integration so touchpad clicks NEVER trap the mouse pointer!
subprocess.run([VBOXMGR, "modifyvm", "Micro-OS-64", "--mouse", "usbtablet"], capture_output=True)
print("[3] Configured VirtualBox with USB Tablet pointer (no mouse trapping)!")

# 5. Convert to VDI
if os.path.exists(VDI_OUT):
    try: os.remove(VDI_OUT)
    except: pass

res = subprocess.run([VBOXMGR, "convertfromraw", IMG_SRC, VDI_OUT, "--format", "VDI"], capture_output=True, text=True)
if res.returncode == 0:
    print(f"[4] VDI re-generated: {os.path.getsize(VDI_OUT):,} bytes")
    # Restore UUID
    subprocess.run([VBOXMGR, "internalcommands", "sethduuid", VDI_OUT, "0f2ea5af-32ed-4525-aa38-a0b2a95984fa"], capture_output=True)
    subprocess.run([VBOXMGR, "storageattach", "Micro-OS-64", "--storagectl", "IDE", "--port", "0", "--device", "0", "--type", "hdd", "--medium", VDI_OUT], capture_output=True)
    subprocess.run([VBOXMGR, "startvm", "Micro-OS-64", "--type", "gui"], capture_output=True)
    print("[5] VM restarted in GUI mode!")
else:
    print("VBoxManage convert error:", res.stderr)
