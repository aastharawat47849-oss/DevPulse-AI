import sys
import os

# Automatically resolve paths so cli.py works from anywhere
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
repo_dir = os.path.dirname(backend_dir)
for p in [repo_dir, backend_dir, current_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from app.models.audit import CodeScanRequest
    from app.services.security_engine import SecurityEngine
except ImportError:
    try:
        from models.audit import CodeScanRequest
        from services.security_engine import SecurityEngine
    except ImportError:
        from backend.app.models.audit import CodeScanRequest
        from backend.app.services.security_engine import SecurityEngine

def main():
    """
    DevPulse AI CLI Tool for local terminal security auditing.
    Usage:
        python scan.py <file_path>
        devpulse scan <file_path>
        python -m devpulse scan <file_path>
    """
    args = sys.argv[1:]
    
    # Handle help or no arguments
    if not args or args[0] in ("-h", "--help", "help"):
        print("\n" + "=" * 60)
        print("[+] DevPulse AI -- Autonomous Code Security Auditor")
        print("=" * 60)
        print("Usage:")
        print("  python scan.py <file_path>          (Direct file scan)")
        print("  devpulse scan <file_path>           (CLI command)")
        print("  python -m devpulse scan <file_path> (Module command)")
        print("\nExamples:")
        print("  python scan.py test_vulnerable.py")
        print("  devpulse scan main.py")
        print("=" * 60 + "\n")
        sys.exit(0)

    # If first argument is 'scan', use next argument as file. Otherwise first arg is file!
    if args[0] == "scan":
        target_file = args[1] if len(args) > 1 else "main.py"
    else:
        target_file = args[0]
    
    if not os.path.exists(target_file):
        print(f"\n[-] Error: File '{target_file}' not found!")
        print(f"[*] Searched in current directory: {os.getcwd()}")
        sys.exit(1)

    with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
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
