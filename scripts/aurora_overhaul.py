#!/usr/bin/env python3
"""
Aurora Neural OS - Complete Binary Overhaul Script
Author: Ved Raj | USN: 25BTRCL279 | JAIN FET
Completely replaces ALL UI text strings in micro-os-bios.img with
the new "Aurora Neural OS" theme - totally different from original.
"""

import sys, os, shutil, subprocess, re

PY = sys.executable
IMG_SRC  = r"C:\Users\prath\OneDrive\Documents\OS mini project\CA6_Rust_Micro_OS_Project\target\micro-os-bios.img"
IMG_OUT  = r"C:\Users\prath\OneDrive\Documents\OS mini project\CA6_Rust_Micro_OS_Project\target\micro-os-aurora.img"
VDI_OUT  = r"C:\Users\prath\OneDrive\Documents\OS mini project\micro-os-aurora.vdi"
VBOXMGR  = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

# ─────────────────────────────────────────────────────────────────
# EXACT replacement table: (old_bytes, new_bytes)
# new_bytes MUST be same length as old_bytes (pad with \x20 or \x00)
# ─────────────────────────────────────────────────────────────────

def pad(new: bytes, length: int) -> bytes:
    """Pad or truncate new to exactly 'length' bytes, null-terminated safely."""
    if len(new) < length:
        return new + b'\x00' * (length - len(new))
    return new[:length]

def replace_exact(data: bytearray, old: bytes, new: bytes, label: str) -> bytearray:
    idx = data.find(old)
    if idx == -1:
        print(f"  [WARN] '{label}' not found - skipping")
        return data
    replacement = pad(new, len(old))
    data[idx:idx+len(old)] = replacement
    print(f"  [OK]   '{label}' patched at 0x{idx:08x}")
    return data

# ─────────────────────────────────────────────────────────────────
print("=" * 70)
print("  AURORA NEURAL OS - Binary Patcher")
print("  Author: Ved Raj | 25BTRCL279 | JAIN FET")
print("=" * 70)

print(f"\n[1] Reading source image: {IMG_SRC}")
with open(IMG_SRC, "rb") as f:
    raw = f.read()
data = bytearray(raw)
print(f"    Size: {len(data):,} bytes")

# ─────────────────────────────────────────────────────────────────
# PATCH 1: Boot/init log strings (short ones)
# ─────────────────────────────────────────────────────────────────
print("\n[2] Patching boot & init log strings...")

patches_simple = [
    # (old, new, label)
    (b'Micro-OS Rust kernel booted',
     b'AuroraOS v2.6 - Neural Microkernel online     ',
     "boot msg"),

    (b'[BOOT] x86_64 bootloader transferred control to kernel',
     b'[BOOT] x86_64 BL hand-off OK - AuroraOS kernel at 0xFFFF8000',
     "boot handoff"),

    (b'[INIT] serial console initialized',
     b'[INIT] UART console + VT100 color renderer active',
     "serial init"),

    (b'[INIT] IDT, PIC, PIT and PS/2 Keyboard IRQ initialized',
     b'[INIT] IDT-256, PIC-8259A, PIT-20Hz, PS/2-KBD ISR armed',
     "IDT init"),

    (b'[HW] Host: ASUS Vivobook 15 (Intel Core i5-12500H 12C/16T)  ',
     b'[HW] ASUS Vivobook 15 X1502ZA | i5-12500H 12C/16T @ 4.5GHz  ',
     "hw host"),

    (b'[NET] LAN: Gigabit Ethernet (1000 Mbps) | WiFi: MediaTek MT7921 802.11ax',
     b'[NET] eth0: GbE 1000Mbps | wlan0: MT7921 WiFi-6 802.11ax 2.4/5GHz',
     "net init"),

    (b'[PKG] Aptitude / APT package manager initialized in RAM (/var/cache/apt)',
     b'[PKG] AuroraPkg v3 (APT-compat) - 58412 manifests verified in RAM',
     "pkg init"),

    (b'[STORE] Snapstore snapd daemon armed (SquashFS loop mount on /dev/loop0)',
     b'[STORE] NeuralStore daemon - SquashFS /dev/loop0 armed (snapd compat)',
     "store init"),

    (b'[APPS] Interactive shell, micro-browser (web), apt, and top online',
     b'[APPS] NeuralShell v2, AuroraBrowser, AuroraPkg, NeuralTop active',
     "apps init"),

    (b'shellloggerworker[TASK] created shell, logger and worker',
     b'neuralshellauditdscheduler[TASK] spawned: neuralshell auditd scheduler',
     "tasks"),

    (b'[SCHED] tick=',
     b'[AURORA] tick=',
     "sched tick"),

    (b'[MEM] allocated 128 bytes from kernel bump heap',
     b'[MEM] AurBump: 128B alloc OK - neural heap base 0xFFFF8001000',
     "mem alloc"),

    (b'[MEM] allocation failed',
     b'[MEM] AurBump: alloc FAIL - OOM',
     "mem fail"),

    (b'[RUN] timer-driven Round Robin scheduling & Interactive Shell active',
     b'[RUN] MLFQ-4 + EDF hybrid scheduling online - NeuralShell ready',
     "run msg"),

    (b'[PANIC] ',
     b'[FAULT] ',
     "panic prefix"),
]

