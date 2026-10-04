import sys
sys.path.append("backend")

from app.models.audit import CodeScanRequest
from app.services.security_engine import SecurityEngine

engine = SecurityEngine()
sample_code = """
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
query = f"SELECT * FROM users WHERE id={user_input}"
os.system(f"ping {ip_address}")
"""

req = CodeScanRequest(file_name="sample.py", code_content=sample_code)
result = engine.scan_code(req)

print("=== PYTHON DIRECT ENGINE TEST RESULTS ===")
print("File Name:", result.file_name)
print("Security Score:", result.security_score)
print("Risk Level:", result.risk_level)
print("Total Issues Found:", result.total_issues)
for vuln in result.vulnerabilities:
    print(f" -> [{vuln.severity}] {vuln.rule_name} (Line {vuln.line_number}): {vuln.description}")
