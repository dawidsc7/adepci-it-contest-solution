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

    words = text.lower().split()
    score = 0
    
    for word in words:
        if word in polish_keywords:
            score += 1
    return score