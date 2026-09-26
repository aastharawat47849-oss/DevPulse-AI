import logging
from typing import Dict, Any, List
from app.models.audit import AuditResult

logger = logging.getLogger("DevPulseAI.GitHubBot")

class GitHubPRBot:
    """
    Simulates / handles GitHub Webhook automation for posting
    inline code reviews and PR check status reports.
    """
    
    @staticmethod
    def generate_pr_markdown_summary(audit_result: AuditResult) -> str:
        """
        Formats audit results into GitHub-flavored Markdown for PR review comment.
        """
        status_emoji = "✅" if audit_result.security_score >= 85 else "⚠️" if audit_result.security_score >= 60 else "🚨"
        
        md = f"## {status_emoji} DevPulse AI — Code Security Audit Report\n\n"
        md += f"**File Audited:** `{audit_result.file_name}`  \n"
        md += f"**Security Score:** `{audit_result.security_score} / 100`  \n"
        md += f"**Risk Level:** `{audit_result.risk_level}`  \n\n"
        
        md += "### 📊 Vulnerability Breakdown\n"
        md += f"- 🔴 **Critical:** {audit_result.critical_count}\n"
        md += f"- 🟠 **High:** {audit_result.high_count}\n"
        md += f"- 🟡 **Medium:** {audit_result.medium_count}\n"
        md += f"- 🔵 **Low:** {audit_result.low_count}\n\n"
        
        if audit_result.vulnerabilities:
            md += "### 🔍 Detected Issues & AI Fixes\n\n"
            for vuln in audit_result.vulnerabilities:
                md += f"#### [{vuln.severity}] {vuln.rule_name} (Line {vuln.line_number})\n"
                md += f"- **CWE Category:** `{vuln.category}`\n"
                md += f"- **Description:** {vuln.description}\n"
                md += f"- **Vulnerable Line:**\n```python\n{vuln.vulnerable_code}\n```\n"
                md += f"- **🤖 AI Suggested Fix:**\n```python\n{vuln.ai_suggested_fix}\n```\n\n"
                md += "---\n"
        else:
            md += "🎉 **No security vulnerabilities detected! PR is safe to merge.**\n"
            
        md += "\n*Powered by DevPulse AI Autonomous Agent*"
        return md

    @classmethod
    def post_inline_review(cls, repo_owner: str, repo_name: str, pr_number: int, audit_result: AuditResult) -> Dict[str, Any]:
        """
        Posts simulated PR review comment to GitHub API.
        """
        summary_markdown = cls.generate_pr_markdown_summary(audit_result)
        logger.info(f"Posted DevPulse AI review to PR #{pr_number} in {repo_owner}/{repo_name}")
        
        return {
            "status": "SUCCESS",
            "pr_number": pr_number,
            "repo": f"{repo_owner}/{repo_name}",
            "posted_comments": len(audit_result.vulnerabilities),
            "review_summary": summary_markdown
        }
