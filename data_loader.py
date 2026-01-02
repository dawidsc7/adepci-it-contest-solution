import os
def get_encrypted_text(source=None):
    """
    Reads encrypted text from user-given file or returns provided string.
    
    Args:
        source(str, optional): Path to file or direct ciphertext.
        If None, uses default 'ciphertext.txt'
    
    Returns:
        str: The encrypted message using Caesar cipher.
    """
    if source is None:
       source = "ciphertext.txt"
    if os.path.isfile(source):
        with open(source, "r", encoding="utf-8") as file:
            return file.read().strip()
    else:
        return source.strip()
