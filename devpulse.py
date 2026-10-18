#!/usr/bin/env python3
"""
DevPulse AI -- CLI Runner
Usage:
    python devpulse.py scan <file_path>
    python devpulse.py <file_path>
"""
import sys
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(root_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.cli import main

if __name__ == "__main__":
    main()
