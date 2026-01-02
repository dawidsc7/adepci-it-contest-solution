import pytest
from analyzer import calculate_score


# ===================== BASIC CASES =====================

def test_empty_text_returns_zero():
    """Empty string should return score of 0."""
    assert calculate_score("") == 0


def test_no_keywords_returns_zero():
    """Text without Polish keywords should return 0."""
    assert calculate_score("abc xyz") == 0
    assert calculate_score("hello world") == 0


def test_single_keyword():
    """Single Polish keyword should return 1."""
    assert calculate_score("jest") == 1
    assert calculate_score("to") == 1


def test_multiple_keywords():
    """Multiple Polish keywords should be counted correctly."""
    assert calculate_score("to jest tekst") == 2  # "to" + "jest"
    assert calculate_score("to jest i nie") == 4  # "to" + "jest" + "i" + "nie"


# ===================== PUNCTUATION HANDLING =====================

def test_dots_are_treated_as_spaces():
    """Dots should be replaced with spaces for word splitting."""
    assert calculate_score("to.jest.tekst") == 2


def test_commas_are_treated_as_spaces():
    """Commas should be replaced with spaces for word splitting."""
    assert calculate_score("to,jest,tekst") == 2


def test_at_sign_is_treated_as_space():
    """@ symbol should be replaced with space for word splitting."""
    assert calculate_score("to@jest") == 2


def test_colon_is_treated_as_space():
    """Colons should be replaced with spaces for word splitting."""
    assert calculate_score("to:jest") == 2


def test_mixed_punctuation():
    """Mixed punctuation should all be handled correctly."""
    assert calculate_score("to.jest,i:na@do") == 5


# ===================== CASE INSENSITIVITY =====================

def test_uppercase_keywords_are_matched():
    """Keywords should match regardless of case."""
    assert calculate_score("TO JEST") == 2
    assert calculate_score("Jest") == 1


def test_mixed_case_keywords():
    """Mixed case should still match keywords."""
    assert calculate_score("To JeSt TeKsT") == 2


# ===================== EDGE CASES =====================

def test_only_punctuation():
    """Text with only punctuation should return 0."""
    assert calculate_score("...") == 0
    assert calculate_score(",,,") == 0
    assert calculate_score("@@@") == 0


def test_extra_spaces():
    """Extra spaces should not affect scoring."""
    assert calculate_score("to   jest") == 2
    assert calculate_score("  to  ") == 1


def test_keyword_as_part_of_word_not_matched():
    """Keywords embedded in larger words should NOT be matched."""
    assert calculate_score("jester") == 0  # "jest" is inside but "jester" != "jest"
    assert calculate_score("toster") == 0  # "to" is inside but "toster" != "to"