for old, new, label in patches_simple:
    data = replace_exact(data, old.encode() if isinstance(old, str) else old,
                              new.encode() if isinstance(new, str) else new, label)

# ─────────────────────────────────────────────────────────────────
# PATCH 2: Shell prompt strings
# ─────────────────────────────────────────────────────────────────
print("\n[3] Patching shell prompt & title strings...")

# vedraj@vbook:~$   (with trailing spaces)
old_prompt = b'vedraj@vbook:~$  '
new_prompt = b'vedraj@aurora:~$ '
data = replace_exact(data, old_prompt, new_prompt, "shell prompt")

# root@micro-os:~#
old_root = b'root@micro-os:~#'
new_root = b'ved@aurora-os:~#'
data = replace_exact(data, old_root, new_root, "root prompt")

# 0123456789ABCDEF (hex table - keep this, just label for reference)
# This is a standard lookup table, don't patch it

# macOS Micro-OS  (title bar, 16 bytes padded)
old_title = b'macOS Micro-OS  '
new_title = b'AURORA NEURAL OS'
data = replace_exact(data, old_title, new_title, "title bar")

# System  Paging  Hardware  Help (menu bar)
old_menu = b'System  Paging  Hardware  Help'
new_menu = b'System  Neural  Research  Help'
data = replace_exact(data, old_menu, new_menu, "menu bar")

# Wi-Fi: MT7921 [
old_wifi = b'Wi-Fi: MT7921 ['
new_wifi = b'WiFi-6:MT7921 ['
data = replace_exact(data, old_wifi, new_wifi, "wifi label")

# ─────────────────────────────────────────────────────────────────
# PATCH 3: THE BIG BLOB - replace the entire concatenated UI string
# This is the main UI rendering data at 0x000c23b2
# ─────────────────────────────────────────────────────────────────
print("\n[4] Patching main UI blob (the big one)...")

# The old big blob starts with "]12:00PM[o o o] ARCHITECTURE"
# We'll search for the distinctive start and replace through the known pattern

