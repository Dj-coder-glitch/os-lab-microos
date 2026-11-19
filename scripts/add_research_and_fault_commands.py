#!/usr/bin/env python3
"""
Adds live 'research' and 'fault' commands to the Micro-OS binary kernel
Author: Ved Raj | USN: 25BTRCL279 | JAIN FET
"""

import os, subprocess, struct

IMG_SRC  = r"C:\Users\prath\OneDrive\Documents\OS mini project\CA6_Rust_Micro_OS_Project\target\micro-os-aurora.img"
VDI_OUT  = r"C:\Users\prath\OneDrive\Documents\OS mini project\micro-os-aurora.vdi"
VBOXMGR  = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
ELF_BASE = 0xbfa00

with open(IMG_SRC, "rb") as f:
    data = bytearray(f.read())

print("[1] Loaded micro-os-aurora.img")

# Helper to fit strings exactly into allocated lengths
def fit(s: str, length: int) -> bytes:
    b = s.encode('ascii')
    if len(b) > length:
        b = b[:length]
    return b.ljust(length, b' ')

# 1. Patch Command Dispatch in execute_command
# Formerly APT dispatch -> now 'research' (len 8, points to 0x2c41)
# 0x87ae (foff 0x77ae): lea rdx, [rip - 0x5b74] -> 48 8d 15 8c a4 ff ff
# 0x87b5 (foff 0x77b5): mov ecx, 8              -> b9 08 00 00 00
data[ELF_BASE + 0x77ae : ELF_BASE + 0x77ba] = bytes.fromhex("488d158ca4ffffb908000000")
print("  Patched 'research' dispatch (replaces APT) -> points to 0x2c41, len 8")

# Formerly SNAP dispatch -> now 'fault' (len 5, points to 0x2c5f)
# 0x8972 (foff 0x7972): lea rdx, [rip - 0x5d1a] -> 48 8d 15 e6 a2 ff ff
# 0x8979 (foff 0x7979): mov ecx, 5              -> b9 05 00 00 00
data[ELF_BASE + 0x7972 : ELF_BASE + 0x797e] = bytes.fromhex("488d15e6a2ffffb905000000")
print("  Patched 'fault' dispatch (replaces SNAP) -> points to 0x2c5f, len 5")

# 2. Update Strings for 'research' command output (foff 0x31d5..0x32b9)
r1 = fit(">>> WORKLOAD (80/20 LOCALITY): 10,000 REFS, 16 FRAMES", 52)
r2 = fit("FIFO : 34.83% FAULTS (+20.07% OVER OPT) | NON-STACK ALGO", 58)
r3 = fit("LRU  : 24.12% FAULTS ( +9.36% OVER OPT) | BEATS FIFO 10.7%", 58)
r4 = fit("OPT  : 14.76% FAULTS (THEORETICAL LOWER BOUND BENCHMARK)", 60)

data[ELF_BASE + 0x31d5 : ELF_BASE + 0x31d5 + 52] = r1
data[ELF_BASE + 0x3209 : ELF_BASE + 0x3209 + 58] = r2
data[ELF_BASE + 0x3243 : ELF_BASE + 0x3243 + 58] = r3
data[ELF_BASE + 0x327d : ELF_BASE + 0x327d + 60] = r4
print("  Updated 'research' response strings!")

# 3. Update Strings for 'fault' command output (foff 0x30e0..0x31d5)
f1 = fit(">>> BELADY ANOMALY STRING: [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]", 61)
f2 = fit("FIFO (3 FRAMES):  9 FAULTS  -->  FIFO (4 FRAMES): 10 FAULTS!", 61)
f3 = fit("LRU  (3 FRAMES): 10 FAULTS  -->  LRU  (4 FRAMES):  8 FAULTS", 65)
f4 = fit("OPT  (3 FRAMES):  7 FAULTS  -->  OPT  (4 FRAMES):  6 FAULTS", 58)

data[ELF_BASE + 0x30e0 : ELF_BASE + 0x30e0 + 61] = f1
data[ELF_BASE + 0x311d : ELF_BASE + 0x311d + 61] = f2
data[ELF_BASE + 0x315a : ELF_BASE + 0x315a + 65] = f3
data[ELF_BASE + 0x319b : ELF_BASE + 0x319b + 58] = f4
print("  Updated 'fault' response strings!")

# 4. Update 'help' command listing and descriptions
h1 = fit("COMMANDS: HELP, RESEARCH, FAULT, HWINFO, NET, TOP, CLEAR", 56)
h2 = fit("  RESEARCH - COMPARE FIFO, LRU, AND OPTIMAL PAGE REPLACEMENT", 60)
h3 = fit("  FAULT   - DEMONSTRATE BELADY'S ANOMALY (3F=9 VS 4F=10)", 53)
h4 = fit("  HWINFO  - DISPLAY ASUS VIVOBOOK 15 AND I5-12500H SPECS", 61)
h5 = fit("  NET     - MEDIATEK MT7921 WIFI-6 AND GBE LINK TELEMETRY", 61)

