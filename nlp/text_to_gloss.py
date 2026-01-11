import string
import re

# Configuration constants
DEFAULT_MAX_CHUNK_WORDS = 15
MAX_INPUT_LENGTH = 1000

# Manually defined stopwords for MVP (expanded)
STOPWORDS = {
    # Articles & Determiners
    "to",
    "the",
    "a",
    "an",
    # Common verbs (dropped in ASL)
    "is",
    "are",
    "am",
    "do",
    "does",
    "did",
    "drink",
    "was",
    "were",
    "been",
    "being",
    # Additional determiners
    "this",
    "that",
    "these",
    "those",
    "some",
    "any",
    "each",
    "every",
    # Auxiliary verbs
    "will",
    "would",
    "can",
    "could",
    "should",
    "may",
    "might",
    "must",
    # Prepositions (common in English but dropped in ASL)
    "at",
    "in",
    "on",
    "of",
    "for",
    "with",
    "from",
    "by",
    "about",
    # Conjunctions (often simplified in ASL)
    "and",
    "but",
    "or",
    "so",
    "if",
}

SYNONYMS = {
    # Pronouns
    "I": "ME",
    "MY": "ME",
    "MINE": "ME",
    "HIM": "HE",
    "HER": "SHE",
    "HIS": "HE",
    "HERS": "SHE",
    "US": "WE",
    "THEM": "THEY",
    "THEIR": "THEY",
    "OUR": "WE",
    # Time expressions
    "TODAY": "NOW",
    "TONIGHT": "NOW",
    "LATER": "TIME",
    # Actions (verb variations)
    "DRINKING": "WATER",
    "EATING": "EAT",
    "WORKING": "WORK",
    "LOOKING": "LOOK",
    "KNOWING": "KNOW",
    "SEEING": "SEE",
    "GOING": "GO",
    "COMING": "COME",
    "GIVING": "GIVE",
    "TAKING": "TAKE",
    "WANTING": "WANT",
    "NEEDING": "NEED",
    "HELPING": "HELP",
    "LEARNING": "LEARN",
    "STOPPING": "STOP",
    "FINISHING": "FINISH",
    # Past tense (ASL often uses time markers instead)
    "WENT": "GO",
    "CAME": "COME",
    "SAW": "SEE",
    "ATE": "EAT",
    "GAVE": "GIVE",
    "TOOK": "TAKE",
    "KNEW": "KNOW",
    "LOVED": "LOVE",
    "HELPED": "HELP",
    "LEARNED": "LEARN",
    "STOPPED": "STOP",
    "FINISHED": "FINISH",
    "WORKED": "WORK",
    "WANTED": "WANT",
    "NEEDED": "NEED",
    # Greetings & Social
    "HI": "HELLO",
    "HEY": "HELLO",
    "THANKS": "THANK-YOU",
    "THANK": "THANK-YOU",
    "BYE": "GOODBYE",
    "GOODBYE": "FINISH",
    # Questions
    "HOW": "WHAT",
    # Affirmations
    "OK": "YES",
    "OKAY": "YES",
    "FINE": "GOOD",
    "GREAT": "GOOD",
    "NICE": "GOOD",
    # Negations
    "NOT": "NO",
    "NOPE": "NO",
    "DON'T": "NO",
    "DONT": "NO",
    "DOESN'T": "NO",
    "DOESNT": "NO",
    # Common phrases
    "MOM": "MOTHER",
    "DAD": "FATHER",
    "MOMMY": "MOTHER",
    "DADDY": "FATHER",
}


def chunk_long_text(text: str, max_words: int = DEFAULT_MAX_CHUNK_WORDS) -> list[str]:
    """
    Break long text into manageable chunks for signing.

    Args:
        text (str): Input text
        max_words (int): Maximum words per chunk

    Returns:
        list[str]: List of text chunks
    """
    # Split by common sentence boundaries
    sentences = re.split(r"[.!?]+", text)
    chunks = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        words = sentence.split()

        # If sentence is short enough, keep it as one chunk
        if len(words) <= max_words:
            chunks.append(sentence)
        else:
            # Split long sentence by commas or at word boundaries
            comma_parts = sentence.split(",")
            for part in comma_parts:
                part = part.strip()
                if not part:
                    continue

                part_words = part.split()
                if len(part_words) <= max_words:
                    chunks.append(part)
                else:
                    # Force split at max_words boundary
                    for i in range(0, len(part_words), max_words):
                        chunk_words = part_words[i : i + max_words]
                        chunks.append(" ".join(chunk_words))

    return chunks if chunks else [text]


def validate_input(text: str) -> tuple[bool, str]:
    """
    Validate input text for processing.

    Args:
        text (str): Input text

    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Input text is empty"

    if len(text) > MAX_INPUT_LENGTH:
        return False, f"Input text is too long (max {MAX_INPUT_LENGTH} characters)"

    # Check if text has at least some alphabetic characters
    if not any(c.isalpha() for c in text):
        return False, "Input text contains no valid words"

    return True, ""


def text_to_gloss(
    text: str, chunk: bool = True, max_chunk_words: int = DEFAULT_MAX_CHUNK_WORDS
) -> list[str]:
    """
    Convert natural language text into sign-language-friendly gloss.

    Args:
        text (str): Input sentence from ASR
        chunk (bool): Whether to chunk long text
        max_chunk_words (int): Maximum words per chunk if chunking is enabled

    Returns:
        list[str]: List of gloss tokens
    """
    # Validate input
    is_valid, error_msg = validate_input(text)
    if not is_valid:
        raise ValueError(f"Invalid input: {error_msg}")

    # Chunk if needed (for very long inputs)
    if chunk and len(text.split()) > max_chunk_words:
        chunks = chunk_long_text(text, max_chunk_words)
        # Process each chunk and combine results
        all_glosses = []
        for chunk_text in chunks:
            chunk_glosses = _process_text_to_gloss(chunk_text)
            all_glosses.extend(chunk_glosses)
        return all_glosses
    else:
        return _process_text_to_gloss(text)


def _process_text_to_gloss(text: str) -> list[str]:
    """
    Internal function to process text to gloss (no validation or chunking).

    Args:
        text (str): Input text

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
    filtered_words = [word for word in words if word not in STOPWORDS]

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

    # Test chunking
    long_text = "Hello my friend, I want to go to school tomorrow because I need to learn more about work and help my mother with food at home"
    print("\nLong text test:")
    print(f"Input: {long_text}")
    chunked_gloss = text_to_gloss(long_text, chunk=True)
    print(f"Output: {chunked_gloss}")
