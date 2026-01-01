import string

# Manually defined stopwords for MVP
STOPWORDS = {
    "to", "the", "a", "an", "is", "are", "am",
    "do", "does", "did", "drink"
}

def text_to_gloss(text: str) -> list[str]:
    """
    Convert natural language text into sign-language-friendly gloss.

    Args:
        text (str): Input sentence from ASR

    Returns:
        list[str]: List of gloss tokens
    """

    # 1. Lowercase text
    text = text.lower()

    # 2. Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # 3. Tokenize
    words = text.split()

    # 4. Remove stopwords
    filtered_words = [
        word for word in words if word not in STOPWORDS
    ]

    # 5. Convert to uppercase gloss
    gloss_tokens = [word.upper() for word in filtered_words]

    return gloss_tokens


# Simple test
if __name__ == "__main__":
    test_sentence = "I want to drink water"
    gloss = text_to_gloss(test_sentence)
    print(gloss)
    
