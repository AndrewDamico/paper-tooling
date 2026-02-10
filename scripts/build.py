#!/usr/bin/env python3
"""
Build script wrapper - calls paper_tooling.pipeline.main()
"""
import sys
from pathlib import Path

# Add repo root to path for importability without installation
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

from paper_tooling import pipeline

if __name__ == "__main__":
    raise SystemExit(pipeline.main())
