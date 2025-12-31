def calculate_score(text: str) -> int:
    """
    Calculates a score for the given text based on Polish keywords.
    Higher score indicates higher probability of being Polish text.
    
    Args:
        text (str): The text to analyze.
        
    Returns:
        int: Score based on Polish keyword matches.
    """
    polish_keywords = ["i", "w", "z", "na", "do", "jest", "jak", "aby", "czy", "jesli", "to", "nie",
    "się", "od", "za", "po", "dla", "przy", "ze", "oraz", "lub", "ale", "już", "tak", "było", "być", "może", "można"]
    
    for char in [".", ",", ":", "@"]:
        text = text.replace(char, " ")

    words = text.split()
    score = 0
    
    for word in words:
        if word in polish_keywords:
            score += 1
    if has_polish_characters(text):
        score += 3
    return score

def has_polish_characters(text: str) -> bool:
    """
    Checks if the text has polish special characters.
    
    Args:
        text (str): The text to analyze.
        
    Returns:
        bool: True if the text contains polish special characters, False otherwise.
    """
    polish_chars = "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ"
    
    for char in polish_chars:
        if char in text:
            return True
    
    return False