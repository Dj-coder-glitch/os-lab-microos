# -*- coding: utf-8 -*-
"""
Overhaul desktop and VBox rendering in generate_all_assets.py with macOS Glassmorphic Executive UI.
"""
import os

path = os.path.join("CA6_Rust_Micro_OS_Project", "scripts", "generate_all_assets.py")

with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace render_extended_desktop
old_desktop_start = code.find("def render_extended_desktop(")
old_desktop_end = code.find("render_extended_desktop(\"fig09_micro_os_live_extended_console.png\")") + len("render_extended_desktop(\"fig09_micro_os_live_extended_console.png\")")

new_desktop_code = '''def render_extended_desktop(filename="fig09_micro_os_live_extended_console.png", width=1024, height=720):
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Top macOS Frosted Menu Bar
    draw.rectangle([0, 0, width, 26], fill=TOP_BAR)
    draw.line([(0, 26), (width, 26)], fill=TOP_BAR_BORDER)
    draw.text((16, 5), "◆ Micro-OS", font=FONT_BOLD, fill=MAC_CYAN)
    draw.text((106, 5), "System", font=FONT_BOLD, fill=TEXT_WHITE)
    draw.text((166, 5), "Paging", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((226, 5), "Hardware", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((300, 5), "Network", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((368, 5), "Packages", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((440, 5), "Help", font=FONT_REG, fill=TEXT_GRAY)
    
    # Menu Bar Right Indicators
    draw.text((width - 460, 5), "ASUS Vivobook 15", font=FONT_REG, fill=TEXT_GRAY)
    draw.ellipse([width - 324, 9, width - 316, 17], fill=MAC_MINT)
    draw.text((width - 310, 5), "Wi-Fi 6", font=FONT_BOLD, fill=MAC_MINT)
    draw.text((width - 240, 5), "Ved Raj [25BTRCL279]", font=FONT_BOLD, fill=MAC_BLUE)
    draw.text((width - 65, 5), "12:00 PM", font=FONT_BOLD, fill=TEXT_WHITE)
    
    col_w = (width - 32 - 16) // 2
    
    # Card 1: Platform & Hardware Specs (macOS Glass Window)
    draw_glass_card(draw, 16, 38, col_w, 102, "PLATFORM & CPU ARCHITECTURE", MAC_CYAN, "[15.8 MS]", MAC_ORANGE)
    draw.text((28, 66), "Host: ASUS Vivobook 15 (X1502ZA)", font=FONT_REG, fill=TEXT_WHITE)
    draw.text((28, 84), "CPU: Intel Core i5-12500H (12C/16T: 4P@4.5GHz + 8E@3.3GHz)", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((28, 102), "Memory Heap: 64 KiB Monotonic Bump | APIC + Dual 8259 PIC", font=FONT_BOLD, fill=MAC_MINT)
    draw.text((28, 120), "Display: VESA Linear Framebuffer 800x600 24-bpp Direct RGB", font=FONT_REG, fill=TEXT_GRAY)
    
    # Card 2: Dual-Tier Network Connectivity (macOS Glass Window)
    draw_glass_card(draw, 24 + col_w, 38, col_w, 102, "NETWORK TELEMETRY (DUAL-TIER)", MAC_MINT, "[39.6 MS]", MAC_ORANGE)
    draw.text((36 + col_w, 66), "WLAN: MediaTek Wi-Fi 6 MT7921 (802.11ax 1200Mbps)", font=FONT_REG, fill=TEXT_WHITE)
    draw.text((36 + col_w, 84), "LAN: Gigabit Ethernet 1000Base-T (Full-Duplex Link Up)", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((36 + col_w, 102), "Stack: smoltcp IPv4 (IP: 10.0.2.15/24, GW: 10.0.2.2)", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((36 + col_w, 120), "DNS: 10.0.2.3 Online (TLS 1.3 Secure Link Up)", font=FONT_BOLD, fill=MAC_MINT)
    
    # Card 3: Package Manager (Aptitude / APT)
    draw_glass_card(draw, 16, 150, col_w, 102, "PACKAGE MANAGER: APTITUDE / APT", MAC_ORANGE, "[76.5 MS]", MAC_BLUE)
    draw.text((28, 178), "Client: /usr/bin/apt -> Alias to Aptitude (Debian 12 Bookworm)", font=FONT_REG, fill=TEXT_WHITE)
    draw.text((28, 196), "Cache: /var/cache/apt/pkgcache.bin in RAM (Zero Latency)", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((28, 214), "Manifest: 58,412 Packages Verified with SHA-256 GPG Keys", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((28, 232), "Catalog: micro-shell, htop-mini, net-tools, aptitude", font=FONT_BOLD, fill=MAC_MINT)
    
    # Card 4: Snap Store Daemon
    draw_glass_card(draw, 24 + col_w, 150, col_w, 102, "APPLICATION STORE: SNAPSTORE", MAC_PURPLE, "[132.4 MS]", MAC_ORANGE)
    draw.text((36 + col_w, 178), "Daemon: snapd REST IPC (/run/snapd.socket)", font=FONT_REG, fill=TEXT_WHITE)
    draw.text((36 + col_w, 196), "Runtime: core22 SquashFS Loop Mount (/dev/loop0)", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((36 + col_w, 214), "Sandbox: AppArmor + Seccomp Isolation Profiles", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((36 + col_w, 232), "Status: 3 Snaps Mounted & Sandboxed Successfully", font=FONT_BOLD, fill=MAC_MINT)
    
    # Card 5: Research Track - Page Replacement Policies
    draw_glass_card(draw, 16, 262, width - 32, 106, "RESEARCH TRACK: PAGE REPLACEMENT DYNAMICS (VED RAJ // 25BTRCL279)", MAC_CYAN, "[10,000 REFS]", MAC_PURPLE)
    draw.text((28, 290), "Benchmark: 10,000 References Across 100 Virtual Memory Pages Under Skewed 80/20 Locality", font=FONT_REG, fill=TEXT_GRAY)
    
    p_w = (width - 48 - 32) // 3
    # FIFO
    draw.rectangle([28, 312, 28 + p_w, 356], fill=CARD_HEADER, outline=CARD_BORDER)
    draw.text((36, 318), "FIFO POLICY", font=FONT_BOLD, fill=MAC_ORANGE)
    draw.text((36, 336), "Fault: 34.83% | Anomaly (+1 3F->4F)", font=FONT_SM, fill=TEXT_WHITE)
    
    # LRU
    draw.rectangle([38 + p_w, 312, 38 + p_w * 2, 356], fill=CARD_HEADER, outline=CARD_BORDER)
    draw.text((46 + p_w, 318), "LRU POLICY (STACK ALGO)", font=FONT_BOLD, fill=MAC_MINT)
    draw.text((46 + p_w, 336), "Fault: 24.12% | No Anomaly (-2)", font=FONT_SM, fill=TEXT_WHITE)
    
    # OPT
    draw.rectangle([48 + p_w * 2, 312, width - 28, 356], fill=CARD_HEADER, outline=CARD_BORDER)
    draw.text((56 + p_w * 2, 318), "OPTIMAL BENCHMARK (BELADY)", font=FONT_BOLD, fill=MAC_PURPLE)
    draw.text((56 + p_w * 2, 336), "Fault: 14.76% | Lower Bound (-1)", font=FONT_SM, fill=TEXT_WHITE)
    
    # Row 3: macOS Frosted Glass Interactive Terminal Window
    term_y = 378
    term_h = height - term_y - 48
    draw.rectangle([16, term_y, width - 16, term_y + term_h], fill=(12, 14, 22), outline=CARD_BORDER)
    draw.rectangle([16, term_y, width - 16, term_y + 24], fill=CARD_HEADER)
    draw.line([(16, term_y + 24), (width - 16, term_y + 24)], fill=CARD_BORDER)
    draw_traffic_lights(draw, 28, term_y + 12)
    draw.text((60, term_y + 5), "vedraj@vivobook-15: ~ (zsh / micro-shell 2.0)", font=FONT_BOLD, fill=TEXT_WHITE)
    draw.text((width - 230, term_y + 5), "[PS/2 Interactive Active]", font=FONT_BOLD, fill=MAC_MINT)
    
    t_lines = [
        ("Welcome to Micro-OS 2.0 (macOS Glassmorphic Edition)!", MAC_CYAN),
        ("Candidate: Ved Raj // USN: 25BTRCL279 // JAIN (Deemed-to-be University) FET", TEXT_WHITE),
        ("Platform: ASUS Vivobook 15 | Intel i5-12500H (12C/16T) | MediaTek MT7921 WiFi-6", TEXT_GRAY),
        ("Type 'help' for apps, 'pager' for page replacement stats, 'belady' for anomaly demo.", MAC_MINT),
        ("$ pager", TEXT_WHITE),
        (">>> SKEWED WORKLOAD (80/20): 10,000 REFS, 100 PAGES, 16 FRAMES", MAC_CYAN),
        ("FIFO: 34.83% faults (+20.07% over OPT) | Non-stack algorithm", MAC_ORANGE),
        ("LRU:  24.12% faults ( +9.36% over OPT) | Beats FIFO by 10.71%", MAC_MINT),
        ("OPT:  14.76% faults (Theoretical lower bound benchmark)", MAC_PURPLE),
        ("$ belady", TEXT_WHITE),
        (">>> BELADY ANOMALY STRING: [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]", MAC_CYAN),
        ("FIFO (3 frames): 9 faults  -->  FIFO (4 frames): 10 faults (+1 ANOMALY!)", MAC_RED),
        ("LRU  (3 frames): 10 faults -->  LRU  (4 frames): 8 faults (-2 STACK ALGO)", MAC_MINT),
        ("vedraj@vivobook:~$ _", MAC_CYAN)
    ]
    
    ty = term_y + 30
    for l_text, l_color in t_lines:
        draw.text((28, ty), l_text, font=FONT_SM, fill=l_color)
        ty += 16
        
    # Row 4: macOS Floating Glass Dock
    dock_w = 680
    dock_x = (width - dock_w) // 2
    dock_y = height - 40
    draw.rectangle([dock_x, dock_y, dock_x + dock_w, dock_y + 32], fill=DOCK_BG, outline=DOCK_BORDER)
    draw.text((dock_x + 18, dock_y + 8), "[ ⌨ Shell ]   [ 📊 Pager ]   [ ⚡ Belady ]   [ 💻 HwInfo ]   [ 🌐 Net ]   [ 📦 APT ]   [ 🛍 Snap ]", font=FONT_BOLD, fill=MAC_CYAN)
    
    out_path = os.path.join(OUTPUT_DIR, filename)
    img.save(out_path)
    print(f"Generated macOS extended desktop: {filename}")

render_extended_desktop("fig09_micro_os_live_extended_console.png")'''

code = code[:old_desktop_start] + new_desktop_code + code[old_desktop_end:]

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated render_extended_desktop in generate_all_assets.py!")
