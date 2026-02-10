"""
andrewdamico - Bespoke notebook helpers for teaching and research.

This package provides a user-friendly namespace for notebook helper functions
used in Andrew D'Amico's teaching and research work.
"""

from paper_tooling.notebook.run_context import (
    start_run,
    set_current_run,
    get_current_run,
    get_run_dir,
)

from paper_tooling.notebook.export import (
    export_figure,
    export_table,
)

__all__ = [
    "start_run",
    "set_current_run",
    "get_current_run",
    "get_run_dir",
    "export_figure",
    "export_table",
]

__version__ = "0.1.0"
