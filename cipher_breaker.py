from langdetect import detect, LangDetectException
from analyzer import calculate_score


def find_solution(ciphertext: str) -> tuple:
    """
    Tries all possible Caesar cipher shifts and finds the Polish message.
    
    Uses langdetect library to identify Polish text, then additionally
    filters using calculate_score function for better accuracy.
    
    Args:
        ciphertext (str): The encrypted text to decrypt.
        
    Returns:
        tuple: (best_text, correct_shift, all_versions)
            - best_text: The most likely Polish decryption
            - correct_shift: The shift value that produced best_text
            - all_versions: List of all 25 decryption attempts
    """
    best_text = ""
    max_score = 0
    correct_shift = 0
    all_versions = []
    candidates = []
    
    for shift in range(1, 26):
        candidate = decrypt_text(ciphertext, shift)
        candidate_score= calculate_score(candidate)
        candidates.append((candidate_score, shift, candidate))
        all_versions.append(candidate)
        
        try:
            if detect(candidate) == 'pl':
                score = calculate_score(candidate)
                if score > max_score:
                    max_score = score
                    correct_shift = shift
                    best_text = candidate
        except LangDetectException:
            continue
    if not best_text and candidates:
        candidates.sort(reverse=True, key=lambda x: x[0])
        max_score, correct_shift, best_text = candidates[0]    
        print(f"\nFALLBACK: langdetect nie wykrył polskiego tekstu")
        print(f"Użyto score-based detection")
        print(f"Najlepszy wynik: shift={correct_shift}, score={max_score}")
    return best_text, correct_shift, all_versions


def decrypt_text(text: str, shift: int) -> str:
    """
    Decrypts text encrypted with Caesar cipher by shifting letters left.
    
    Non-alphabetic characters (spaces, punctuation, @) remain unchanged.
    
    Args:
        text (str): The ciphertext to decrypt.
        shift (int): Number of positions to shift letters.
        
    Returns:
        str: The decrypted text.
    """
    result = ""
    characters = list(text)
    
    for char in characters:
        if char.isalpha():
            position = ord(char) - ord('A') if char.isupper() else ord(char) - ord('a')
            new_position = (position - shift) % 26
            new_char = chr(new_position + ord('A') if char.isupper() else new_position + ord('a'))
            result += new_char
        else:
            result += char
            
    return result
