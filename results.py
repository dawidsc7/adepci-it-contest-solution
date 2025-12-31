import re


def save_results(best_text: str, correct_shift: int, all_versions: list) -> None:
    """
    Displays all decryption attempts, the best solution, and extracts email.
    Also saves the decrypted message to a file.
    
    Args:
        best_text (str): The correctly decrypted Polish message.
        correct_shift (int): The shift value used for decryption.
        all_versions (list): All 25 decryption attempts to display.
    """
    
    # Display all versions
    for version in all_versions:
        print(version)
    if not best_text:
        print("\n Nie udało się znaleźć rozwiązania.")
        return
    # Display the solution
    print(f"\nOdszyfrowana wiadomość: {best_text}")
    print(f"Ilość przesunięć: {correct_shift}")
    
    # Extract and display email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", best_text)
    if email_match:
        print(f"Email: {email_match.group()}")
    
    # Save to file
    with open("./solution.txt", "w", encoding="utf-8") as f:
        f.write(best_text)
