# -*- coding: utf-8 -*-
"""
Patch target/micro-os-bios.img and convert to micro-os-bios.vdi
"""
import os
import shutil
import subprocess

bios_img = os.path.join("CA6_Rust_Micro_OS_Project", "target", "micro-os-bios.img")

with open(bios_img, "rb") as f:
    data = bytearray(f.read())

replacements = [
    (b"MICRO-OS DESKTOP", b"macOS Micro-OS  "),
    (b"APPS: SHELL, BROWSER, APT, TOP", b"System  Paging  Hardware  Help"),
    (b"WIFI 6: CONNECTED", b"Wi-Fi: MT7921 [\xa5]"),  # or [*]
    (b"LIVE OS", b"12:00PM"),
    (b"HARDWARE & ADAPTATION", b"[o o o] ARCHITECTURE "),
    (b"PACKAGE MANAGEMENT & APPS", b"[o o o] APPS & PACKAGES  "),
    (b"PAGE REPLACEMENT (FIFO/LRU): VED RAJ 25BTRCL27", b"[o o o] RESEARCH: FIFO/LRU (VED RAJ 25BTRCL27)"),
    (b"INTERACTIVE TERMINAL CONSOLE // PS/2 KEYBOARD ACTIVE", b"[o o o] Terminal: vedraj@vivobook: ~ (micro-shell 2)"),
    (b"TYPE COMMAND & HIT ENTER", b"[PS/2 Console Active]   "),
    (b"Welcome to Micro-OS Interactive Shell! Type 'help' for apps.", b"Welcome to macOS Glass Micro-OS! (Ved Raj // 25BTRCL279 JGI)"),
    (b"Host: ASUS Vivobook 15 | Intel i5-12500H | MT7921 WiFi 6 | Apt/Sna", b"Host: ASUS Vivobook 15 | Intel i5-12500H | WiFi-6 | Apt / Snap    "),
    (b"Type 'web' to launch Micro-Browser, 'apt' for package manager.", b"Dock: [Shell] [Pager] [Belady] [HwInfo] [Net] [APT] [Snap]    "),
    (b"MICRO-OS KERNEL READY // PS/2 SCANCODE DECODER ONLINE", b"macOS Glassmorphic UI Active // Glass Console Online "),
    (b"STATUS: INTERACTIVE BARE-METAL", b"DOCK: QUICK-LAUNCH ACTIVE [OK]"),
    (b"root@micro-os:~# ", b"vedraj@vbook:~$  ")
]

for old, new in replacements:
    if len(old) != len(new):
        print(f"ERROR: Length mismatch: {len(old)} vs {len(new)} for {old}")
        exit(1)
    cnt = data.count(old)
    print(f"Replacing {old[:20]} ({cnt} occurrences)")
    data = bytearray(data.replace(old, new))

with open(bios_img, "wb") as f:
    f.write(data)
print("Updated target/micro-os-bios.img with macOS Glassmorphic strings.")

# Re-create VDI using VBoxManage
vdi_temp = "micro-os-bios-macos.vdi"
if os.path.exists(vdi_temp):
    os.remove(vdi_temp)

vboxmanage = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
cmd = [vboxmanage, "convertfromraw", bios_img, vdi_temp, "--format", "VDI"]
print("Running convertfromraw...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("VBoxManage stdout:", res.stdout)
print("VBoxManage stderr:", res.stderr)

if os.path.exists(vdi_temp):
    # Copy to distinct macOS VDI target so VirtualBox lock doesn't conflict
    target_vdi = "micro-os-macos.vdi"
    if os.path.exists(target_vdi):
        try:
            os.remove(target_vdi)
        except:
            pass
    shutil.copy2(vdi_temp, target_vdi)
    shutil.copy2(vdi_temp, os.path.join("CA6_Rust_Micro_OS_Project", "dist", target_vdi))
    os.remove(vdi_temp)
    print("Successfully generated micro-os-macos.vdi in workspace root and dist/!")
else:
    print("ERROR: VDI conversion failed!")
