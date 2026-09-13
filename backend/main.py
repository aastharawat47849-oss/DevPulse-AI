# =====================================================================
# 🚀 DEVPULSE AI: FASTAPI BACKEND SERVER
# =====================================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from audit_engine import audit_engine

app = FastAPI(
    title="DevPulse AI API",
    description="Autonomous Code Auditor & Security Agent API",
    version="1.0.0"
)

# Enable CORS for Frontend Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas for Request Payloads
class AuditRequest(BaseModel):
    code: str
    file_name: Optional[str] = "app.py"

class GitHubPRWebhookRequest(BaseModel):
    repository: str
    pull_request_id: int
    author: str
    code_diff: str

@app.get("/")
def root_status():
    """Server Root Health Check"""
    return {
        "service": "DevPulse AI Autonomous Security Agent",
        "status": "ONLINE",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.post("/api/audit")
def audit_code_endpoint(payload: AuditRequest):
    """
    Main Code Security Audit Endpoint.
    Receives code snippet, runs security engine, returns audit JSON report.
    """
    if not payload.code or len(payload.code.strip()) == 0:
        raise HTTPException(status_code=400, detail="Code payload cannot be empty.")
    
    report = audit_engine.audit_code(code_snippet=payload.code, file_name=payload.file_name)
    return report

@app.post("/api/github-webhook")
def github_pr_webhook_endpoint(payload: GitHubPRWebhookRequest):
    """
    Simulated GitHub Webhook Endpoint.
    Receives GitHub Pull Request event, audits code diff, and returns inline review comments.
    """
    report = audit_engine.audit_code(code_snippet=payload.code_diff, file_name=f"PR-#{payload.pull_request_id}")
    
    # Format GitHub Inline Comments
    github_inline_comments = []
    for issue in report["issues"]:
        github_inline_comments.append({
            "path": payload.repository,
            "line": issue["line_number"],
            "body": f"⚠️ **[DevPulse AI Bot - {issue['severity']}]**: {issue['message']}\n\n💡 **Recommendation**: {issue['recommendation']}"
        })

    return {
        "event": "pull_request.opened",
        "repository": payload.repository,
        "pr_id": payload.pull_request_id,
        "author": payload.author,
        "security_score": report["security_score"],
        "status": report["status"],
        "comments_posted_to_github": len(github_inline_comments),
        "inline_comments": github_inline_comments
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
