from lingua import Language, LanguageDetectorBuilder

# Build detector with all languages for accurate Polish detection
# Using detect_language_of() to identify Polish candidates
detector = LanguageDetectorBuilder.from_all_languages().build()


def find_solution(ciphertext: str) -> tuple[str, int, list[str]]:
    """
    Tries all possible Caesar cipher shifts and finds the Polish message.
    
    Uses lingua-py library to detect language of each candidate.
    Selects the candidate detected as Polish with highest confidence.
    
    Args:
        ciphertext (str): The encrypted text to decrypt.
        
    Returns:
        tuple: (best_text, correct_shift, all_versions)
            - best_text: The most likely Polish decryption
            - correct_shift: The shift value that produced best_text
            - all_versions: List of all 26 decryption attempts
    """
    best_text = ""
    best_confidence = 0.0
    correct_shift = 0
    all_versions = []
    
    for shift in range(26):
        candidate = decrypt_text(ciphertext, shift)
        all_versions.append(candidate)
        
        # Check if detected language is Polish
        detected_language = detector.detect_language_of(candidate)
        if detected_language == Language.POLISH:
            confidence = detector.compute_language_confidence(candidate, Language.POLISH)
            if confidence > best_confidence:
                best_confidence = confidence
                best_text = candidate
                correct_shift = shift
    
    # Fallback: if no Polish detected, return original text (shift=0)
    if not best_text and all_versions:
        best_text = all_versions[0]
        correct_shift = 0
    
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
