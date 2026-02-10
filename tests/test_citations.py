"""
Unit tests for citation conversion.
"""
import unittest
from pathlib import Path
import tempfile
import shutil

from paper_tooling.citations import convert_text, process_file


class TestCitationConversion(unittest.TestCase):
    """Test citation conversion functionality."""
    
    def test_basic_conversion(self):
        """Test basic citation conversion."""
        text = "Some text {Bodapati, 2021 #535} more text"
        result, count = convert_text(text)
        self.assertEqual(result, "Some text [@RN535] more text")
        self.assertEqual(count, 1)
    
    def test_whitespace_variants(self):
        """Test conversion handles various whitespace."""
        text = "Text {Bodapati,2021#535} and {Author, Year # 540}"
        result, count = convert_text(text)
        self.assertEqual(result, "Text [@RN535] and [@RN540]")
        self.assertEqual(count, 2)
    
    def test_braces_without_hash_unchanged(self):
        """Test that braces without # are not changed."""
        text = "Some {text} with {braces}"
        result, count = convert_text(text)
        self.assertEqual(result, "Some {text} with {braces}")
        self.assertEqual(count, 0)
    
    def test_multiple_citations_one_line(self):
        """Test multiple citations in one line."""
        text = "Research shows {Author1, 2020 #100} and {Author2, 2021 #200} that..."
        result, count = convert_text(text)
        self.assertEqual(result, "Research shows [@RN100] and [@RN200] that...")
        self.assertEqual(count, 2)
    
    def test_no_changes_to_plain_text(self):
        """Test that plain text is not modified."""
        text = "Just plain text with no citations at all."
        result, count = convert_text(text)
        self.assertEqual(result, text)
        self.assertEqual(count, 0)
    
    def test_mixed_content(self):
        """Test mixed content with citations and other braces."""
        text = "See {Smith, 2019 #123} and note that {this is not a citation}."
        result, count = convert_text(text)
        self.assertEqual(result, "See [@RN123] and note that {this is not a citation}.")
        self.assertEqual(count, 1)
    
    def test_process_file_dry_run(self):
        """Test file processing in dry-run mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            in_file = tmpdir / "test.md"
            in_file.write_text("Text {Author, 2020 #100} text")
            
            out_dir = tmpdir / "out"
            out_dir.mkdir()
            
            count, has_remaining = process_file(in_file, out_dir, dry_run=True, in_place=False)
            
            self.assertEqual(count, 1)
            self.assertFalse(has_remaining)
            # Output file should not exist in dry-run
            self.assertFalse((out_dir / "test.md").exists())
    
    def test_process_file_normal(self):
        """Test file processing with normal output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            in_file = tmpdir / "test.md"
            in_file.write_text("Text {Author, 2020 #100} text")
            
            out_dir = tmpdir / "out"
            out_dir.mkdir()
            
            count, has_remaining = process_file(in_file, out_dir, dry_run=False, in_place=False)
            
            self.assertEqual(count, 1)
            self.assertFalse(has_remaining)
            
            # Output file should exist
            out_file = out_dir / "test.md"
            self.assertTrue(out_file.exists())
            self.assertEqual(out_file.read_text(), "Text [@RN100] text")


if __name__ == "__main__":
    unittest.main()
