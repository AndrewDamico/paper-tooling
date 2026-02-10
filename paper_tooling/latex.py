"""
LaTeX build utilities using latexmk and biber.
"""
import subprocess
from pathlib import Path


def build_latex(paper_dir: Path, target: str, verbose: bool = False) -> None:
    """Build PDF using latexmk and biber."""
    main_file = f"main_{target}.tex"
    
    if verbose:
        print(f"  latexmk -pdf {main_file}")
    
    cmd = [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-use-biber",
        "-outdir=build",
        main_file
    ]
    subprocess.run(cmd, check=True, cwd=paper_dir)
