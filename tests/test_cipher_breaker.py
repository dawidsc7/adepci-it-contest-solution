import pytest
from cipher_breaker import find_solution, decrypt_text


# ===================== TESTS FOR decrypt_text =====================

class TestDecryptTextBasicShifts:
    """Tests for basic shift values."""
    
    def test_shift_by_1(self):
        """Shift by 1: 'B' → 'A'"""
        assert decrypt_text("B", 1) == "A"
    
    def test_shift_by_3(self):
        """Shift by 3: 'D' → 'A'"""
        assert decrypt_text("D", 3) == "A"
    
    def test_shift_by_0_no_change(self):
        """Shift by 0 returns unchanged text."""
        assert decrypt_text("abc", 0) == "abc"
        assert decrypt_text("ABC", 0) == "ABC"
    
    def test_shift_by_26_no_change(self):
        """Shift by 26 returns unchanged text (full alphabet cycle)."""
        assert decrypt_text("abc", 26) == "abc"
        assert decrypt_text("XYZ", 26) == "XYZ"


class TestDecryptTextWrapAround:
    """Tests for alphabet wrap-around behavior."""
    
    def test_wrap_around_uppercase(self):
        """'A' with shift=1 → 'Z' (wraps around alphabet start)."""
        assert decrypt_text("A", 1) == "Z"
    
    def test_wrap_around_lowercase(self):
        """'a' with shift=1 → 'z' (wraps around alphabet start)."""
        assert decrypt_text("a", 1) == "z"
    
    def test_wrap_around_multiple_letters(self):
        """'ABC' with shift=3 → 'XYZ'."""
        assert decrypt_text("ABC", 3) == "XYZ"


class TestDecryptTextCase:
    """Tests for letter case preservation."""
    
    def test_lowercase_only(self):
        """Lowercase letters remain lowercase."""
        assert decrypt_text("abc", 1) == "zab"
        assert decrypt_text("b", 1) == "a"
    
    def test_uppercase_only(self):
        """Uppercase letters remain uppercase."""
        assert decrypt_text("ABC", 1) == "ZAB"
        assert decrypt_text("B", 1) == "A"
    
    def test_mixed_case(self):
        """Mixed case text preserves original letter cases."""
        assert decrypt_text("AbC", 1) == "ZaB"
        assert decrypt_text("aBcDeF", 1) == "zAbCdE"


class TestDecryptTextSpecialCharacters:
    """Tests for special characters and spaces."""
    
    def test_spaces_unchanged(self):
        """Spaces remain unchanged."""
        assert decrypt_text("a b c", 1) == "z a b"
        assert decrypt_text("   ", 1) == "   "
    
    def test_punctuation_unchanged(self):
        """Punctuation marks remain unchanged."""
        assert decrypt_text("A.B", 1) == "Z.A"
        assert decrypt_text("A,B,C", 1) == "Z,A,B"
    
    def test_at_symbol_unchanged(self):
        """@ symbol remains unchanged."""
        assert decrypt_text("A@B", 1) == "Z@A"
    
    def test_mixed_special_characters(self):
        """Mix of special characters remains unchanged."""
        assert decrypt_text("A.B@C!", 1) == "Z.A@B!"
        assert decrypt_text("A\nB\nC", 1) == "Z\nA\nB"
    
    def test_numbers_unchanged(self):
        """Numbers remain unchanged."""
        assert decrypt_text("A1B2C3", 1) == "Z1A2B3"


class TestDecryptTextEdgeCases:
    """Tests for edge cases."""
    
    def test_empty_string(self):
        """Empty string returns empty string."""
        assert decrypt_text("", 1) == ""
        assert decrypt_text("", 0) == ""
        assert decrypt_text("", 26) == ""
    
    def test_single_letter(self):
        """Single letter is correctly decrypted."""
        assert decrypt_text("A", 1) == "Z"
        assert decrypt_text("z", 1) == "y"
    
    def test_only_special_characters(self):
        """String with only special characters returns unchanged."""
        assert decrypt_text("!@#$%^&*()", 5) == "!@#$%^&*()"
        assert decrypt_text("   ", 10) == "   "


# ===================== TESTS FOR find_solution =====================

class TestFindSolutionReturnType:
    """Tests for correct return type."""
    
    def test_returns_tuple(self):
        """Function returns a tuple."""
        result = find_solution("abc")
        assert isinstance(result, tuple)
    
    def test_returns_three_elements(self):
        """Tuple contains exactly 3 elements."""
        result = find_solution("abc")
        assert len(result) == 3
    
    def test_all_versions_has_26_elements(self):
        """all_versions list contains 26 elements (shifts 0-25)."""
        _, _, all_versions = find_solution("abc")
        assert len(all_versions) == 26


class TestFindSolutionPolishText:
    """Tests for Polish text detection."""
    
    def test_known_polish_text(self):
        """Known encrypted Polish text returns correct shift."""
        best_text, correct_shift, all_versions = find_solution("epomj ezno yudndve")
        assert best_text == "jutro jest dzisiaj"
        assert correct_shift == 21
    
    def test_polish_text_round_trip(self):
        """Encrypt text, verify find_solution finds the original."""
        original = "jutro jest dzisiaj"
        shift = 21
        # Encryption = shift right, so decrypt with negative shift
        encrypted = decrypt_text(original, -shift % 26)  # -21 % 26 = 5
        best_text, found_shift, _ = find_solution(encrypted)
        assert best_text == original
        assert found_shift == shift


class TestFindSolutionAllVersions:
    """Tests for all_versions list."""
    
    def test_all_versions_contains_correct_answer(self):
        """all_versions contains the correct decrypted text."""
        _, _, all_versions = find_solution("epomj ezno yudndve")
        # Correct answer should be in the list (shift=21 means index 20)
        assert "jutro jest dzisiaj" in all_versions
    
    def test_all_versions_first_element_is_shift_0(self):
        """First element corresponds to shift=0 (unchanged text)."""
        _, _, all_versions = find_solution("epomj ezno yudndve")
        assert all_versions[0] == "epomj ezno yudndve"
    
    def test_all_versions_last_element_is_shift_25(self):
        """Last element corresponds to shift=25."""
        _, _, all_versions = find_solution("epomj ezno yudndve")
        assert all_versions[25] == "fqpnk faop zveoewf"


class TestFindSolutionFallback:
    """Tests for fallback mechanism."""
    
    def test_short_text_returns_result(self):
        """Very short text still returns a result."""
        best_text, shift, all_versions = find_solution("bc")
        assert best_text != ""  # should return some result
        assert isinstance(shift, int)
        assert len(all_versions) == 26
    
    def test_non_polish_text_uses_fallback(self):
        """Non-Polish text uses score-based fallback."""
        # Text that probably won't be detected as Polish
        result = find_solution("xyz")
        best_text, shift, all_versions = result
        # Function should still return a result
        assert best_text != ""
        assert isinstance(shift, int)
