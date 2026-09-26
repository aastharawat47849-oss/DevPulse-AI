from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class Vulnerability(BaseModel):
    id: str
    rule_name: str
    category: str
    severity: Severity
    line_number: int
    vulnerable_code: str
    description: str
    remediation: str
    ai_suggested_fix: str

class AuditResult(BaseModel):
    audit_id: str
    file_name: str
    security_score: float = Field(..., ge=0.0, le=100.0)
    risk_level: str
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    vulnerabilities: List[Vulnerability]
    scanned_at: str

class CodeScanRequest(BaseModel):
    file_name: str = "main.py"
    code_content: str

class CodeFixRequest(BaseModel):
    vulnerability_id: str
    original_code: str
    ai_suggested_fix: str
