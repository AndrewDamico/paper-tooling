# Paper Tooling

Shared tooling for academic paper authoring with Markdown, EndNote, Pandoc, and LaTeX.

## Overview

Paper Tooling is a git submodule designed to provide consistent, maintainable build automation for academic papers. It converts EndNote unformatted citations to Pandoc format and orchestrates the Markdown -> LaTeX -> PDF pipeline.

## Features

- **Citation conversion**: Converts EndNote unformatted tokens like `{Author, 2021 #535}` to Pandoc citations `[@RN535]`
- **Build pipeline**: Orchestrates Pandoc and latexmk to generate PDFs from Markdown sources
- **Modular architecture**: Clean separation between CLI scripts and implementation
- **No dependencies**: Uses only Python standard library
- **Reproducible**: Each paper repo pins a specific tooling commit via git submodule

## Usage as a Submodule

### Adding to a paper repository

From your paper repository root:

```bash
git submodule add https://github.com/AndrewDamico/paper-tooling tooling/paper-tooling
git submodule update --init --recursive
```

### Running build commands

From your paper repository root:

```bash
# Build full paper
python tooling/paper-tooling/scripts/build.py --target full

# Build abstract only
python tooling/paper-tooling/scripts/build.py --target abstract

# Convert citations only
python tooling/paper-tooling/scripts/convert_citations.py

# Check system prerequisites
python tooling/paper-tooling/scripts/doctor.py
```

### Updating the tooling in a paper repo

```bash
git submodule update --remote --merge
git add tooling/paper-tooling
git commit -m "Update paper-tooling"
```

Each paper repo pins a specific tooling commit for reproducibility.

## Script Reference

### build.py

Orchestrates the complete build pipeline.

Options:
- `--target {full,abstract}`: Build target (default: full)
- `--project-root PATH`: Project root directory (default: current directory)
- `--clean`: Clean generated outputs before building
- `--no-pandoc`: Skip Pandoc conversion step
- `--no-latex`: Skip LaTeX build step
- `--verbose`: Verbose output

Example:
```bash
python tooling/paper-tooling/scripts/build.py --target full --verbose
```

### convert_citations.py

Converts EndNote unformatted citations to Pandoc format.

Options:
- `--in-dir PATH`: Input directory of Markdown files (default: paper/sections)
- `--out-dir PATH`: Output directory (default: paper/generated_md)
- `--check`: Exit with error if unconverted tokens remain
- `--dry-run`: Show replacement counts without writing output
- `--in-place`: Overwrite source files in input directory

Example:
```bash
python tooling/paper-tooling/scripts/convert_citations.py --check
```

### doctor.py

Checks availability of required tools (Python, Pandoc, latexmk, biber).

Example:
```bash
python tooling/paper-tooling/scripts/doctor.py
```

## Bespoke notebook helpers

The `andrewdamico` package provides a user-friendly namespace for notebook helper functions used in Andrew D'Amico's teaching and research work. These helpers manage experimental runs and export outputs.

### Usage example

```python
import andrewdamico as ad

# Start a new experimental run
run_id = ad.start_run(project_root=".", label="exp1")

# Set as current run (optional - allows omitting run_id in subsequent calls)
ad.set_current_run(project_root=".", run_id=run_id)

# Export a matplotlib figure
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
ad.export_figure(project_root=".", run_id=run_id, name="fig_01", fig=fig, formats=["pdf", "png"])

# Export a pandas DataFrame as a table
import pandas as pd
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
ad.export_table(project_root=".", run_id=run_id, name="tbl_01", df=df, formats=["tex", "csv"])
```

### Run structure

Each run creates a directory structure:
```
project_root/
  runs/
    <run_id>/
      metadata.json
      figures/
        fig_01.pdf
        fig_01.png
      tables/
        tbl_01.tex
        tbl_01.csv
    CURRENT_RUN.txt
```

## Development

### Running tests

```bash
python -m unittest discover tests
```

### Project structure

```
paper-tooling/
  scripts/          # Stable CLI entrypoints
    build.py
    convert_citations.py
    doctor.py
  paper_tooling/    # Implementation modules
    __init__.py
    pipeline.py     # Build orchestration
    citations.py    # Citation conversion
    pandoc.py       # Pandoc integration
    latex.py        # LaTeX/latexmk integration
    utils.py        # Utilities
  tests/
    test_citations.py
  CITATION.cff
  CHANGELOG.md
  LICENSE
  README.md
```

## How to cite

If you use this software in your research, please cite it using the metadata in [CITATION.cff](CITATION.cff).

For BibTeX:

```bibtex
@software{damico_paper_tooling,
  author = {D'Amico, Andrew},
  title = {Paper Tooling},
  url = {https://github.com/AndrewDamico/paper-tooling},
  version = {0.1.0},
  year = {2026},
  license = {Apache-2.0}
}
```

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

## Author

Andrew D'Amico