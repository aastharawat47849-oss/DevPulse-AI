import sys
import os
from app.models.audit import CodeScanRequest
from app.services.security_engine import SecurityEngine

def main():
    """
    DevPulse AI CLI Tool for local terminal security auditing.
    Usage: devpulse scan <file_path>
    """
    args = sys.argv[1:]
    if not args or args[0] != "scan":
        print("[+] DevPulse AI -- Autonomous Code Security Auditor")
        print("Usage: devpulse scan <file_path>")
        print("Example: devpulse scan main.py")
        sys.exit(0)

    target_file = args[1] if len(args) > 1 else "main.py"
    
    if not os.path.exists(target_file):
        print(f"[-] Error: File '{target_file}' not found!")
        sys.exit(1)

    with open(target_file, "r", encoding="utf-8") as f:
        code_content = f.read()

    print(f"\n[*] DevPulse AI Auditing File: '{target_file}'...")
    request = CodeScanRequest(file_name=target_file, code_content=code_content)
    result = SecurityEngine.scan_code(request)

    print("=" * 60)
    print(f"SECURITY SCORE: {result.security_score} / 100")
    print(f"RISK LEVEL: {result.risk_level}")
    print(f"TOTAL ISSUES: {result.total_issues} (Critical: {result.critical_count}, High: {result.high_count})")
    print("=" * 60)

    if result.vulnerabilities:
        print("\nDETECTED VULNERABILITIES:")
        for v in result.vulnerabilities:
            print(f"\n[{v.severity}] {v.rule_name} (Line {v.line_number})")
            print(f" Category: {v.category}")
            print(f" Vulnerable Code: {v.vulnerable_code}")
            print(f" AI Suggested Fix:\n{v.ai_suggested_fix}")
    else:
        print("\n[+] No security vulnerabilities detected! Code is clean.")

if __name__ == "__main__":
    main()
