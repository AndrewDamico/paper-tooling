"""
paper_tooling.notebook package - Notebook helper utilities.

Main functions:
- export_figure(): Export matplotlib figures to multiple formats
- export_table(): Export pandas DataFrames to multiple formats
- start_run(): Start a new experimental run
- get_current_run(): Get the current active run
- find_project_root(): Detect the paper repository root
"""

from .export import export_figure, export_table
from .run_context import start_run, get_current_run, set_current_run, get_run_dir, create_run_id
from .project_root import find_project_root

__all__ = [
    "export_figure",
    "export_table",
    "start_run",
    "get_current_run",
    "set_current_run",
    "get_run_dir",
    "create_run_id",
    "find_project_root",
]
