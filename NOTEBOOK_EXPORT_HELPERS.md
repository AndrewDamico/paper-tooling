# Paper Tooling Notebook Export Helpers

Robust, production-ready utilities for managing experimental runs and exporting figures/tables from Jupyter notebooks to a paper repository.

## Overview

The `paper_tooling.notebook` module provides utilities to:
- **Detect project root** automatically
- **Manage versioned runs** with unique run IDs
- **Export figures** in multiple formats (PDF, PNG)
- **Export tables** in multiple formats (LaTeX, CSV, Excel, HTML)
- **Track exports** with JSON manifests for audit trails

All artifacts are organized hierarchically under `paper/figures/runs/<run_id>/` and `paper/tables/runs/<run_id>/`.

## Installation

The module is included in the `paper-tooling` package. Import it in your notebooks:

```python
from paper_tooling.notebook import (
    export_figure,
    export_table,
    start_run,
    get_current_run,
    find_project_root,
)
```

## Quick Start

### 1. Auto-detect project root

```python
from paper_tooling.notebook import find_project_root

root = find_project_root()
# Searches upward for paper/ and tooling/paper-tooling/ directories
```

### 2. Start a new experimental run

```python
from paper_tooling.notebook import start_run

run_id = start_run(label="baseline-experiment", set_current=True)
# Creates: paper/figures/runs/<run_id>/ and paper/tables/runs/<run_id>/
# Format: YYYY-MM-DD_HHMM_<label>_<git-hash>
```

### 3. Export a figure

```python
import matplotlib.pyplot as plt
from paper_tooling.notebook import export_figure

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])

result = export_figure("accuracy_plot", fig=fig, formats=["pdf", "png"])
# Saves to: paper/figures/runs/<run_id>/accuracy_plot.{pdf,png}
print(result['paths'])  # {'pdf': '...', 'png': '...'}
```

### 4. Export a table

```python
import pandas as pd
from paper_tooling.notebook import export_table

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
result = export_table("results", df=df, formats=["tex", "csv"])
# Saves to: paper/tables/runs/<run_id>/results.{tex,csv}
print(result['paths'])  # {'tex': '...', 'csv': '...'}
```

## API Reference

### Project Root Detection

#### `find_project_root(start_path=None) -> Path`

Automatically detect the paper repository root by searching upward for both:
- `paper/` directory (for sources and artifacts)
- `tooling/paper-tooling/` directory (the tooling submodule)

**Parameters:**
- `start_path` (str|Path, optional): Starting directory for search. Default: current working directory.

**Returns:**
- `Path`: The resolved project root directory.

**Raises:**
- Emits `RuntimeWarning` if root not found; returns `Path.cwd()`.

**Example:**
```python
root = find_project_root()
assert (root / "paper").exists()
assert (root / "tooling" / "paper-tooling").exists()
```

---

### Run Management

#### `create_run_id(prefix=None) -> str`

Generate a unique run identifier with git hash.

**Parameters:**
- `prefix` (str, optional): Label to include in the run_id. Sanitized for filesystem.

**Returns:**
- `str`: Run ID in format `YYYY-MM-DD_HHMM_<label>_<git-hash>` or `YYYY-MM-DD_HHMM_<git-hash>`.

**Example:**
```python
run_id = create_run_id(prefix="baseline")
# Returns: "2024-01-15_1430_baseline_a1b2c3d"
```

---

#### `start_run(project_root=None, label=None, set_current=True) -> str`

Start a new experimental run with versioned directory structure.

**Parameters:**
- `project_root` (str|Path, optional): Project root. Auto-detected if None.
- `label` (str, optional): Label for the run (included in run_id).
- `set_current` (bool): If True, mark this as the current active run. Default: True.

**Returns:**
- `str`: The created run_id.

**Creates:**
- `paper/figures/runs/<run_id>/manifest.json`
- `paper/tables/runs/<run_id>/manifest.json`
- `paper/figures/CURRENT_RUN.txt` (if `set_current=True`)
- `paper/tables/CURRENT_RUN.txt` (if `set_current=True`)

**Example:**
```python
run_id = start_run(label="exp-v1", set_current=True)
# Creates versioned directories and sets as current
```

