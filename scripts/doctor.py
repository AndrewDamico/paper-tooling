#!/usr/bin/env python3
"""
Doctor script - checks availability of required tools.
"""
import shutil
import subprocess
import sys


def check_tool(name: str) -> tuple[bool, str]:
    """Check if a tool is available and get its version."""
    if shutil.which(name) is None:
        return False, "NOT FOUND"
    
    # Try to get version
    try:
        if name == "python":
            result = subprocess.run(
                [sys.executable, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            version = result.stdout.strip() or result.stderr.strip()
        elif name == "pandoc":
            result = subprocess.run(
                ["pandoc", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            version = result.stdout.split('\n')[0] if result.stdout else "unknown"
        elif name in ["latexmk", "biber"]:
            result = subprocess.run(
                [name, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            version = result.stdout.split('\n')[0] if result.stdout else "unknown"
        else:
            version = "found"
        
        return True, version
    except Exception:
        return True, "found (version unknown)"


def main() -> int:
    """Check all required tools."""
    print("Paper Tooling - System Check")
    print("=" * 50)
    
    tools = [
        ("python", "Required"),
        ("pandoc", "Required"),
        ("latexmk", "Required"),
        ("biber", "Required"),
    ]
    
    all_ok = True
    
    for tool, status in tools:
        found, version = check_tool(tool)
        status_icon = "[OK]" if found else "[MISSING]"
        print(f"{status_icon} {tool:12s} {status:12s} {version}")
        
        if not found:
            all_ok = False
    
    print("=" * 50)
    
    if all_ok:
        print("All required tools are available.")
        return 0
    else:
        print("\nSome required tools are missing. Please install them:")
        print("  - Python: https://www.python.org/")
        print("  - Pandoc: https://pandoc.org/")
        print("  - LaTeX (includes latexmk): https://www.latex-project.org/get/")
        print("  - Biber: usually included with LaTeX distributions")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
