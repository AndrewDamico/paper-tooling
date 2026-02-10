"""
Main build pipeline orchestration.
"""
import argparse
import subprocess
import sys
from pathlib import Path

from . import citations
from . import pandoc
from . import latex
from . import utils


def run_convert(project_root: Path, verbose: bool = False) -> None:
    """Run citation conversion step."""
    if verbose:
        print("[1/3] Converting EndNote citations...")
    
    in_dir = project_root / "paper" / "sections"
    out_dir = project_root / "paper" / "generated_md"
    
    argv = ["--in-dir", str(in_dir), "--out-dir", str(out_dir)]
    result = citations.main(argv)
    
    if result != 0:
        raise subprocess.CalledProcessError(result, "convert_citations")


def run_pandoc(project_root: Path, verbose: bool = False) -> None:
    """Run Pandoc conversion step."""
    if verbose:
        print("[2/3] Converting Markdown to LaTeX via Pandoc...")
    
    utils.ensure_tool("pandoc", "Pandoc is required but was not found on PATH.")
    
    in_dir = project_root / "paper" / "generated_md"
    out_dir = project_root / "paper" / "generated"
    
    pandoc.convert_markdown_to_latex(in_dir, out_dir, verbose)


def run_latexmk(project_root: Path, target: str, verbose: bool = False) -> None:
    """Run latexmk build step."""
    if verbose:
        print(f"[3/3] Building PDF via latexmk + biber (target: {target})...")
    
    utils.ensure_tool("latexmk", "latexmk is required but was not found on PATH.")
    utils.ensure_tool("biber", "biber is required but was not found on PATH.")
    
    paper_dir = project_root / "paper"
    latex.build_latex(paper_dir, target, verbose)


def main(argv=None) -> int:
    """Main entrypoint for build pipeline."""
    parser = argparse.ArgumentParser(description="Build the paper PDF via Pandoc and latexmk.")
    parser.add_argument("--target", choices=["full", "abstract"], default="full", help="Build target")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(), help="Project root directory")
    parser.add_argument("--clean", action="store_true", help="Clean generated outputs before building")
    parser.add_argument("--no-pandoc", action="store_true", help="Skip Pandoc conversion step")
    parser.add_argument("--no-latex", action="store_true", help="Skip LaTeX build step")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args(argv)

    project_root = args.project_root.resolve()
    
    try:
        if args.clean:
            utils.clean_generated_outputs(project_root, args.verbose)
        
        run_convert(project_root, args.verbose)
        
        if not args.no_pandoc:
            run_pandoc(project_root, args.verbose)
        
        if not args.no_latex:
            run_latexmk(project_root, args.target, args.verbose)
    
    except subprocess.CalledProcessError as exc:
        print(f"Command failed: {exc}", file=sys.stderr)
        return exc.returncode or 1
    
    return 0
