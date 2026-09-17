# =====================================================================
# 🚀 DEVPULSE AI: ADVANCED SECURITY & SYNTAX AUDIT ENGINE
# =====================================================================

import re
import json

class DevPulseAuditEngine:
    """
    Core Intelligence Engine of DevPulse AI.
    Audits source code snippets for security risks, syntax flaws,
    leaked secrets, code anti-patterns, and unclosed brackets.
    """

    def __init__(self):
        self.rules = [
            # Security Rule 1: Leaked API Keys & Secret Tokens
            {
                "id": "SEC-001",
                "name": "Hardcoded Secret Key",
                "severity": "CRITICAL",
                "deduction": 35,
                "pattern": r'(api_key|secret|private_key|token|auth_token|db_password|password)\s*=\s*["\'][A-Za-z0-9_\-]{8,}["\']',
                "message": "CRITICAL: Hardcoded API Key / Secret detected! Move sensitive credentials to environment variables (.env file).",
                "recommendation": "Use os.environ.get('API_KEY') instead of hardcoded strings."
            },
            # Security Rule 2: Potential SQL Injection Risk
            {
                "id": "SEC-002",
                "name": "SQL Injection Vulnerability",
                "severity": "HIGH",
                "deduction": 30,
                "pattern": r'(SELECT|INSERT|UPDATE|DELETE)\s+.*\s+FROM\s+.*\s*\+\s*|\s*f["\'].*(SELECT|INSERT|UPDATE|DELETE).*\*\{',
                "message": "HIGH RISK: Potential SQL Injection via string concatenation in query.",
                "recommendation": "Use parameterized queries (ORMs like SQLAlchemy or Prisma) to sanitize user inputs."
            },
            # Security Rule 3: Dangerous Code Execution
            {
                "id": "SEC-003",
                "name": "Arbitrary Code Execution",
                "severity": "HIGH",
                "deduction": 25,
                "pattern": r'\b(eval|exec)\s*\(',
                "message": "SECURITY RISK: Usage of eval() / exec() detected.",
                "recommendation": "Avoid dynamic code execution as it exposes the server to Remote Code Execution (RCE) attacks."
            },
            # Security Rule 4: Incomplete Variable Assignment
            {
                "id": "SYN-001",
                "name": "Incomplete Variable Assignment",
                "severity": "HIGH",
                "deduction": 25,
                "pattern": r'\b\w+\s*=\s*["\']?\s*$',
                "message": "SYNTAX ERROR: Empty or incomplete variable declaration.",
                "recommendation": "Provide a valid expression or string for variable assignment."
            },
            # Security Rule 5: Silent Exception Handling
            {
                "id": "QUAL-001",
                "name": "Silent Exception Suppression",
                "severity": "MEDIUM",
                "deduction": 15,
                "pattern": r'except.*:\s*pass',
                "message": "ANTI-PATTERN: Catching exceptions without logging or handling.",
                "recommendation": "Log exceptions properly instead of swallowing them with pass."
            }
        ]

    def audit_code(self, code_snippet: str, file_name: str = "main.py") -> dict:
        issues = []
        base_score = 100

        lines = code_snippet.split('\n')
        open_paren = 0
        open_bracket = 0
        open_brace = 0

        # Run Rule Matching across code lines
        for line_idx, line_content in enumerate(lines, start=1):
            trimmed = line_content.strip()
            if trimmed.startswith('#') or trimmed.startswith('//'):
                continue

            # Track Brackets
            open_paren += line_content.count('(') - line_content.count(')')
            open_bracket += line_content.count('[') - line_content.count(']')
            open_brace += line_content.count('{') - line_content.count('}')

            # Unclosed Quote Check per line
            if (line_content.count('"') % 2 != 0) or (line_content.count("'") % 2 != 0):
                issues.append({
                    "rule_id": "SYN-002",
                    "rule_name": "Syntax Error (Unclosed String)",
                    "severity": "HIGH",
                    "line_number": line_idx,
                    "code_snippet": trimmed,
                    "message": "SYNTAX ERROR: Unclosed string literal detected on this line.",
                    "recommendation": "Close string literals with matching quotes (\" or ').",
                    "deduction": 30
                })
                base_score -= 30

            # Pattern Rule Match
            for rule in self.rules:
                if re.search(rule["pattern"], line_content, re.IGNORECASE):
                    issues.append({
                        "rule_id": rule["id"],
                        "rule_name": rule["name"],
                        "severity": rule["severity"],
                        "line_number": line_idx,
                        "code_snippet": trimmed,
                        "message": rule["message"],
                        "recommendation": rule["recommendation"],
                        "deduction": rule["deduction"]
                    })
                    base_score -= rule["deduction"]

        # Bracket Mismatch Error Check
        if open_paren != 0 or open_bracket != 0 or open_brace != 0:
            issues.append({
                "rule_id": "SYN-003",
                "rule_name": "Unmatched Brackets / Parentheses",
                "severity": "HIGH",
                "line_number": len(lines),
                "code_snippet": "Global Check",
                "message": "SYNTAX ERROR: Unclosed parentheses (), brackets [], or braces {} in code block.",
                "recommendation": "Check closing parentheses and brackets across your code block.",
                "deduction": 20
            })
            base_score -= 20

        final_score = max(0, min(100, base_score))

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
            "summary": f"Deep audit completed for '{file_name}'. Score: {final_score}/100 ({status}). Found {len(issues)} issue(s).",
            "issues": issues
        }

# Global Instance
audit_engine = DevPulseAuditEngine()
