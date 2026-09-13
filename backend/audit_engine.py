# =====================================================================
# 🚀 DEVPULSE AI: SECURITY AUDIT ENGINE MODULE
# =====================================================================

import re
import json

class DevPulseAuditEngine:
    """
    Core Intelligence Engine of DevPulse AI.
    Audits source code snippets for security risks, leaked secrets,
    code quality, and performance bottlenecks.
    """

    def __init__(self):
        self.rules = [
            # Security Rule 1: Leaked API Keys & Secret Tokens
            {
                "id": "SEC-001",
                "name": "Hardcoded Secret Key",
                "severity": "CRITICAL",
                "deduction": 35,
                "pattern": r'(api_key|secret|private_key|token|auth_token)\s*=\s*["\'][A-Za-z0-9_\-]{12,}["\']',
                "message": "CRITICAL: Hardcoded API Key / Secret detected! Move sensitive credentials to environment variables (.env file).",
                "recommendation": "Use os.environ.get('API_KEY') instead of hardcoded strings."
            },
            # Security Rule 2: Hardcoded Passwords
            {
                "id": "SEC-002",
                "name": "Hardcoded Password",
                "severity": "CRITICAL",
                "deduction": 30,
                "pattern": r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']',
                "message": "CRITICAL: Hardcoded password found in source code.",
                "recommendation": "Use secure password vaults or environment variables."
            },
            # Security Rule 3: Potential SQL Injection Risk
            {
                "id": "SEC-003",
                "name": "SQL Injection Vulnerability",
                "severity": "HIGH",
                "deduction": 25,
                "pattern": r'(SELECT|INSERT|UPDATE|DELETE)\s+.*\s+FROM\s+.*\s*\+\s*|\s*f["\'].*(SELECT|INSERT|UPDATE|DELETE).*\*\{',
                "message": "HIGH RISK: Potential SQL Injection via string concatenation in query.",
                "recommendation": "Use parameterized queries (ORMs like SQLAlchemy or Prisma) to sanitize user inputs."
            },
            # Security Rule 4: Dangerous Code Execution
            {
                "id": "SEC-004",
                "name": "Arbitrary Code Execution",
                "severity": "HIGH",
                "deduction": 20,
                "pattern": r'\b(eval|exec)\s*\(',
                "message": "SECURITY RISK: Usage of eval() / exec() detected.",
                "recommendation": "Avoid dynamic code execution as it exposes the server to Remote Code Execution (RCE) attacks."
            },
            # Security Rule 5: XSS Vulnerability (Cross-Site Scripting)
            {
                "id": "SEC-005",
                "name": "XSS Vulnerability",
                "severity": "MEDIUM",
                "deduction": 15,
                "pattern": r'dangerouslySetInnerHTML|innerHTML\s*=',
                "message": "MEDIUM RISK: Unsanitized HTML insertion detected.",
                "recommendation": "Sanitize HTML payloads before rendering to prevent Cross-Site Scripting (XSS)."
            }
        ]

    def audit_code(self, code_snippet: str, file_name: str = "main.py") -> dict:
        """
        Executes security audit rules against code_snippet.
        Returns a complete structured Audit JSON Report.
        """
        issues = []
        base_score = 100

        lines = code_snippet.split('\n')

        # Run Rule Matching across code
        for rule in self.rules:
            for line_idx, line_content in enumerate(lines, start=1):
                if re.search(rule["pattern"], line_content, re.IGNORECASE):
                    issues.append({
                        "rule_id": rule["id"],
                        "rule_name": rule["name"],
                        "severity": rule["severity"],
                        "line_number": line_idx,
                        "code_snippet": line_content.strip(),
                        "message": rule["message"],
                        "recommendation": rule["recommendation"],
                        "deduction": rule["deduction"]
                    })
                    base_score -= rule["deduction"]

        # Ensure score stays in 0 - 100 range
        final_score = max(0, min(100, base_score))

        # Determine Security Health Status
        if final_score >= 85:
            status = "EXCELLENT"
            grade = "A+"
        elif final_score >= 70:
            status = "PASSED"
            grade = "B"
        elif final_score >= 50:
            status = "NEEDS_ATTENTION"
            grade = "C"
        else:
            status = "CRITICAL_FAILED"
            grade = "F"

        return {
            "file_name": file_name,
            "security_score": final_score,
            "grade": grade,
            "status": status,
            "total_issues_found": len(issues),
            "summary": f"Audit completed for '{file_name}'. Score: {final_score}/100 ({status}). Found {len(issues)} security issue(s).",
            "issues": issues
        }

# Global Instance
audit_engine = DevPulseAuditEngine()
