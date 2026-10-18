import sys
import os

# Ensure backend directory is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.services.security_engine import SecurityEngine
from app.models.audit import CodeScanRequest, AuditResult, Vulnerability, Severity
from app.cli import main

__all__ = [
    "SecurityEngine",
    "CodeScanRequest",
    "AuditResult",
    "Vulnerability",
    "Severity",
    "main",
]
