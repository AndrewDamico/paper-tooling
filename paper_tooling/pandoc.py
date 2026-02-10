"""
Pandoc conversion utilities.
"""
import subprocess
import sys
from pathlib import Path


def convert_markdown_to_latex(in_dir: Path, out_dir: Path, verbose: bool = False) -> None:
    """Convert all Markdown files to LaTeX using Pandoc."""
    out_dir.mkdir(parents=True, exist_ok=True)

    md_files = sorted(in_dir.glob("*.md"))
    if not md_files:
        print("No generated Markdown files found. Run the citation conversion step first.", file=sys.stderr)
        raise SystemExit(1)

    for md_file in md_files:
        tex_file = out_dir / (md_file.stem + ".tex")
        cmd = ["pandoc", str(md_file), "-o", str(tex_file)]
        
        if verbose:
            print(f"  pandoc {md_file.name} -> {tex_file.name}")
        
        subprocess.run(cmd, check=True)
