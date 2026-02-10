"""
Run context management for notebook experiments with versioning.

Runs are organized by run_id (timestamp + optional label + short hash).
Each run gets its own folder under paper/figures/runs/<run_id> and paper/tables/runs/<run_id>.
CURRENT_RUN.txt tracks the active run for exports.
"""
import json
from datetime import datetime
from pathlib import Path
import subprocess

from .project_root import find_project_root


def create_run_id(prefix=None):
    """
    Create a unique run identifier.
    
    Format: YYYY-MM-DD_HHMM_<label>_<short-hash>
    
    Args:
        prefix: Optional label to include in the run_id
    
    Returns:
        str: The run_id
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    
    # Try to get short git hash
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            git_hash = result.stdout.strip()
        else:
            git_hash = "nogit"
    except Exception:
        git_hash = "nogit"
    
    if prefix:
        # Sanitize prefix for filesystem
        safe_prefix = "".join(c if c.isalnum() or c in "-_" else "_" for c in prefix)
        return f"{timestamp}_{safe_prefix}_{git_hash}"
    else:
        return f"{timestamp}_{git_hash}"


def start_run(project_root=None, label=None, set_current=True):
    """
    Start a new experimental run.
    
    Creates directory structure:
    - paper/figures/runs/<run_id>/
    - paper/tables/runs/<run_id>/
    Each gets a manifest.json and optionally becomes CURRENT_RUN.
    
    Args:
        project_root: Project root (auto-detected if None)
        label: Optional label for the run
        set_current: If True, write CURRENT_RUN.txt to mark this as active
    
    Returns:
        str: The run_id
    """
    if project_root is None:
        project_root = find_project_root()
    else:
        project_root = Path(project_root).resolve()
    
    run_id = create_run_id(prefix=label)
    
    # Create run directories
    fig_run_dir = project_root / "paper" / "figures" / "runs" / run_id
    tbl_run_dir = project_root / "paper" / "tables" / "runs" / run_id
    
    fig_run_dir.mkdir(parents=True, exist_ok=True)
    tbl_run_dir.mkdir(parents=True, exist_ok=True)
    
    # Create manifest files
    manifest = {
        "run_id": run_id,
        "label": label,
        "created": datetime.now().isoformat(),
        "exports": []
    }
    
    (fig_run_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8"
    )
    (tbl_run_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8"
    )
    
    # Set as current if requested
    if set_current:
        set_current_run(project_root=project_root, run_id=run_id)
    
    return run_id


def set_current_run(project_root=None, run_id=None):
    """
    Set the current active run by writing CURRENT_RUN.txt.
    
    Args:
        project_root: Project root (auto-detected if None)
        run_id: The run ID to set as current (or None to clear)
    """
    if project_root is None:
        project_root = find_project_root()
    else:
        project_root = Path(project_root).resolve()
    
    fig_current_file = project_root / "paper" / "figures" / "CURRENT_RUN.txt"
    tbl_current_file = project_root / "paper" / "tables" / "CURRENT_RUN.txt"
    
    if run_id:
        fig_current_file.write_text(run_id, encoding="utf-8")
        tbl_current_file.write_text(run_id, encoding="utf-8")
    else:
        if fig_current_file.exists():
            fig_current_file.unlink()
        if tbl_current_file.exists():
            tbl_current_file.unlink()


def get_current_run(project_root=None):
    """
    Get the current active run ID.
    
    Args:
        project_root: Project root (auto-detected if None)
    
    Returns:
        str: The run_id, or None if not set
    
    Raises:
        ValueError: If CURRENT_RUN.txt does not exist
    """
    if project_root is None:
        project_root = find_project_root()
    else:
        project_root = Path(project_root).resolve()
    
    fig_current_file = project_root / "paper" / "figures" / "CURRENT_RUN.txt"
    
    if not fig_current_file.exists():
        raise ValueError(
            "No current run set. Call start_run() first or use set_current_run()."
        )
    
    return fig_current_file.read_text(encoding="utf-8").strip()


def get_run_dir(project_root=None, run_id=None, artifact_type="figures"):
    """
    Get the directory path for a run artifact.
    
    Args:
        project_root: Project root (auto-detected if None)
        run_id: The run ID (uses current if None)
        artifact_type: "figures" or "tables"
    
    Returns:
        Path: The run directory
    """
    if project_root is None:
        project_root = find_project_root()
    else:
        project_root = Path(project_root).resolve()
    
    if run_id is None:
        run_id = get_current_run(project_root=project_root)
    
    run_dir = project_root / "paper" / artifact_type / "runs" / run_id
    
    if not run_dir.exists():
        raise ValueError(f"Run directory does not exist: {run_dir}")
    
    return run_dir
