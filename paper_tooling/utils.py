"""
Utility functions for paper tooling.
"""
import shutil
import sys


def ensure_tool(name: str, hint: str) -> None:
    """Check if a command-line tool is available."""
    if shutil.which(name) is None:
        print(hint, file=sys.stderr)
        raise SystemExit(1)


def clean_generated_outputs(project_root, verbose: bool = False) -> None:
    """Clean generated outputs."""
    from pathlib import Path
    
    dirs_to_clean = [
        Path(project_root) / "paper" / "generated",
        Path(project_root) / "paper" / "generated_md",
        Path(project_root) / "paper" / "build",
    ]
    
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            if verbose:
                print(f"Cleaning {dir_path}")
            for item in dir_path.iterdir():
                if item.name not in {'.gitkeep', 'README.md'}:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        import shutil as sh
                        sh.rmtree(item)