---

#### `get_current_run(project_root=None) -> str`

Get the ID of the current active run.

**Parameters:**
- `project_root` (str|Path, optional): Project root. Auto-detected if None.

**Returns:**
- `str`: The current run_id.

**Raises:**
- `ValueError`: If no current run is set (CURRENT_RUN.txt doesn't exist).

**Example:**
```python
current_run = get_current_run()
```

---

#### `set_current_run(project_root=None, run_id=None) -> None`

Set or clear the current active run.

**Parameters:**
- `project_root` (str|Path, optional): Project root. Auto-detected if None.
- `run_id` (str, optional): Run ID to set as current. If None, clears current run.

**Example:**
```python
set_current_run(run_id="2024-01-15_1430_baseline_a1b2c3d")
# Writes to paper/figures/CURRENT_RUN.txt and paper/tables/CURRENT_RUN.txt
```

---

#### `get_run_dir(project_root=None, run_id=None, artifact_type="figures") -> Path`

Get the directory path for a run's artifacts.

**Parameters:**
- `project_root` (str|Path, optional): Project root. Auto-detected if None.
- `run_id` (str, optional): Run ID. Uses current if None.
- `artifact_type` (str): "figures" or "tables". Default: "figures".

**Returns:**
- `Path`: The run directory (e.g., `paper/figures/runs/<run_id>/`).

**Raises:**
- `ValueError`: If run directory doesn't exist.

**Example:**
```python
fig_dir = get_run_dir(artifact_type="figures")
tbl_dir = get_run_dir(artifact_type="tables")
```

---

### Figure Export

#### `export_figure(name, fig=None, project_root=None, run_id=None, formats=None, dpi=300) -> dict`

Export a matplotlib figure to one or more formats.

**Parameters:**
- `name` (str): Figure name (without extension).
- `fig` (matplotlib.figure.Figure, optional): Figure object. Uses `plt.gcf()` if None.
- `project_root` (str|Path, optional): Project root. Auto-detected if None.
- `run_id` (str, optional): Run ID. Uses current or creates new if None.
- `formats` (list, optional): List of formats (e.g., `["pdf", "png"]`). Default: `["pdf", "png"]`.
- `dpi` (int): DPI for PNG export. Default: 300.

**Returns:**
- `dict`: Export metadata with keys:
  - `run_id`: The run ID used
  - `name`: Figure name
  - `paths`: Dict mapping format to output path

**Saves to:**
- `paper/figures/runs/<run_id>/<name>.<format>`

**Updates:**
- `paper/figures/runs/<run_id>/manifest.json` with export record

**Example:**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])

result = export_figure(
    "accuracy_plot",
    fig=fig,
    formats=["pdf", "png"],
    dpi=300
)

print(result['paths'])
# {'pdf': '.../accuracy_plot.pdf', 'png': '.../accuracy_plot.png'}
```

---

### Table Export

#### `export_table(name, df=None, project_root=None, run_id=None, formats=None, index=False) -> dict`

Export a pandas DataFrame to one or more formats.

**Parameters:**
- `name` (str): Table name (without extension).
- `df` (pandas.DataFrame): The DataFrame to export. Required.
- `project_root` (str|Path, optional): Project root. Auto-detected if None.
- `run_id` (str, optional): Run ID. Uses current or creates new if None.
- `formats` (list, optional): List of formats (e.g., `["tex", "csv", "xlsx"]`). Default: `["tex", "csv"]`.
- `index` (bool): Include DataFrame index in export. Default: False.

**Returns:**
- `dict`: Export metadata with keys:
  - `run_id`: The run ID used
  - `name`: Table name
  - `paths`: Dict mapping format to output path

**Saves to:**
- `paper/tables/runs/<run_id>/<name>.<format>`

**Supported Formats:**
- `tex`: LaTeX table format
- `csv`: Comma-separated values
- `xlsx`: Excel workbook
- `html`: HTML table

**Updates:**
- `paper/tables/runs/<run_id>/manifest.json` with export record

**Example:**
```python
import pandas as pd

df = pd.DataFrame({
    "Method": ["A", "B", "C"],
    "Accuracy": [0.85, 0.89, 0.91],
    "F1": [0.84, 0.88, 0.90]
})

