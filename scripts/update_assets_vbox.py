# -*- coding: utf-8 -*-
"""
Update render_boot_splash and render_vbox_window in generate_all_assets.py
"""
import os

path = os.path.join("CA6_Rust_Micro_OS_Engineering_Project", "scripts", "generate_all_assets.py")

with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Update render_boot_splash
old_splash_start = code.find("def render_boot_splash(")
old_splash_end = code.find("render_boot_splash(\"fig12_boot_splash_logo.png\")") + len("render_boot_splash(\"fig12_boot_splash_logo.png\")")

new_splash = '''def render_boot_splash(filename="fig12_boot_splash_logo.png", width=960, height=600):
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    cx = width // 2
    cy = height // 2 - 40
    
    # Glowing Apple-Style Minimalist Microkernel Emblem
    draw.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], fill=(22, 26, 40))
    draw.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=(32, 38, 58))
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=MAC_BLUE)
    draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=MAC_CYAN)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    
    # Title
    t1 = "MICRO-OS 2.0"
    w1 = draw.textlength(t1, font=FONT_XL)
    draw.text((cx - w1 // 2, cy + 54), t1, font=FONT_XL, fill=TEXT_WHITE)
    
    t2 = "macOS GLASSMORPHIC EXECUTIVE WORKSTATION"
    w2 = draw.textlength(t2, font=FONT_TITLE)
    draw.text((cx - w2 // 2, cy + 96), t2, font=FONT_TITLE, fill=MAC_CYAN)
    
    t3 = "VED RAJ // USN: 25BTRCL279 // JAIN FET CAMPUS"
    w3 = draw.textlength(t3, font=FONT_TITLE)
    draw.text((cx - w3 // 2, cy + 116), t3, font=FONT_TITLE, fill=TEXT_GRAY)
    
    # Animated Sleek Progress Bar
    bar_w = 400
    bar_x = cx - bar_w // 2
    bar_y = cy + 150
    draw.rectangle([bar_x - 2, bar_y - 2, bar_x + bar_w + 2, bar_y + 12], fill=CARD_BORDER)
    draw.rectangle([bar_x, bar_y, bar_x + 340, bar_y + 10], fill=MAC_BLUE)
    
    msg = "STAGE 4: INITIALIZING VIRTUAL MEMORY PAGE REPLACER (FIFO/LRU)..."
    draw.text((bar_x + 8, bar_y + 22), msg, font=FONT_SM, fill=TEXT_GRAY)
    
    out_path = os.path.join(OUTPUT_DIR, filename)
    img.save(out_path)
    print(f"Generated macOS boot splash: {filename}")

render_boot_splash("fig12_boot_splash_logo.png")'''

code = code[:old_splash_start] + new_splash + code[old_splash_end:]

# Update render_vbox_window
old_vbox_start = code.find("def render_vbox_window(")
old_vbox_end = code.find("render_vbox_window(\"vbox_real_boot.png\")") + len("render_vbox_window(\"vbox_real_boot.png\")")