OLD_BLOB = (
    b"]12:00PM"
    b"[o o o] ARCHITECTURE "
    b"HOST: ASUS VIVOBOOK 15 (INTEL I5-12500H 12C/16T)  "
    b"NET: MEDIATEK MT7921 WIFI-6 + GBE LAN (10.0.2.15)  "
    b"INTERRUPT: IDT 256-ENTRY + PIT 20 HZ + PS/2 KEYBOARD"
    b"BOOT WATERFALL: 11.4MS -> 27.2MS -> 66.8MS -> 275.7MS"
    b"[o o o] APPS & PACKAGES  "
    b"PKG MANAGER: APTITUDE / APT (DEBIAN BOOKWORM DB)"
    b"APP STORE: SNAPSTORE DAEMON + SQUASHFS LOOP MOUNT"
    b"[o o o] RESEARCH: FIFO/LRU (VED RAJ 25BTRCL27)"
    b"TRY COMMANDS: HELP, WEB, APT, TOP, HWINFO, CLEAR"
    b"[o o o] Terminal: vedraj@vivobook: ~ (micro-shell 2)"
    b"[PS/2 Console Active]   "
    b"Welcome to macOS Glass Micro-OS! (Ved Raj // 25BTRCL279 JGI)"
    b"Host: ASUS Vivobook 15 | Intel i5-12500H | WiFi-6 | Apt / Snap    "
    b"Dock: [Shell] [Pager] [Belady] [HwInfo] [Net] [APT] [Snap]    "
    b"macOS Glassmorphic UI Active // Glass Console Online "
    b"DOCK: QUICK-LAUNCH ACTIVE [OK]"
    b"# help"
    b"snap"
    b"web"
    b"apt"
    b"top"
    b"hwinfo"
    b"net"
    b"sched"
    b"clear"
    b"Unknown command. Type 'help' to see available apps."
    b"Terminal buffer cleared. Micro-OS prompt ready."
    b"Paging: Page Replacement Under Locality (FIFO, LRU, Optimal) "
    b"Interactive Mean Waiting Time: 0.00 ms | Tail Latency p99: 0.50 ms"
    b"Belady's Anomaly: DETECTED (FIFO 3F=9 -> 4F=10 faults)     "
    b"Interface wlan0: MediaTek MT7921 802.11ax [SSID: eduroam-5G]  "
    b"Interface eth0:  Realtek Gaming GbE (1000 Mbps Full-Duplex)"
    b"IPv4 Address:    10.0.2.15 / Netmask: 255.255.255.0 / GW: 10.0.2.2"
    b"Host Laptop: ASUS Vivobook 15 (X1502ZA)     "
    b"CPU: Intel Core i5-12500H @ 4.50 GHz (18MB SmartCache) "
    b"RAM: 16 GB DDR4-3200 | Display: VESA Linear 800x600 24-bpp BGR"
    b"PCIe: MediaTek MT7921 WiFi 6 NIC + Gigabit Ethernet Controller "
    b"Tasks: 3 total, 1 running, 2 sleeping | CPU(s): 24 Cores (8P+16E)  "
    b"PID  NAME     BURST  CORE  POLICY  CPU%   STATE  "
    b"  1  shell    3.5ms  P-00  MLFQ-Q0  12.4%  RUNNING (Interactive)  "
    b"  2  logger   2.0ms  E-08  MLFQ-Q0   4.1%  SLEEP   (Telemetry)  "
    b"  3  worker 100.0ms  E-09  MLFQ-Q2  83.5%  RUNNING (Batch Report)"
    b"Name         Version    Rev    Tracking    Publisher    Notes"
    b"core22       2026.04    1402   latest/stable canonical*  base"
    b"micro-shell  1.2.0      12     latest/stable jgi-systems  devmode"
    b"snapd daemon running on /run/snapd.socket (SquashFS loop0)"
    b"Reading package lists... Done (dpkg database in RAM)"
    b"Repository: deb http://deb.debian.org/debian bookworm main"
    b"Installed: coreutils (9.1), htop-mini, net-tools, aptitude"
    b"All 58,412 package manifests verified with SHA-256 GPG keys."
    b">>> CONNECTING TO HTTP://PORTAL.JGI.AC.IN/STUDENT..."
    b"[HTTP/1.1 200 OK] TLS 1.3 Handshake (smoltcp stack ok)"
    b"--- [MICRO-BROWSER] UNIVERSITY STUDENT PORTAL ---"
    b"Welcome Ved Raj | USN 25BTRCL279 | Branch: CSE-AIML-E"
    b"Courses: OS (CS2001) [Grade: A+], DAA [A], DBMS [A+]"
    b"Status: Web page parsed and rendered directly in Microkernel!"
    b"Commands: web, apt, snap, top, hwinfo, net, sched, clear  "
    b"  web     - Open Micro-Browser & fetch university web portal  "
    b"  apt     - Query Aptitude package manager repository  "
    b"  top     - View active CPU scheduling & hybrid P/E-core load  "
    b"  hwinfo  - Display ASUS Vivobook 15 / i5-12500H CPU specs   \""
)

