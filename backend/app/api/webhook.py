from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
from app.models.audit import CodeScanRequest, AuditResult
from app.services.security_engine import SecurityEngine
from app.services.github_bot import GitHubPRBot

router = APIRouter()

# Sample vulnerable code snippet for instant dashboard demo
SAMPLE_VULNERABLE_CODE = """import os
import sqlite3
import yaml
import hashlib

# SEC-001: Hardcoded AWS Secret Key Leak
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def login_user(username, password):
    # SEC-002: Vulnerable SQL Injection
    db = sqlite3.connect("app.db")
    cursor = db.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    # SEC-006: Weak Cryptographic Hash (MD5)
    hashed_pass = hashlib.md5(password.encode()).hexdigest()
    return cursor.fetchone()

def execute_admin_command(user_command):
    # SEC-003: Remote Code Execution (RCE)
    os.system("echo Executing: " + user_command)

def load_user_config(yaml_string):
    # SEC-005: Insecure Deserialization
    return yaml.load(yaml_string, Loader=yaml.Loader)
"""

@router.post("/scan", response_model=AuditResult)
async def scan_code_endpoint(request: CodeScanRequest):
    """
    Scans a given code snippet for OWASP security vulnerabilities.
    """
    try:
        result = SecurityEngine.scan_code(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sample", response_model=AuditResult)
async def get_sample_audit():
    """
    Returns a pre-computed sample audit result for instant UI dashboard demonstration.
    """
    request = CodeScanRequest(file_name="auth_service.py", code_content=SAMPLE_VULNERABLE_CODE)
    return SecurityEngine.scan_code(request)

@router.post("/webhook/github")
async def github_webhook_endpoint(payload: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    GitHub Webhook receiver for Pull Request events.
    Fires autonomous security audit and posts PR review comments.
    """
    action = payload.get("action")
    pull_request = payload.get("pull_request", {})
    
    if action in ["opened", "synchronize", "reopened"]:
        pr_number = pull_request.get("number", 101)
        repo_name = payload.get("repository", {}).get("name", "devpulse-demo-repo")
        repo_owner = payload.get("repository", {}).get("owner", {}).get("login", "devpulse-org")
        
        # Scan code
        scan_req = CodeScanRequest(file_name="pr_diff.py", code_content=SAMPLE_VULNERABLE_CODE)
        audit_res = SecurityEngine.scan_code(scan_req)
        
        # Post review comment
        bot_response = GitHubPRBot.post_inline_review(repo_owner, repo_name, pr_number, audit_res)
        
        return {
            "message": "GitHub PR Webhook processed successfully",
            "bot_response": bot_response,
            "audit_summary": audit_res
        }
        
    return {"message": f"Ignored GitHub action: {action}"}
