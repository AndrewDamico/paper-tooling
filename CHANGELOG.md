# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-02-10

### Added
- Initial stable release with modular architecture
- Stable entrypoints: scripts/build.py and scripts/convert_citations.py
- Package structure in paper_tooling/ for maintainability
- Citation conversion module (paper_tooling/citations.py)
- Build pipeline orchestration (paper_tooling/pipeline.py)
- Pandoc integration (paper_tooling/pandoc.py)
- LaTeX build support (paper_tooling/latex.py)
- Utility functions (paper_tooling/utils.py)
- System check script (scripts/doctor.py)
- Unit tests for citation conversion
- CITATION.cff for software citation
- Comprehensive README with usage examples

### Changed
- Refactored implementation from monolithic scripts to modular package
- Build script now supports --project-root, --clean, --no-pandoc, --no-latex, --verbose
- Citation conversion now supports --in-place option

### Maintained
- Backwards compatibility with existing paper repos
- Apache 2.0 license
- Standard library only (no external dependencies)
