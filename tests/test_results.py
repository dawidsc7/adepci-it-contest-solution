import pytest
import os
import results
from results import save_results


# ===================== FILE SAVING =====================

def test_saves_solution_to_file(tmp_path, monkeypatch):
    """Solution text should be saved to solution.txt file in the script directory."""
    # Mock the __file__ attribute to point to tmp_path
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    best_text = "Testowa wiadomość"
    save_results(best_text, 5, [])
    
    solution_file = tmp_path / "solution.txt"
    assert solution_file.exists()
    assert solution_file.read_text(encoding="utf-8") == best_text


def test_file_contains_correct_content(tmp_path, monkeypatch):
    """Saved file should contain exactly the decrypted message."""
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    best_text = "jutro jest dzisiaj kontakt na: test@example.com"
    save_results(best_text, 21, ["version1", "version2"])
    
    content = (tmp_path / "solution.txt").read_text(encoding="utf-8")
    assert content == best_text


def test_file_handles_polish_characters(tmp_path, monkeypatch):
    """File should correctly save Polish special characters."""
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    best_text = "żółć ąęśćźń"
    save_results(best_text, 1, [])
    
    content = (tmp_path / "solution.txt").read_text(encoding="utf-8")
    assert content == best_text


# ===================== OUTPUT DISPLAY =====================

def test_prints_all_versions(tmp_path, monkeypatch, capsys):
    """All decryption versions should be printed."""
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    versions = ["wersja1", "wersja2", "wersja3"]
    save_results("rozwiązanie", 5, versions)
    
    captured = capsys.readouterr()
    for version in versions:
        assert version in captured.out


def test_prints_shift_count(tmp_path, monkeypatch, capsys):
    """Shift count should be displayed in output."""
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    save_results("test message", 21, [])
    
    captured = capsys.readouterr()
    assert "21" in captured.out


def test_prints_extracted_email(tmp_path, monkeypatch, capsys):
    """Extracted email should be displayed."""
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    save_results("kontakt: test@example.com", 5, [])
    
    captured = capsys.readouterr()
    assert "test@example.com" in captured.out


# ===================== EMAIL EXTRACTION =====================

def test_extracts_simple_email(tmp_path, monkeypatch, capsys):
    """Simple email formats should be extracted."""
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    save_results("napisz na: user@domain.com", 1, [])
    
    captured = capsys.readouterr()
    assert "user@domain.com" in captured.out


def test_extracts_email_with_dots_in_name(tmp_path, monkeypatch, capsys):
    """Emails with dots in username should be extracted."""
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    save_results("email: jutro.jest.dzisiaj@adepci.it", 21, [])
    
    captured = capsys.readouterr()
    assert "jutro.jest.dzisiaj@adepci.it" in captured.out


def test_extracts_email_with_subdomain(tmp_path, monkeypatch, capsys):
    """Emails with subdomains should be extracted."""
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    save_results("kontakt: info@sub.domain.org", 5, [])
    
    captured = capsys.readouterr()
    assert "info@sub.domain.org" in captured.out


# ===================== EDGE CASES =====================

def test_empty_best_text_shows_error(tmp_path, monkeypatch, capsys):
    """Empty solution should display error message."""
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    save_results("", 0, ["v1", "v2"])
    
    captured = capsys.readouterr()
    assert "Nie udało się" in captured.out


def test_no_email_in_text(tmp_path, monkeypatch, capsys):
    """Text without email should not crash."""
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    save_results("tekst bez emaila", 5, [])
    
    captured = capsys.readouterr()
    # Should not contain "Email:" line
    assert "Email:" not in captured.out


def test_empty_versions_list(tmp_path, monkeypatch, capsys):
    """Empty versions list should not crash."""
    monkeypatch.setattr(results, '__file__', str(tmp_path / "results.py"))
    
    save_results("rozwiązanie", 5, [])
    
    captured = capsys.readouterr()
    assert "rozwiązanie" in captured.out