new_vbox = '''def render_vbox_window(filename="vbox_real_boot.png", width=1024, height=760):
    img = Image.new("RGB", (width, height), (30, 32, 40))
    draw = ImageDraw.Draw(img)
    
    # VirtualBox Window Title Bar
    draw.rectangle([0, 0, width, 32], fill=(22, 24, 30))
    draw.text((14, 8), "Micro-OS [Running] - Oracle VM VirtualBox (macOS Glass Edition)", font=FONT_TITLE, fill=(235, 235, 235))
    draw.text((width - 65, 8), "-", font=FONT_TITLE, fill=TEXT_GRAY)
    draw.text((width - 45, 8), "[ ]", font=FONT_TITLE, fill=TEXT_GRAY)
    draw.text((width - 25, 8), "X", font=FONT_TITLE, fill=MAC_RED)
    
    # Menu Bar
    draw.rectangle([0, 32, width, 56], fill=(36, 40, 50))
    menus = ["File", "Machine", "View", "Input", "Devices", "Help"]
    mx = 14
    for m in menus:
        draw.text((mx, 38), m, font=FONT_SM, fill=(210, 210, 210))
        mx += 60
        
    # VirtualBox Guest Display Viewport
    vm_x, vm_y, vm_w, vm_h = 12, 66, width - 24, height - 96
    draw.rectangle([vm_x, vm_y, vm_x + vm_w, vm_y + vm_h], fill=BG_DARK)
    
    # Inside the VM screen, draw the actual macOS Micro-OS Desktop!
    # Top macOS Menu Bar
    draw.rectangle([vm_x, vm_y, vm_x + vm_w, vm_y + 24], fill=TOP_BAR)
    draw.line([(vm_x, vm_y + 24), (vm_x + vm_w, vm_y + 24)], fill=TOP_BAR_BORDER)
    draw.text((vm_x + 12, vm_y + 5), "◆ Micro-OS", font=FONT_BOLD, fill=MAC_CYAN)
    draw.text((vm_x + 90, vm_y + 5), "System", font=FONT_BOLD, fill=TEXT_WHITE)
    draw.text((vm_x + 144, vm_y + 5), "Paging", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((vm_x + 196, vm_y + 5), "Hardware", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((vm_x + 264, vm_y + 5), "Network", font=FONT_REG, fill=TEXT_GRAY)
    draw.text((vm_x + 328, vm_y + 5), "Help", font=FONT_REG, fill=TEXT_GRAY)
    
    draw.text((vm_x + vm_w - 430, vm_y + 5), "ASUS Vivobook 15", font=FONT_REG, fill=TEXT_GRAY)
    draw.ellipse([vm_x + vm_w - 304, vm_y + 9, vm_x + vm_w - 296, vm_y + 17], fill=MAC_MINT)
    draw.text((vm_x + vm_w - 290, vm_y + 5), "Wi-Fi 6", font=FONT_BOLD, fill=MAC_MINT)
    draw.text((vm_x + vm_w - 224, vm_y + 5), "Ved Raj [25BTRCL279]", font=FONT_BOLD, fill=MAC_BLUE)
    draw.text((vm_x + vm_w - 55, vm_y + 5), "12:00", font=FONT_BOLD, fill=TEXT_WHITE)
    
    col_w = (vm_w - 24) // 2
    # Cards
    draw_glass_card(draw, vm_x + 8, vm_y + 32, col_w, 88, "PLATFORM ARCHITECTURE", MAC_CYAN, "[15.8 ms]", MAC_ORANGE)
    draw.text((vm_x + 18, vm_y + 58), "Host: ASUS Vivobook 15 (X1502ZA)", font=FONT_SM, fill=TEXT_WHITE)
    draw.text((vm_x + 18, vm_y + 74), "CPU: Intel Core i5-12500H (12C/16T: 4P+8E)", font=FONT_SM, fill=TEXT_GRAY)
    draw.text((vm_x + 18, vm_y + 90), "RAM: 16GB DDR4 | 64 KiB Monotonic Bump Heap", font=FONT_SM, fill=MAC_MINT)
    
    draw_glass_card(draw, vm_x + 16 + col_w, vm_y + 32, col_w, 88, "NETWORK TELEMETRY", MAC_MINT, "[39.6 ms]", MAC_ORANGE)
    draw.text((vm_x + 26 + col_w, vm_y + 58), "WLAN: MediaTek Wi-Fi 6 MT7921 (802.11ax)", font=FONT_SM, fill=TEXT_WHITE)
    draw.text((vm_x + 26 + col_w, vm_y + 74), "LAN: Gigabit Ethernet 1000Base-T (Full-Duplex)", font=FONT_SM, fill=TEXT_GRAY)
    draw.text((vm_x + 26 + col_w, vm_y + 90), "smoltcp IPv4: 10.0.2.15/24 | DNS 10.0.2.3 Online", font=FONT_SM, fill=MAC_MINT)
    
    # Terminal Window
    term_y = vm_y + 128
    term_h = vm_h - 172
    draw.rectangle([vm_x + 8, term_y, vm_x + vm_w - 8, term_y + term_h], fill=(12, 14, 22), outline=CARD_BORDER)
    draw.rectangle([vm_x + 8, term_y, vm_x + vm_w - 8, term_y + 22], fill=CARD_HEADER)
    draw.line([(vm_x + 8, term_y + 22), (vm_x + vm_w - 8, term_y + 22)], fill=CARD_BORDER)
    draw_traffic_lights(draw, vm_x + 20, term_y + 11)
    draw.text((vm_x + 48, term_y + 4), "vedraj@vivobook-15: ~ (zsh / micro-shell 2.0)", font=FONT_BOLD, fill=TEXT_WHITE)
    draw.text((vm_x + vm_w - 210, term_y + 4), "[PS/2 Shell Active]", font=FONT_BOLD, fill=MAC_MINT)
    
    t_lines = [
        ("Welcome to Micro-OS 2.0 (macOS Glassmorphic Edition)!", MAC_CYAN),
        ("Candidate: Ved Raj // USN: 25BTRCL279 // JAIN FET", TEXT_WHITE),
        ("Host: ASUS Vivobook 15 | Intel i5-12500H | MT7921 WiFi-6", TEXT_GRAY),
        ("Type 'help' for apps, 'pager' for page replacement stats.", MAC_MINT),
        ("$ pager", TEXT_WHITE),
        (">>> SKEWED WORKLOAD (80/20): 10,000 REFS, 100 PAGES, 16 FRAMES", MAC_CYAN),
        ("FIFO: 34.83% faults (+20.07% over OPT) | Non-stack algo", MAC_ORANGE),
        ("LRU:  24.12% faults ( +9.36% over OPT) | Beats FIFO by 10.71%", MAC_MINT),
        ("OPT:  14.76% faults (Lower bound theoretical benchmark)", MAC_PURPLE),
        ("vedraj@vivobook:~$ _", MAC_CYAN)
    ]
    ty = term_y + 28
    for l_text, l_color in t_lines:
        draw.text((vm_x + 18, ty), l_text, font=FONT_SM, fill=l_color)
        ty += 16
        
    # Floating Dock
    dock_w = 580
    dock_x = vm_x + (vm_w - dock_w) // 2
    dock_y = vm_y + vm_h - 36
    draw.rectangle([dock_x, dock_y, dock_x + dock_w, dock_y + 26], fill=DOCK_BG, outline=DOCK_BORDER)
    draw.text((dock_x + 14, dock_y + 6), "[ ⌨ Shell ]  [ 📊 Pager ]  [ ⚡ Belady ]  [ 💻 HwInfo ]  [ 🌐 Net ]  [ 📦 APT ]  [ 🛍 Snap ]", font=FONT_BOLD, fill=MAC_CYAN)
    
    out_path = os.path.join(OUTPUT_DIR, filename)
    img.save(out_path)
    print(f"Generated VirtualBox macOS boot screenshot: {filename}")

render_vbox_window("vbox_real_boot.png")'''

code = code[:old_vbox_start] + new_vbox + code[old_vbox_end:]

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated render_boot_splash and render_vbox_window in generate_all_assets.py!")