result = export_table(
    "results_summary",
    df=df,
    formats=["tex", "csv"],
    index=False
)

print(result['paths'])
# {'tex': '.../results_summary.tex', 'csv': '.../results_summary.csv'}
```

---

## Directory Structure

The module organizes artifacts hierarchically under the `paper/` directory:

```
project_root/
├── paper/
│   ├── figures/
│   │   ├── CURRENT_RUN.txt              # Current active run ID
│   │   └── runs/
│   │       ├── 2024-01-15_1430_baseline_a1b2c3d/
│   │       │   ├── manifest.json
│   │       │   ├── plot1.pdf
│   │       │   ├── plot1.png
│   │       │   ├── plot2.pdf
│   │       │   └── plot2.png
│   │       └── 2024-01-15_1500_v2_x7y8z9w/
│   │           ├── manifest.json
│   │           ├── plot1.pdf
│   │           └── plot1.png
│   │
│   ├── tables/
│   │   ├── CURRENT_RUN.txt              # Current active run ID
│   │   └── runs/
│   │       ├── 2024-01-15_1430_baseline_a1b2c3d/
│   │       │   ├── manifest.json
│   │       │   ├── results.tex
│   │       │   ├── results.csv
│   │       │   └── metrics.tex
│   │       └── 2024-01-15_1500_v2_x7y8z9w/
│   │           ├── manifest.json
│   │           └── results.tex
│   │
│   └── ... (paper sources)
│
└── tooling/
    └── paper-tooling/
        └── ... (tooling package)
```

### Manifest Structure

Each run creates `manifest.json` files in both figures and tables directories:

```json
{
  "run_id": "2024-01-15_1430_baseline_a1b2c3d",
  "label": "baseline",
  "created": "2024-01-15T14:30:45.123456",
  "exports": [
    {
      "type": "figure",
      "name": "accuracy_plot",
      "timestamp": "2024-01-15T14:31:12.654321",
      "formats": ["pdf", "png"],
      "paths": {
        "pdf": "/path/to/accuracy_plot.pdf",
        "png": "/path/to/accuracy_plot.png"
      }
    },
    {
      "type": "table",
      "name": "results",
      "timestamp": "2024-01-15T14:32:01.987654",
      "formats": ["tex", "csv"],
      "paths": {
        "tex": "/path/to/results.tex",
        "csv": "/path/to/results.csv"
      }
    }
  ]
}
```

---

## Usage Patterns

### Pattern 1: Single experiment with multiple exports

```python
from paper_tooling.notebook import start_run, export_figure, export_table
import matplotlib.pyplot as plt
import pandas as pd

# Start a run
run_id = start_run(label="experiment-1", set_current=True)

# Export multiple figures
for i in range(3):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [i, i+1, i+2])
    export_figure(f"plot_{i}", fig=fig)

# Export multiple tables
for i in range(2):
    df = pd.DataFrame({"A": [i, i+1], "B": [i+2, i+3]})
    export_table(f"table_{i}", df=df)
```

### Pattern 2: Multiple runs for comparison

```python
from paper_tooling.notebook import start_run, get_run_dir, export_figure

# Run 1
run1 = start_run(label="baseline", set_current=True)
# ... create and export figures/tables ...

# Run 2 (different hyperparameters)
run2 = start_run(label="improved", set_current=True)
# ... create and export figures/tables ...

# Access artifacts from both runs
from paper_tooling.notebook import get_run_dir
dir1 = get_run_dir(run_id=run1, artifact_type="figures")
dir2 = get_run_dir(run_id=run2, artifact_type="figures")
```

### Pattern 3: Switching between runs

```python
from paper_tooling.notebook import (
    get_current_run, set_current_run, export_figure
)

# Check current
current = get_current_run()

# Switch to different run
set_current_run(run_id="2024-01-15_1430_baseline_a1b2c3d")

# Subsequent exports go to this run
export_figure("new_plot", ...)

