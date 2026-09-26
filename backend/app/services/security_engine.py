import re
import uuid
from datetime import datetime, timezone
from typing import List
from app.models.audit import Vulnerability, Severity, AuditResult, CodeScanRequest

class SecurityEngine:
    """
    Autonomous Security Audit Engine for DevPulse AI.
    Inspects source code diffs/files for OWASP Top 10 vulnerabilities, API secret leaks,
    SQL Injection, XSS, and Remote Code Execution patterns.
    """
    
    SECURITY_RULES = [
        {
            "id": "SEC-001",
            "rule_name": "Hardcoded API Secret / Private Key",
            "category": "CWE-798: Use of Hard-coded Credentials",
            "severity": Severity.CRITICAL,
            "pattern": r"(?i)(api[_\-]?key|secret[_\-]?key|aws[_\-]?secret|bearer[_\-]?token|password)\s*=\s*['\"][A-Za-z0-9/+=]{8,}['\"]",
            "description": "Hardcoded credential detected in source code. Exposing secrets leads to unauthorized cloud account takeover.",
            "remediation": "Move sensitive credentials to environment variables using `os.getenv()` or a secrets manager.",
            "fix_template": lambda line: f"import os\n# SECURE FIX: Loaded from environment\nAPI_KEY = os.getenv('API_SECRET_KEY', 'your_default_secure_vault_key')"
        },
        {
            "id": "SEC-002",
            "rule_name": "SQL Injection Vulnerability",
            "category": "CWE-89: Improper Neutralization of Special Elements used in an SQL Command",
            "severity": Severity.CRITICAL,
            "pattern": r"(?i)(?:f['\"].*?(?:select|insert|update|delete)|(?:select|insert|update|delete)\s+.*?(?:f['\"]|\.format\(|\+\s*[a-zA-Z_]|\{[a-zA-Z_]))",
            "description": "Unsanitized dynamic string concatenation used in SQL query, allowing malicious SQL injection payloads.",
            "remediation": "Use parameterized queries with prepared statements (e.g. `cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))`).",
            "fix_template": lambda line: "# SECURE FIX: Parameterized SQL Query\ncursor.execute('SELECT * FROM users WHERE username = %s', (username,))"
        },
        {
            "id": "SEC-003",
            "rule_name": "Remote Code Execution (RCE)",
            "category": "CWE-94: Improper Control of Generation of Code ('Code Injection')",
            "severity": Severity.CRITICAL,
            "pattern": r"(?i)\b(eval|exec|os\.system|subprocess\.call\(.*shell\s*=\s*True)\b",
            "description": "Dangerous execution of arbitrary system commands or dynamic code evaluation based on untrusted input.",
            "remediation": "Avoid using `eval()` or `os.system()`. Use `subprocess.run()` with argument lists and `shell=False`.",
            "fix_template": lambda line: "# SECURE FIX: Safe subprocess execution without shell=True\nimport subprocess\nsubprocess.run(['ls', '-l'], check=True, capture_output=True)"
        },
        {
            "id": "SEC-004",
            "rule_name": "Cross-Site Scripting (XSS)",
            "category": "CWE-79: Improper Neutralization of Input During Web Page Generation",
            "severity": Severity.HIGH,
            "pattern": r"(?i)(innerHTML\s*=|dangerouslySetInnerHTML|document\.write\()",
            "description": "Raw unescaped DOM insertion detected, making the web frontend susceptible to Cross-Site Scripting (XSS).",
            "remediation": "Sanitize user input before DOM insertion using DOMPurify or safe React text nodes.",
            "fix_template": lambda line: "// SECURE FIX: Sanitized HTML rendering\nconst cleanHTML = DOMPurify.sanitize(userInput);\nelement.innerHTML = cleanHTML;"
        },
        {
            "id": "SEC-005",
            "rule_name": "Insecure Deserialization",
            "category": "CWE-502: Deserialization of Untrusted Data",
            "severity": Severity.HIGH,
            "pattern": r"(?i)\b(pickle\.loads|yaml\.load\(.*Loader\s*=\s*yaml\.Loader)\b",
            "description": "Deserializing untrusted data streams allows arbitrary object instantiation and remote code execution.",
            "remediation": "Use `yaml.safe_load()` instead of `yaml.load()`, or replace pickle with JSON serialization.",
            "fix_template": lambda line: "# SECURE FIX: Safe YAML loading\nimport yaml\ndata = yaml.safe_load(yaml_string)"
        },
        {
            "id": "SEC-006",
            "rule_name": "Weak Cryptographic Hash Algorithm",
            "category": "CWE-327: Use of a Broken or Risky Cryptographic Algorithm",
            "severity": Severity.MEDIUM,
            "pattern": r"(?i)\b(hashlib\.md5|hashlib\.sha1)\b",
            "description": "MD5 and SHA-1 hashing algorithms are cryptographically vulnerable to collision attacks.",
            "remediation": "Upgrade hashing algorithm to SHA-256 (`hashlib.sha256()`) or bcrypt for passwords.",
            "fix_template": lambda line: "# SECURE FIX: SHA-256 Hashing\nimport hashlib\nhash_object = hashlib.sha256(data.encode()).hexdigest()"
        }
    ]

    @classmethod
    def scan_code(cls, request: CodeScanRequest) -> AuditResult:
        lines = request.code_content.splitlines()
        vulnerabilities: List[Vulnerability] = []
        
        for line_idx, line in enumerate(lines, start=1):
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith("#") or stripped_line.startswith("//"):
                continue
                
            for rule in cls.SECURITY_RULES:
                if re.search(rule["pattern"], stripped_line):
                    vulnerabilities.append(
                        Vulnerability(
                            id=f"VULN-{uuid.uuid4().hex[:6].upper()}",
                            rule_name=rule["rule_name"],
                            category=rule["category"],
                            severity=rule["severity"],
                            line_number=line_idx,
                            vulnerable_code=stripped_line,
                            description=rule["description"],
                            remediation=rule["remediation"],
                            ai_suggested_fix=rule["fix_template"](stripped_line)
                        )
                    )

        # Calculate metrics & score
        total_issues = len(vulnerabilities)
        critical = sum(1 for v in vulnerabilities if v.severity == Severity.CRITICAL)
        high = sum(1 for v in vulnerabilities if v.severity == Severity.HIGH)
        medium = sum(1 for v in vulnerabilities if v.severity == Severity.MEDIUM)
        low = sum(1 for v in vulnerabilities if v.severity == Severity.LOW)

        # Security Score Algorithm (100 - weighted penalty)
        penalty = (critical * 25) + (high * 15) + (medium * 8) + (low * 3)
        security_score = max(0.0, float(100 - penalty))

        if security_score >= 85:
            risk_level = "LOW RISK (PASS)"
        elif security_score >= 60:
            risk_level = "MODERATE RISK (WARNING)"
        else:
            risk_level = "CRITICAL RISK (BLOCK PR)"

        return AuditResult(
            audit_id=f"AUDIT-{uuid.uuid4().hex[:8].upper()}",
            file_name=request.file_name,
            security_score=round(security_score, 1),
            risk_level=risk_level,
            total_issues=total_issues,
            critical_count=critical,
            high_count=high,
            medium_count=medium,
            low_count=low,
            vulnerabilities=vulnerabilities,
            scanned_at=datetime.now(timezone.utc).isoformat()
        )
