import os


def get_encrypted_text(source: str | None = None) -> str:
    """
    Reads encrypted text from user-given file or returns provided string.
    
    Args:
        source(str, optional): Path to file or direct ciphertext.
        If None, uses default 'ciphertext.txt'
    
    Returns:
        str: The encrypted message using Caesar cipher.
        
    Raises:
        FileNotFoundError: If source looks like a file path but file doesn't exist.
        ValueError: If source is empty or None with no default file.
    """
    if source is None:
        source = "ciphertext.txt"

    file_extensions = ('.txt', '.csv', '.dat', '.text')
    looks_like_file = source.lower().endswith(file_extensions)
    
    if os.path.isfile(source):
        with open(source, "r", encoding="utf-8") as file:
            text = file.read().strip()
            if not text:
                raise ValueError(f"Plik '{source}' jest pusty.")
            return text
    elif looks_like_file:
        raise FileNotFoundError(f"Plik '{source}' nie istnieje.")
    else:
        text = source.strip()
        if not text:
            raise ValueError("Podany tekst jest pusty.")
        return text