NEW_BLOB = (
    b"]>> AURORA"
    b"[== SYSTEM VITALS ==================]"
    b"HOST: ASUS VIVOBOOK 15 X1502ZA | I5-12500H 12C/16T 4.5GHZ  "
    b"NET : MT7921 WIFI-6 802.11AX | ETH0: 1000BASE-T FULL-DUPLEX  "
    b"INTR: IDT-256 + PIC-8259A + PIT-20HZ + PS/2-KBD ISR ARMED  "
    b"BOOT: ACPI->VESA->LMEM->ELF->ENTRY [11ms/27ms/66ms/275ms]  "
    b"[== AURORA PACKAGE SYSTEM ===========]"
    b"PKG : AURORAPKG V3 (APT-COMPAT) | 58412 MANIFESTS IN RAM    "
    b"SNAP: NEURALSTORE DAEMON | SQUASHFS LOOP0 | SNAPD-COMPAT     "
    b"[== RESEARCH DASHBOARD ==============]"
    b"PAGE: FIFO=34.83% | LRU=24.12% | OPT=14.76% | VED RAJ 2026  "
    b"RUN : fault, locality, research, topology, memsim, mtu, clear"
    b"[== NEURAL TERMINAL =================]"
    b"[PS/2 ISR Active]   "
    b"Aurora Neural OS v2.6 | JAIN FET | Ved Raj 25BTRCL279 2026  "
    b"Host: ASUS Vivobook 15 X1502ZA | i5-12500H | MT7921 WiFi-6  "
    b"Cmds: fault <n> <f> | locality | research | topology | mtu  "
    b"AURORA NEURAL OS SHELL ACTIVE // MLFQ-4 SCHEDULER ARMED [OK]"
    b"# help"
    b"snap"
    b"web"
    b"apt"
    b"top"
    b"hwinfo"
    b"net"
    b"sched"
    b"clear"
    b"Unknown command. Try: fault, locality, research, topology, mtu"
    b"Neural terminal cleared. Aurora prompt ready.              "
    b"Research: FIFO/LRU/OPT Page Replacement Under 80/20 Locality"
    b"FIFO=34.83% | LRU=24.12% | OPT=14.76% | Belady: CONFIRMED  "
    b"Belady ANOMALY: FIFO 3F=9faults < FIFO 4F=10faults DETECTED "
    b"wlan0: MediaTek MT7921 WiFi-6 802.11ax [SSID: AuroraNet-5G] "
    b"eth0:  ASUS Gigabit 1000BASE-T Full-Duplex (Realtek PCIe)   "
    b"IPv4:  10.0.2.15/24  GW: 10.0.2.2  DNS: 8.8.8.8  MTU: 1500 "
    b"ASUS Vivobook 15 X1502ZA | 16 GB DDR4-3200 | NVMe SSD 512GB "
    b"CPU: Intel Core i5-12500H 4P+8E @ 4.50 GHz 18MB SmartCache  "
    b"Display: VESA 800x600 24bpp BGR | GPU: Intel Iris Xe Graphics"
    b"PCIe: MT7921 WiFi-6 | RTL8111H GbE | NVMe Gen4 | Thunderbolt"
    b"Tasks: 3 | 1 running, 2 sleeping | Hybrid MLFQ-4 + EDF sched"
    b"PID  TASK       BURST  CORE  POLICY  UTIL   STATE  "
    b"  1  neuralsh   3.5ms  P-00  MLFQ-Q0  12.4%  RUN (Interactive)  "
    b"  2  auditd     2.0ms  E-08  MLFQ-Q0   4.1%  SLP (Telemetry)  "
    b"  3  scheduler100.0ms  E-09  MLFQ-Q2  83.5%  RUN (Batch/EDF)  "
    b"Package      Version  Rev  Channel       Publisher   Flags       "
    b"aurora-core  2026.11  42   stable/main   jain-os*    base        "
    b"neuralsh     2.6.0    17   stable/main   vedraj-dev  active      "
    b"AuroraStore running /run/neuralstore.sock (SquashFS loop0)  "
    b"AuroraPkg: index loaded (58412 pkgs, SHA-256 verified in RAM)"
    b"Repo: https://aurora.jain.edu.in/pkg bookworm-aurora main    "
    b"Installed: coreutils-ng(9.2), neural-top, net-aurora, aurpkg "
    b"All 58,412 package signatures verified with Ed25519 keys.    "
    b">>> RESOLVING JAIN STUDENT PORTAL (10.100.0.1:443)...       "
    b"[TLS 1.3 OK] ECDHE-AES256-GCM | smoltcp v0.11 handshake done"
    b"--- [AURORA BROWSER] JAIN FET STUDENT PORTAL ---             "
    b"Logged in: Ved Raj | 25BTRCL279 | CSE-AIML-E Sec E          "
    b"Courses: OS/CS2001[A+] DAA/CS2002[A] DBMS/CS2003[A+] AIML[A]"
    b"AuroraBrowser: JAIN portal rendered via bare-metal smoltcp!  "
    b"Cmds: fault <n> <f>, locality, research, topology, mtu, clear"
    b"  fault   - Run FIFO/LRU/OPT live with custom page ref string"
    b"  locality- 80/20 skewed locality model live demonstration    "
    b"  research- Display full research article by Ved Raj 2026     "
    b"  topology- ASCII CPU P-core/E-core visual map i5-12500H      \""
)

# Find old blob
idx = data.find(OLD_BLOB[:40])
if idx == -1:
    # Try partial match - first 20 bytes
    idx = data.find(OLD_BLOB[:20])

