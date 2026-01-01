import string

# Manually defined stopwords for MVP (26 total)
STOPWORDS = {
    # Articles & Determiners
    "to", "the", "a", "an",

    # Common verbs (dropped in ASL)
    "is", "are", "am", "do", "does", "did", "drink",

    # Additional determiners
    "this", "that", "these", "those", "some",

    # Auxiliary verbs
    "will", "would", "can", "could", "should",

    # Prepositions (common in English but dropped in ASL)
    "at", "in", "on", "of", "for"
}

SYNONYMS = {
    # Pronouns
    "I": "ME",
    "MY": "ME",
    "MINE": "ME",
    "HIM": "HE",
    "HER": "SHE",
    "US": "WE",
    "THEM": "THEY",

    # Time
    "TODAY": "NOW",

    # Actions (verb variations)
    "DRINKING": "WATER",
    "EATING": "EAT",
    "WORKING": "WORK",
    "LOOKING": "LOOK",

    # Greetings
    "HI": "HELLO",
    "HEY": "HELLO",
    "THANKS": "THANK-YOU",
    "THANK": "THANK-YOU",

    # Questions
    "HOW": "WHAT",

    # Affirmations
    "OK": "YES",
    "OKAY": "YES",
    "FINE": "GOOD",

    # Negations
    "NOT": "NO",
    "NOPE": "NO",
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
    
    # 6. Replace synonyms
    gloss_tokens = [SYNONYMS.get(word, word) for word in gloss_tokens]

    return gloss_tokens


# Simple test
if __name__ == "__main__":
    test_sentence = "I want to drink water"
    gloss = text_to_gloss(test_sentence)
    print(gloss)
    
