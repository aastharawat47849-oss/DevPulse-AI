#!/usr/bin/env python3
"""
DevPulse AI -- Direct Code Security Scanner
Run instantly without any installation or PATH configuration:
    python scan.py <file_path>
    python scan.py test_vulnerable.py
"""
import sys
import os

# Ensure backend directory is in sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(root_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.cli import main

if __name__ == "__main__":
    main()
