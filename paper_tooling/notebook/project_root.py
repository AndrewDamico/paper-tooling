"""
Project root detection for paper repositories.

Finds the root directory of a paper repository that contains both:
- paper/ (paper sources and artifacts)
- tooling/paper-tooling/ (the tooling submodule)
"""
from pathlib import Path
import warnings


def find_project_root(start_path=None):
    """
    Find the paper repository root by searching upward for paper/ and tooling/paper-tooling/.
    
    Args:
        start_path: Starting directory for search (default: current working directory)
    
    Returns:
        Path: The resolved project root directory
    
    Raises:
        If paper/ or tooling/paper-tooling/ is not found, returns Path.cwd() and warns.
    
    Usage:
        root = find_project_root()
        assert (root / "paper").exists()
    """
    if start_path is None:
        current = Path.cwd()
    else:
        current = Path(start_path).resolve()
    
    # Search upward
    while current != current.parent:
        paper_dir = current / "paper"
        tooling_dir = current / "tooling" / "paper-tooling"
        
        if paper_dir.exists() and tooling_dir.exists():
            return current
        
        current = current.parent
    
    # Fallback: return cwd and warn
    warnings.warn(
        f"Could not find project root (paper/ and tooling/paper-tooling/). "
        f"Using current directory: {Path.cwd()}",
        RuntimeWarning
    )
    return Path.cwd()
