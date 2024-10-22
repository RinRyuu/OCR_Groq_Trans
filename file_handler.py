def save_translation(text: str, filename: str = "translation.txt") -> None:
    """Save translated text to a file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)