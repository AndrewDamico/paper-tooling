"""
Export utilities for figures and tables from notebooks.

Supports versioned runs so artifacts are organized by run_id.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

from .project_root import find_project_root
from .run_context import get_run_dir, get_current_run, start_run


def _load_manifest(manifest_path):
    """Load or initialize a manifest file."""
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        return {"run_id": "", "exports": []}


def _save_manifest(manifest_path, manifest):
    """Save a manifest file."""
    manifest_path.write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8"
    )


def export_figure(
    name,
    fig=None,
    project_root=None,
    run_id=None,
    formats=None,
    dpi=300
) -> Dict:
    """
    Export a figure to one or more formats.
    
    Args:
        name: Figure name (without extension)
        fig: Matplotlib figure object (uses current figure if None)
        project_root: Project root (auto-detected if None)
        run_id: Run ID (uses current or creates new if None)
        formats: List of formats (default: ["pdf", "png"])
        dpi: DPI for PNG export (default: 300)
    
    Returns:
        dict: Export metadata with paths and status
    
    Example:
        import andrewdamico as ad
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        ad.export_figure("accuracy_plot", fig=fig, formats=["pdf", "png"])
    """
    if formats is None:
        formats = ["pdf", "png"]
    
    if project_root is None:
        project_root = find_project_root()
    else:
        project_root = Path(project_root).resolve()
    
    # Get or create run
    if run_id is None:
        try:
            run_id = get_current_run(project_root=project_root)
        except ValueError:
            run_id = start_run(project_root=project_root, set_current=True)
    
    run_dir = get_run_dir(project_root=project_root, run_id=run_id, artifact_type="figures")
    
    # Import matplotlib lazily
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("matplotlib is required for export_figure")
    
    if fig is None:
        fig = plt.gcf()
    
    # Export to all requested formats
    paths = {}
    for fmt in formats:
        output_path = run_dir / f"{name}.{fmt}"
        
        if fmt == "png":
            fig.savefig(output_path, format=fmt, dpi=dpi, bbox_inches="tight")
        else:
            fig.savefig(output_path, format=fmt, bbox_inches="tight")
        
        paths[fmt] = str(output_path)
    
    # Update manifest
    manifest_file = run_dir / "manifest.json"
    manifest = _load_manifest(manifest_file)
    
    manifest["exports"].append({
        "type": "figure",
        "name": name,
        "timestamp": datetime.now().isoformat(),
        "formats": formats,
        "paths": paths
    })
    
    _save_manifest(manifest_file, manifest)
    
    return {
        "run_id": run_id,
        "name": name,
        "paths": paths
    }


def export_table(
    name,
    df=None,
    project_root=None,
    run_id=None,
    formats=None,
    index=False
) -> Dict:
    """
    Export a table (DataFrame) to one or more formats.
    
    Args:
        name: Table name (without extension)
        df: Pandas DataFrame
        project_root: Project root (auto-detected if None)
        run_id: Run ID (uses current or creates new if None)
        formats: List of formats (default: ["tex", "csv"])
        index: Include DataFrame index (default: False)
    
    Returns:
        dict: Export metadata with paths and status
    
    Example:
        import andrewdamico as ad
        import pandas as pd
        
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        ad.export_table("results", df=df, formats=["tex", "csv"])
    """
    if formats is None:
        formats = ["tex", "csv"]
    
    if df is None:
        raise ValueError("df (pandas DataFrame) is required for export_table")
    
    if project_root is None:
        project_root = find_project_root()
    else:
        project_root = Path(project_root).resolve()
    
    # Get or create run
    if run_id is None:
        try:
            run_id = get_current_run(project_root=project_root)
        except ValueError:
            run_id = start_run(project_root=project_root, set_current=True)
    
    run_dir = get_run_dir(project_root=project_root, run_id=run_id, artifact_type="tables")
    
    # Import pandas lazily
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required for export_table")
    
    # Export to all requested formats
    paths = {}
    for fmt in formats:
        output_path = run_dir / f"{name}.{fmt}"
        
        if fmt == "tex":
            df.to_latex(output_path, index=index)
        elif fmt == "csv":
            df.to_csv(output_path, index=index)
        elif fmt == "xlsx":
            df.to_excel(output_path, index=index)
        elif fmt == "html":
            df.to_html(output_path, index=index)
        else:
            raise ValueError(f"Unsupported table format: {fmt}")
        
        paths[fmt] = str(output_path)
    
    # Update manifest
    manifest_file = run_dir / "manifest.json"
    manifest = _load_manifest(manifest_file)
    
    manifest["exports"].append({
        "type": "table",
        "name": name,
        "timestamp": datetime.now().isoformat(),
        "formats": formats,
        "paths": paths
    })
    
    _save_manifest(manifest_file, manifest)
    
    return {
        "run_id": run_id,
        "name": name,
        "paths": paths
    }
