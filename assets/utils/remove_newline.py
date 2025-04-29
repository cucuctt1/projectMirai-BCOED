import re

def clean_text(text: str) -> str:
    text = text.replace("\n", " ")  # Replace newlines with space
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text.strip()