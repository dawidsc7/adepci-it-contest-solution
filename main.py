from data_loader import get_encrypted_text
from cipher_breaker import find_solution
from results import save_results
import sys

def main():
    """
    Main entry point for the Caesar cipher breaker program.

    Usage:
        python main.py                # Uses default ciphertext.txt
        python main.py myfile.txt     # Uses custom file
        python main.py "text..."      # Uses direct text

    1. Loads the encrypted text
    2. Finds the correct decryption using brute-force + language detection
    3. Saves and displays the results
    """
    
    source = sys.argv[1] if len(sys.argv) > 1 else None
    ciphertext = get_encrypted_text(source)
    best_text, correct_shift, all_versions = find_solution(ciphertext)
    save_results(best_text, correct_shift, all_versions)


if __name__ == "__main__":
    main()