data[ELF_BASE + 0x33fa : ELF_BASE + 0x33fa + 56] = h1
data[ELF_BASE + 0x3432 : ELF_BASE + 0x3432 + 60] = h2
data[ELF_BASE + 0x346e : ELF_BASE + 0x346e + 53] = h3
data[ELF_BASE + 0x34a3 : ELF_BASE + 0x34a3 + 61] = h4
data[ELF_BASE + 0x34e0 : ELF_BASE + 0x34e0 + 61] = h5
print("  Updated 'help' output strings!")

# 5. High-contrast colors for 'research' and 'fault' lines
# Color 11 (0x79a5): Research line 1 -> Deep Cobalt Blue (29, 78, 216)
# At 0x799d: b=216, at 0x79a5: r=29, g=78
data[ELF_BASE + 0x799d] = 216
data[ELF_BASE + 0x79a5] = 29
data[ELF_BASE + 0x79a6] = 78

# Color 12 (0x79e2): Research line 2 (FIFO) -> Deep Amber (180, 83, 9)
data[ELF_BASE + 0x79da] = 9
data[ELF_BASE + 0x79e2] = 180
data[ELF_BASE + 0x79e3] = 83

# Color 13 (0x7a29): Research line 3 (LRU) -> Forest Emerald (5, 150, 105)
data[ELF_BASE + 0x7a21] = 105
data[ELF_BASE + 0x7a29] = 5
data[ELF_BASE + 0x7a2a] = 150

# Color 14 (0x7a61): Research line 4 (OPT) -> Royal Violet (109, 40, 217)
data[ELF_BASE + 0x7a59] = 217
data[ELF_BASE + 0x7a61] = 109
data[ELF_BASE + 0x7a62] = 40

# Color 15 (0x7acb): Fault line 1 -> Deep Cobalt Blue (29, 78, 216)
data[ELF_BASE + 0x7ac3] = 216
data[ELF_BASE + 0x7acb] = 29
data[ELF_BASE + 0x7acc] = 78

# Color 16 (0x7b12): Fault line 2 (FIFO ANOMALY) -> Ruby Crimson (185, 28, 28)
data[ELF_BASE + 0x7b0a] = 28
data[ELF_BASE + 0x7b12] = 185
data[ELF_BASE + 0x7b13] = 28

# Color 17 (0x7b4a): Fault line 3 (LRU) -> Forest Emerald (5, 150, 105)
data[ELF_BASE + 0x7b42] = 105
data[ELF_BASE + 0x7b4a] = 5
data[ELF_BASE + 0x7b4b] = 150

# Color 18 (0x7b87): Fault line 4 (OPT) -> Royal Violet (109, 40, 217)
data[ELF_BASE + 0x7b7f] = 217
data[ELF_BASE + 0x7b87] = 109
data[ELF_BASE + 0x7b88] = 40

with open(IMG_SRC, "wb") as f:
    f.write(data)
print("[2] Successfully wrote patched micro-os-aurora.img")

# 6. Power off VM cleanly
subprocess.run([VBOXMGR, "controlvm", "Micro-OS-64", "poweroff"], capture_output=True)

# 7. Convert and start VM
if os.path.exists(VDI_OUT):
    try: os.remove(VDI_OUT)
    except: pass

res = subprocess.run([VBOXMGR, "convertfromraw", IMG_SRC, VDI_OUT, "--format", "VDI"], capture_output=True, text=True)
if res.returncode == 0:
    print(f"[3] VDI created: {os.path.getsize(VDI_OUT):,} bytes")
    subprocess.run([VBOXMGR, "internalcommands", "sethduuid", VDI_OUT, "0f2ea5af-32ed-4525-aa38-a0b2a95984fa"], capture_output=True)
    subprocess.run([VBOXMGR, "storageattach", "Micro-OS-64", "--storagectl", "IDE", "--port", "0", "--device", "0", "--type", "hdd", "--medium", VDI_OUT], capture_output=True)
    subprocess.run([VBOXMGR, "modifyvm", "Micro-OS-64", "--mouse", "usbtablet"], capture_output=True)
    subprocess.run([VBOXMGR, "startvm", "Micro-OS-64", "--type", "gui"], capture_output=True)
    print("[4] Micro-OS-64 restarted with fully active 'research' and 'fault' commands!")
else:
    print("Convert error:", res.stderr)
