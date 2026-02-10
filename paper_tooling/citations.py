"""
Citation conversion utilities for EndNote unformatted citations.
"""
import argparse
import re
import sys
from pathlib import Path

TOKEN_PATTERN = re.compile(r"\{[^{}]*?#\s*(\d+)\s*\}")
REMAINING_PATTERN = re.compile(r"\{[^{}]*#\s*\d+[^{}]*\}")


def convert_text(text: str) -> tuple[str, int]:
    """Convert EndNote unformatted citations to Pandoc citations."""
    def replacer(match: re.Match[str]) -> str:
        return f"[@RN{match.group(1)}]"

    return TOKEN_PATTERN.subn(replacer, text)


def process_file(path: Path, out_dir: Path, dry_run: bool, in_place: bool) -> tuple[int, bool]:
    """Process a single Markdown file."""
    text = path.read_text(encoding="utf-8")
    converted, count = convert_text(text)
    has_remaining = bool(REMAINING_PATTERN.search(converted))

    if dry_run:
        print(f"{path.name}: {count} replacements")
        return count, has_remaining

    if in_place:
        out_path = path
    else:
        out_path = out_dir / path.name
    
    out_path.write_text(converted, encoding="utf-8")
    return count, has_remaining


def main(argv=None) -> int:
    """Main entrypoint for citation conversion."""
    parser = argparse.ArgumentParser(description="Convert EndNote unformatted citations to Pandoc citations.")
    parser.add_argument("--in-dir", default="paper/sections", help="Input directory of Markdown files")
    parser.add_argument("--out-dir", default="paper/generated_md", help="Output directory for converted Markdown")
    parser.add_argument("--check", action="store_true", help="Fail if any tokens with #digits remain")
    parser.add_argument("--dry-run", action="store_true", help="Show replacement counts without writing output")
    parser.add_argument("--in-place", action="store_true", help="Overwrite source files in input directory")
    args = parser.parse_args(argv)

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)

    if not in_dir.exists():
        print(f"Input directory not found: {in_dir}", file=sys.stderr)
        return 1

    md_files = sorted(in_dir.glob("*.md"))
    if not md_files:
        print(f"No Markdown files found in {in_dir}")

    if not args.dry_run and not args.in_place:
        out_dir.mkdir(parents=True, exist_ok=True)

    had_remaining = False
    for path in md_files:
        _, has_remaining = process_file(path, out_dir, args.dry_run, args.in_place)
        had_remaining = had_remaining or has_remaining

    if args.check and had_remaining:
        print("Unconverted EndNote tokens with #digits remain.", file=sys.stderr)
        return 2

    return 0
