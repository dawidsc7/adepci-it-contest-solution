import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path to import main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main


# ===================== TESTS FOR CLI ARGUMENTS =====================

class TestMainCLIArguments:
    """Tests for command-line argument handling."""
    
    def test_no_arguments_uses_default(self, monkeypatch, tmp_path):
        """When no arguments provided, uses default ciphertext.txt."""
        # Create a fake ciphertext.txt in current directory
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        # Create test file with known encrypted Polish text
        ciphertext_file = tmp_path / "ciphertext.txt"
        ciphertext_file.write_text("epomj ezno yudndve", encoding="utf-8")
        
        monkeypatch.setattr(sys, 'argv', ['main.py'])
        
        try:
            main()
            # Verify solution.txt was created
            solution_file = tmp_path / "solution.txt"
            assert solution_file.exists()
            assert solution_file.read_text(encoding="utf-8") == "jutro jest dzisiaj"
        finally:
            os.chdir(original_cwd)
    
    def test_file_argument(self, monkeypatch, tmp_path):
        """When file path provided, loads text from that file."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        custom_file = tmp_path / "custom.txt"
        custom_file.write_text("epomj ezno yudndve", encoding="utf-8")
        
        monkeypatch.setattr(sys, 'argv', ['main.py', str(custom_file)])
        
        try:
            main()
            solution_file = tmp_path / "solution.txt"
            assert solution_file.exists()
            assert solution_file.read_text(encoding="utf-8") == "jutro jest dzisiaj"
        finally:
            os.chdir(original_cwd)
    
    def test_direct_text_argument(self, monkeypatch, tmp_path):
        """When text string provided directly, uses it as ciphertext."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        monkeypatch.setattr(sys, 'argv', ['main.py', 'epomj ezno yudndve'])
        
        try:
            main()
            solution_file = tmp_path / "solution.txt"
            assert solution_file.exists()
            assert solution_file.read_text(encoding="utf-8") == "jutro jest dzisiaj"
        finally:
            os.chdir(original_cwd)


# ===================== TESTS FOR INTEGRATION =====================

class TestMainIntegration:
    """Integration tests verifying the full pipeline."""
    
    def test_full_pipeline_produces_correct_result(self, monkeypatch, tmp_path):
        """Complete pipeline: load → decrypt → save works correctly."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        test_file = tmp_path / "test_cipher.txt"
        test_file.write_text("epomj ezno yudndve", encoding="utf-8")
        
        monkeypatch.setattr(sys, 'argv', ['main.py', str(test_file)])
        
        try:
            main()
            
            # Verify output file exists and contains correct content
            solution_file = tmp_path / "solution.txt"
            assert solution_file.exists(), "solution.txt should be created"
            
            result = solution_file.read_text(encoding="utf-8")
            assert result == "jutro jest dzisiaj"
        finally:
            os.chdir(original_cwd)
    
    def test_pipeline_creates_solution_file(self, monkeypatch, tmp_path):
        """Main function creates solution.txt file."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        test_file = tmp_path / "input.txt"
        test_file.write_text("bcde", encoding="utf-8")
        
        monkeypatch.setattr(sys, 'argv', ['main.py', str(test_file)])
        
        try:
            main()
            solution_file = tmp_path / "solution.txt"
            assert solution_file.exists()
        finally:
            os.chdir(original_cwd)


# ===================== TESTS FOR FUNCTION CALLS =====================

class TestMainFunctionCalls:
    """Tests verifying correct function call order using mocks."""
    
    def test_calls_get_encrypted_text(self, monkeypatch):
        """main() calls get_encrypted_text function."""
        monkeypatch.setattr(sys, 'argv', ['main.py'])
        
        with patch('main.get_encrypted_text') as mock_get, \
             patch('main.find_solution') as mock_find, \
             patch('main.save_results') as mock_save:
            
            mock_get.return_value = "encrypted"
            mock_find.return_value = ("decrypted", 1, ["v1", "v2"])
            
            main()
            
            mock_get.assert_called_once()
    
    def test_calls_find_solution_with_ciphertext(self, monkeypatch):
        """main() passes ciphertext to find_solution."""
        monkeypatch.setattr(sys, 'argv', ['main.py'])
        
        with patch('main.get_encrypted_text') as mock_get, \
             patch('main.find_solution') as mock_find, \
             patch('main.save_results') as mock_save:
            
            mock_get.return_value = "test_ciphertext"
            mock_find.return_value = ("decrypted", 1, ["v1"])
            
            main()
            
            mock_find.assert_called_once_with("test_ciphertext")
    
    def test_calls_save_results_with_solution(self, monkeypatch):
        """main() passes solution to save_results."""
        monkeypatch.setattr(sys, 'argv', ['main.py'])
        
        with patch('main.get_encrypted_text') as mock_get, \
             patch('main.find_solution') as mock_find, \
             patch('main.save_results') as mock_save:
            
            mock_get.return_value = "cipher"
            mock_find.return_value = ("best_text", 5, ["v1", "v2", "v3"])
            
            main()
            
            mock_save.assert_called_once_with("best_text", 5, ["v1", "v2", "v3"])


# ===================== TESTS FOR OUTPUT =====================

class TestMainOutput:
    """Tests verifying printed output."""
    
    def test_prints_all_versions(self, monkeypatch, tmp_path, capsys):
        """main() prints all 25 decryption versions."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("bcde", encoding="utf-8")
        
        monkeypatch.setattr(sys, 'argv', ['main.py', str(test_file)])
        
        try:
            main()
            captured = capsys.readouterr()
            
            # Should print 25 versions
            lines = [line for line in captured.out.split('\n') if line.strip()]
            # At least 25 lines for versions + solution info
            assert len(lines) >= 25
        finally:
            os.chdir(original_cwd)
    
    def test_prints_solution_info(self, monkeypatch, tmp_path, capsys):
        """main() prints decrypted message and shift info."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("epomj ezno yudndve", encoding="utf-8")
        
        monkeypatch.setattr(sys, 'argv', ['main.py', str(test_file)])
        
        try:
            main()
            captured = capsys.readouterr()
            
            assert "Odszyfrowana wiadomość:" in captured.out
            assert "Ilość przesunięć:" in captured.out
        finally:
            os.chdir(original_cwd)
