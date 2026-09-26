from app.models.audit import CodeScanRequest, Severity
from app.services.security_engine import SecurityEngine

def test_detect_hardcoded_secret():
    vulnerable_code = "AWS_SECRET = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'"
    request = CodeScanRequest(file_name="config.py", code_content=vulnerable_code)
    result = SecurityEngine.scan_code(request)
    
    assert result.total_issues >= 1
    assert result.critical_count >= 1
    assert result.vulnerabilities[0].severity == Severity.CRITICAL
    assert "Hardcoded" in result.vulnerabilities[0].rule_name

def test_detect_sql_injection():
    vulnerable_code = "query = f'SELECT * FROM users WHERE id = {user_id}'"
    request = CodeScanRequest(file_name="db.py", code_content=vulnerable_code)
    result = SecurityEngine.scan_code(request)
    
    assert result.total_issues >= 1
    assert any("SQL Injection" in v.rule_name for v in result.vulnerabilities)

def test_clean_code_pass():
    clean_code = "import os\napi_key = os.getenv('API_KEY')"
    request = CodeScanRequest(file_name="clean.py", code_content=clean_code)
    result = SecurityEngine.scan_code(request)
    
    assert result.total_issues == 0
    assert result.security_score == 100.0

if __name__ == "__main__":
    test_detect_hardcoded_secret()
    test_detect_sql_injection()
    test_clean_code_pass()
    print("✅ All DevPulse AI Backend Security Engine Tests Passed!")