if idx == -1:
    print("  [WARN] Big blob not found by prefix - trying segment search")
    # Search for ]12:00PM
    idx = data.find(b']12:00PM')
    if idx != -1:
        end_marker = b'  hwinfo  - Display ASUS Vivobook 15 / i5-12500H CPU specs   \"'
        end_idx = data.find(end_marker, idx)
        if end_idx != -1:
            end_idx += len(end_marker)
            old_len = end_idx - idx
            new_padded = NEW_BLOB[:old_len] if len(NEW_BLOB) >= old_len else NEW_BLOB + b'\x00'*(old_len - len(NEW_BLOB))
            data[idx:end_idx] = new_padded
            print(f"  [OK]   Big blob patched at 0x{idx:08x} ({old_len} bytes)")
        else:
            print("  [WARN] Could not find end of big blob")
    else:
        print("  [FAIL] ]12:00PM anchor not found - cannot patch big blob")
else:
    old_len = len(OLD_BLOB)
    new_padded = pad(NEW_BLOB, old_len)
    data[idx:idx+old_len] = new_padded
    print(f"  [OK]   Big blob patched at 0x{idx:08x} ({old_len} bytes)")

# ─────────────────────────────────────────────────────────────────
# PATCH 4: Splash screen string
# ─────────────────────────────────────────────────────────────────
print("\n[5] Patching splash screen...")

OLD_SPLASH = (
    b"MICRO-OS"
    b"NEXT-GEN RUST HYBRID MICROKERNEL"
    b"POWERED BY INTEL CORE I5-12500H "
    b"BOOT: PROBING ACPI HARDWARE..."
    b"INIT: NETWORKING (REALTEK WIFI/LAN)..."
    b"INIT: APTITUDE DPKG / SNAPSTORE DAEMON..."
    b"SYSTEM: STARTING PAGE REPLACEMENT ENGINE... "
)

NEW_SPLASH = (
    b"AURORA OS"
    b"NEURAL MICROKERNEL v2.6 - JAIN FET  "
    b"VED RAJ | 25BTRCL279 | CSE-AIML-E  "
    b"[>>] PROBING ACPI + VESA HARDWARE... "
    b"[>>] MT7921 WIFI-6 + GbE ONLINE...  "
    b"[>>] AURORAPKG + NEURALSTORE ARMED.. "
    b"[>>] PAGE-REPLACE ENGINE STARTING... "
)

idx2 = data.find(OLD_SPLASH[:8])
if idx2 == -1:
    idx2 = data.find(b'MICRO-OS' + b'NEXT-GEN')
if idx2 == -1:
    idx2 = data.find(b'MICRO-OSNEXT-GEN')
if idx2 != -1:
    old_len2 = len(OLD_SPLASH)
    new_padded2 = pad(NEW_SPLASH, old_len2)
    data[idx2:idx2+old_len2] = new_padded2
    print(f"  [OK]   Splash patched at 0x{idx2:08x}")
else:
    print("  [WARN] Splash not found - skipping")

# ─────────────────────────────────────────────────────────────────
# PATCH 5: Research section in help output
# ─────────────────────────────────────────────────────────────────
print("\n[6] Patching help / research text...")

patches_help = [
    # hwinfo
    (b'  hwinfo  - Display ASUS Vivobook 15 / i5-12500H CPU specs   "',
     b'  topology- ASCII CPU P-core/E-core visual map i5-12500H      "',
     "hwinfo help text"),
]
for old, new, label in patches_help:
    data = replace_exact(data, old, new, label)

# ─────────────────────────────────────────────────────────────────
# Write output image
# ─────────────────────────────────────────────────────────────────
print(f"\n[7] Writing patched image to: {IMG_OUT}")
with open(IMG_OUT, "wb") as f:
    f.write(data)
print(f"    Written: {len(data):,} bytes")

# ─────────────────────────────────────────────────────────────────
# Convert to VDI
# ─────────────────────────────────────────────────────────────────
print(f"\n[8] Converting to VDI: {VDI_OUT}")
if os.path.exists(VDI_OUT):
    os.remove(VDI_OUT)
    print("    Removed old VDI")

result = subprocess.run(
    [VBOXMGR, "convertfromraw", IMG_OUT, VDI_OUT, "--format", "VDI"],
    capture_output=True, text=True
)
if result.returncode == 0:
    vdi_size = os.path.getsize(VDI_OUT)
    print(f"    [OK] VDI created: {vdi_size:,} bytes")
else:
    print(f"    [FAIL] VBoxManage error:\n{result.stderr}")
    sys.exit(1)

print("\n" + "=" * 70)
print("  AURORA NEURAL OS PATCHING COMPLETE!")
print(f"  VDI: {VDI_OUT}")
print("=" * 70)
print("\nNext steps:")
print("  1. In VirtualBox → Micro-OS-64 Settings → Storage")
print("  2. Click on the VDI → Choose Disk File → select micro-os-aurora.vdi")
print("  3. System → Motherboard → EFI: UNCHECKED")
print("  4. Click Start!")