# Switch back
set_current_run(run_id=current)
```

---

## Features & Design

### ✅ Automatic Project Root Detection
- Searches upward for `paper/` and `tooling/paper-tooling/` directories
- Works from any subdirectory in the project
- Falls back to current directory with warning if not found

### ✅ Git-aware Run IDs
- Includes git commit hash for reproducibility
- Format: `YYYY-MM-DD_HHMM_<label>_<short-hash>`
- Gracefully falls back to `nogit` if not in a git repository

### ✅ Multi-format Export
- **Figures**: PDF, PNG, SVG, etc. (any matplotlib-supported format)
- **Tables**: LaTeX, CSV, Excel, HTML
- Configure DPI and formatting per export

### ✅ Manifest Tracking
- JSON audit trail of all exports
- Includes timestamps, formats, and file paths
- Enables programmatic artifact discovery

### ✅ Lazy Imports
- Only loads matplotlib when `export_figure()` is called
- Only loads pandas when `export_table()` is called
- Reduces import overhead for lightweight operations

### ✅ Versioned Runs
- Each run gets isolated directories
- Run IDs include timestamps and git hashes
- Supports concurrent runs and easy switching

### ✅ Production-Ready
- Comprehensive error handling and validation
- Type hints for IDE support
- Extensive docstrings with examples

---

## Error Handling

The module handles common errors gracefully:

```python
# Missing current run
try:
    export_figure("plot", ...)  # No run started
except ValueError:
    print("Please call start_run() first")

# Missing DataFrame
try:
    export_table("table", df=None)  # df is required
except ValueError:
    print("df parameter is required")

# Unsupported format
try:
    export_table("table", df=my_df, formats=["invalid"])
except ValueError:
    print("Unsupported table format: invalid")

# Missing dependencies
try:
    export_figure("plot", ...)  # matplotlib not installed
except ImportError:
    print("Install matplotlib: pip install matplotlib")
```

---

## Integration with Paper Workflow

This module integrates seamlessly with paper repositories:

1. **Notebook Analysis**: Develop and test analyses in Jupyter notebooks
2. **Export Artifacts**: Use `export_figure()` and `export_table()` to generate publication-ready files
3. **Organize by Run**: Each experiment gets a versioned, timestamped directory
4. **Track Versions**: Git hashes and manifests enable reproducibility
5. **Include in LaTeX**: Reference exported `.tex` and `.pdf` files in your paper

### Example LaTeX Integration

In your paper's main `.tex` file:

```latex
\documentclass{article}

\begin{document}

% Import figure from current run
\begin{figure}
  \centering
  \includegraphics{../figures/runs/CURRENT_RUN/accuracy_plot.pdf}
  \caption{Model accuracy across epochs.}
\end{figure}

% Import table from current run
\input{../tables/runs/CURRENT_RUN/results_summary.tex}

\end{document}
```

Then update `CURRENT_RUN.txt` when ready to generate the paper PDF.

---

## Best Practices

1. **Start each notebook with a run**: Call `start_run()` at the beginning to organize all exports.
2. **Use descriptive labels**: Include experiment parameters in the label (e.g., `"lr-0.001-batch-32"`).
3. **Export in consistent formats**: Use `formats=["pdf", "png"]` for figures and `["tex", "csv"]` for tables.
4. **Check manifests**: Review `manifest.json` to audit exports and timestamps.
5. **Version your notebooks**: Commit notebooks along with run artifacts for reproducibility.
6. **Use relative paths in LaTeX**: Reference `../figures/runs/CURRENT_RUN/` instead of absolute paths.

---

## Troubleshooting

### Project root not found
```python
# Manually specify project root
from pathlib import Path
root = Path.home() / "projects" / "my-paper"
export_figure("plot", fig=fig, project_root=root)
```

### "No current run set"
```python
# Start a new run or explicitly pass run_id
from paper_tooling.notebook import start_run, export_figure

run_id = start_run(label="my-run")
export_figure("plot", fig=fig, run_id=run_id)
```

### File already exists
The export functions overwrite existing files. This is intentional for iteration. Remove old runs manually if needed:

```bash
rm -rf paper/figures/runs/2024-01-15_1430_baseline_*
```

---

## See Also

- [example_notebook_export_tutorial.ipynb](example_notebook_export_tutorial.ipynb) - Complete working examples
- Paper template structure and best practices
- Reproducible research guide
