import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def render_terminal_video(output_path, width=1280, height=720, fps=24):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, float(fps), (width, height))

    font_path = "C:/Windows/Fonts/consola.ttf"
    font_bold_path = "C:/Windows/Fonts/consolab.ttf"
    
    font_small = ImageFont.truetype(font_path, 15)
    font_code = ImageFont.truetype(font_path, 17)
    font_bold = ImageFont.truetype(font_bold_path, 18)
    font_title = ImageFont.truetype(font_bold_path, 22)
    font_huge = ImageFont.truetype(font_bold_path, 28)

    # Colors
    bg_color = (13, 17, 23)        # Dark slate
    bar_color = (22, 27, 34)       # Window bar
    text_color = (230, 237, 243)   # Off white
    cyan_color = (88, 166, 255)    # Blue/Cyan
    green_color = (63, 185, 80)    # Success green
    red_color = (248, 81, 73)      # Alert red
    yellow_color = (210, 153, 34)  # Warning yellow
    gray_color = (139, 148, 158)   # Comment gray
    prompt_color = (219, 97, 162)  # Pink/Purple prompt

    def draw_window_frame(draw):
        # Top title bar
        draw.rectangle([0, 0, width, 42], fill=bar_color)
        draw.line([0, 42, width, 42], fill=(48, 54, 61), width=1)
        
        # Window buttons (mac/terminal style)
        draw.ellipse([16, 14, 28, 26], fill=(255, 95, 86))
        draw.ellipse([36, 14, 48, 26], fill=(255, 189, 46))
        draw.ellipse([56, 14, 68, 26], fill=(39, 201, 63))

        # Title
        title_text = "DevPulse AI Terminal -- aastha@devpulse-workstation: ~/DevPulse-AI"
        draw.text((width // 2 - 250, 12), title_text, font=font_small, fill=gray_color)

    frames = []

    # Helper to push a static state for N frames
    def hold_frame(lines_generator, count=15):
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        draw_window_frame(draw)
        lines_generator(draw)
        frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        for _ in range(count):
            out.write(frame_cv)

    # SCENE 1: Writing / Inspecting vulnerable code in VS Code / Editor (0 - 4s)
    code_lines = [
        ("# File: auth_service_vulnerable.py (Human Developer Writing Code)", gray_color),
        ("import os, sqlite3, hashlib, pickle", text_color),
        ("", text_color),
        ("# 🚨 FLAW 1: Hardcoded AWS Secret Key", red_color),
        ('AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"', yellow_color),
        ("", text_color),
        ("# 🚨 FLAW 2: Insecure MD5 Password Hashing", red_color),
        ("def hash_password(p): return hashlib.md5(p.encode()).hexdigest()", text_color),
        ("", text_color),
        ("# 🚨 FLAW 3: SQL Injection Vulnerability", red_color),
        ('query = f"SELECT * FROM users WHERE user=\'{username}\' AND pass=\'{pwd}\'"', yellow_color),
        ("cursor.execute(query)", text_color),
        ("", text_color),
        ("# 🚨 FLAW 4: Remote Code Execution (RCE)", red_color),
        ('os.system("ping -c 1 " + user_input_host)', yellow_color),
    ]

    for show_count in range(1, len(code_lines) + 1):
        def render_code(draw, count=show_count):
            draw.text((30, 60), "[1] DEVELOPER WRITING VULNERABLE CODE (auth_service_vulnerable.py):", font=font_bold, fill=cyan_color)
            y = 100
            for idx in range(count):
                txt, col = code_lines[idx]
                draw.text((40, y), txt, font=font_code, fill=col)
                y += 24
            # Cursor
            draw.rectangle([40, y, 50, y + 18], fill=cyan_color)

        hold_frame(render_code, count=4)

    # Hold code scene
    def render_code_full(draw):
        draw.text((30, 60), "[1] DEVELOPER WRITING VULNERABLE CODE (auth_service_vulnerable.py):", font=font_bold, fill=cyan_color)
        y = 100
        for txt, col in code_lines:
            draw.text((40, y), txt, font=font_code, fill=col)
            y += 24
    hold_frame(render_code_full, count=36) # 1.5s hold

    # SCENE 2: Terminal typing command (4s - 8s)
    cmd_text = "python scan.py auth_service_vulnerable.py"
    for i in range(1, len(cmd_text) + 1):
        typed_cmd = cmd_text[:i]
        def render_typing(draw, typed=typed_cmd):
            draw.text((30, 60), "[2] OPENING TERMINAL & AUDITING SOURCE CODE:", font=font_bold, fill=cyan_color)
            draw.text((40, 110), "aastha@laptop:~/DevPulse-AI$ ", font=font_bold, fill=prompt_color)
            draw.text((310, 110), typed, font=font_code, fill=text_color)
            draw.rectangle([310 + len(typed) * 10, 110, 310 + len(typed) * 10 + 9, 128], fill=text_color)
        hold_frame(render_typing, count=2)

    # Press Enter - Scan Starting
    def render_scan_starting(draw):
        draw.text((30, 60), "[2] OPENING TERMINAL & AUDITING SOURCE CODE:", font=font_bold, fill=cyan_color)
        draw.text((40, 110), "aastha@laptop:~/DevPulse-AI$ ", font=font_bold, fill=prompt_color)
        draw.text((310, 110), cmd_text, font=font_code, fill=text_color)
        draw.text((40, 150), "[*] DevPulse AI Engine Initializing...", font=font_code, fill=yellow_color)
        draw.text((40, 175), "[*] Scanning 'auth_service_vulnerable.py' (48 lines) against OWASP Top 10 rules...", font=font_code, fill=cyan_color)
    hold_frame(render_scan_starting, count=25)

    # SCENE 3: Audit Results (Score 27.0 - CRITICAL RISK) (8s - 16s)
    def render_audit_results(draw):
        draw.text((30, 55), "[3] LIVE SECURITY AUDIT REPORT DETECTED:", font=font_bold, fill=red_color)
        draw.text((40, 90), "aastha@laptop:~/DevPulse-AI$ python scan.py auth_service_vulnerable.py", font=font_code, fill=gray_color)
        
        # Red Score Box
        draw.rectangle([40, 120, 1240, 210], fill=(40, 15, 18), outline=red_color, width=2)
        draw.text((60, 132), "SECURITY SCORE: 27.0 / 100", font=font_huge, fill=red_color)
        draw.text((60, 172), "RISK LEVEL: CRITICAL RISK (BLOCK PR)  |  TOTAL ISSUES: 4 (Critical: 2, High: 1, Med: 1)", font=font_bold, fill=(255, 120, 120))

        # Detected flaws
        y = 230
        draw.text((40, y), "DETECTED VULNERABILITIES & AI FIX RECOMMENDATIONS:", font=font_bold, fill=text_color)
        
        flaws = [
            ("[Severity.CRITICAL] SEC-001: Hardcoded AWS Secret Key (Line 7)", red_color,
             " -> Fix: AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')"),
            ("[Severity.CRITICAL] SEC-002: SQL Injection via String Formatting (Line 28)", red_color,
             " -> Fix: cursor.execute('SELECT * FROM users WHERE user=%s', (username,))"),
            ("[Severity.CRITICAL] SEC-003: Remote Code Execution RCE in os.system (Line 38)", red_color,
             " -> Fix: subprocess.run(['ping', '-c', '1', host], check=True)"),
            ("[Severity.MEDIUM]   SEC-006: Broken Cryptographic Hash MD5 (Line 16)", yellow_color,
             " -> Fix: hashlib.sha256(password.encode()).hexdigest()")
        ]

        y = 265
        for header, col, fix in flaws:
            draw.text((40, y), header, font=font_code, fill=col)
            draw.text((60, y + 22), fix, font=font_code, fill=green_color)
            y += 52

        # Status badge
        draw.rectangle([40, 485, 450, 520], fill=(60, 15, 20), outline=red_color, width=1)
        draw.text((55, 493), "🚨 PR MERGE BLOCKED: Vulnerabilities must be resolved!", font=font_bold, fill=red_color)

    hold_frame(render_audit_results, count=96) # 4 seconds hold

    # SCENE 4: Applying 1-Click Fix & Re-auditing (Clean 100/100) (16s - 22s)
    clean_cmd = "python scan.py clean_test.py"
    def render_clean_audit(draw):
        draw.text((30, 55), "[4] DEVELOPER APPLIES AI REMEDIATION & RE-SCANS:", font=font_bold, fill=green_color)
        draw.text((40, 95), "aastha@laptop:~/DevPulse-AI$ " + clean_cmd, font=font_bold, fill=text_color)
        
        # Green Score Box
        draw.rectangle([40, 130, 1240, 220], fill=(15, 40, 25), outline=green_color, width=2)
        draw.text((60, 142), "SECURITY SCORE: 100.0 / 100", font=font_huge, fill=green_color)
        draw.text((60, 182), "RISK LEVEL: LOW RISK (PASS)  |  TOTAL ISSUES: 0 (All CWE checks clean)", font=font_bold, fill=(120, 255, 160))

        y = 245
        draw.text((40, y), "[+] AUDIT SUMMARY:", font=font_bold, fill=text_color)
        y += 30
        draw.text((40, y), "  [OK] CWE-798: No leaked credentials found (Environment variables used)", font=font_code, fill=green_color)
        y += 26
        draw.text((40, y), "  [OK] CWE-89:  SQL queries properly parameterized with bind tuples", font=font_code, fill=green_color)
        y += 26
        draw.text((40, y), "  [OK] CWE-94:  Zero unsafe os.system() or eval() executions", font=font_code, fill=green_color)
        y += 26
        draw.text((40, y), "  [OK] CWE-327: SHA-256 cryptographic hashing verified", font=font_code, fill=green_color)
        y += 40

        draw.rectangle([40, y, 480, y + 36], fill=(15, 50, 30), outline=green_color, width=1)
        draw.text((55, y + 8), "✅ PR READY TO MERGE: Passed all security gates!", font=font_bold, fill=green_color)

    hold_frame(render_clean_audit, count=96) # 4 seconds hold

    # SCENE 5: Outro Portfolio Slide (22s - 25s)
    def render_outro(draw):
        draw.rectangle([0, 42, width, height], fill=(10, 14, 22))
        
        draw.text((width // 2 - 280, 150), "DevPulse AI -- Autonomous Security Auditor", font=font_huge, fill=cyan_color)
        draw.text((width // 2 - 240, 210), "Real-Time OWASP Static Code Reviewer & PR Bot", font=font_title, fill=text_color)
        
        # Attribution Card
        draw.rectangle([width // 2 - 320, 270, width // 2 + 320, 480], fill=bar_color, outline=(48, 54, 61), width=2)
        draw.text((width // 2 - 280, 300), "Lead Developer : Aastha Rawat", font=font_bold, fill=green_color)
        draw.text((width // 2 - 280, 340), "GitHub Repo    : github.com/aastharawat47849-oss/DevPulse-AI", font=font_code, fill=text_color)
        draw.text((width // 2 - 280, 380), "Live Cloud UI  : aastharawat47849-oss.github.io/DevPulse-AI/", font=font_code, fill=cyan_color)
        draw.text((width // 2 - 280, 420), "CLI Command    : python scan.py <file.py> (Zero Setup Required)", font=font_code, fill=yellow_color)

        draw.text((width // 2 - 160, 540), "Open Source | MIT Licensed | 2026", font=font_small, fill=gray_color)

    hold_frame(render_outro, count=72) # 3 seconds hold

    out.release()
    print(f"Video generated successfully at: {output_path}")

if __name__ == "__main__":
    vid_file = r"C:\Users\B-WOI\Videos\DevPulse_AI_Live_Terminal_Audit_Demo.mp4"
    render_terminal_video(vid_file)
