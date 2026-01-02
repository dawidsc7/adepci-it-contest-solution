import pytest
import os
from data_loader import get_encrypted_text


class TestGetEncryptedTextDefaultFile:
    """Tests for reading from default ciphertext.txt file."""
    
    def test_reads_default_file_when_no_argument(self):
        """Returns content from ciphertext.txt when called without arguments."""
        result = get_encrypted_text()
        expected = "epomj ezno yudndve. nuopxuiv diozgdbzixev rkgtrv iv ivnuv xjyudziijnx. vwt fjiotipjrvx rturvidz, rtngde fjy uvyvidv iv: epomj.ezno.yudndve@vyzkxd.do"
        assert result == expected


class TestGetEncryptedTextFromFile:
    """Tests for reading from custom file paths."""
    
    def test_reads_existing_file(self):
        """Returns file content when valid file path is provided."""
        # Get the path to the test file relative to tests directory
        test_file = os.path.join(os.path.dirname(__file__), "sample_text_for_test_data_loader.txt")
        assert get_encrypted_text(test_file) == "sample text"
    
    def test_nonexistent_file_returns_input(self):
        """Returns input string when file does not exist."""
        assert get_encrypted_text("fake_file.txt") == "fake_file.txt"


class TestGetEncryptedTextDirectString:
    """Tests for direct string input (not a file)."""
    
    def test_returns_direct_string(self):
        """Returns the string directly when it's not a file path."""
        assert get_encrypted_text("abc xyz") == "abc xyz"
    
    def test_strips_whitespace(self):
        """Strips leading and trailing whitespace from input."""
        assert get_encrypted_text("  abc xyz  ") == "abc xyz"
    
    def test_empty_string_after_strip(self):
        """Handles whitespace-only input."""
        assert get_encrypted_text("   ") == ""


class TestGetEncryptedTextEdgeCases:
    """Tests for edge cases."""
    
    def test_multiline_string(self):
        """Handles multiline input string."""
        assert get_encrypted_text("line1\nline2") == "line1\nline2"
    
    def test_special_characters(self):
        """Handles special characters in input."""
        assert get_encrypted_text("test@email.com") == "test@email.com"