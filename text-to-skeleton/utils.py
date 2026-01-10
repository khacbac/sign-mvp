from typing import List
from spoken_to_signed.text_to_gloss.types import Gloss
from spoken_to_signed.text_to_gloss.common import load_spacy_model

LANGUAGE_MODELS_SPACY = {
    "de": "de_core_news_lg",
    "fr": "fr_core_news_lg",
    "it": "it_core_news_lg",
    "en": "en_core_web_lg",
}


def text_to_gloss__spacy_lemma(text: str, language: str, ignore_punctuation: bool = False, **unused_kwargs) -> List[Gloss]:
    if language not in LANGUAGE_MODELS_SPACY:
        raise NotImplementedError("Don't know language '%s'." % language)

    model_name = LANGUAGE_MODELS_SPACY[language]

    # disable unnecessary components to make lemmatization faster

    spacy_model = load_spacy_model((model_name,), disable=("parser", "ner"))

    doc = spacy_model(text)

    glosses = []  # type: Gloss

    for token in doc:
        if ignore_punctuation is True:
            if token.is_punct:
                continue

        gloss = (token.text, token.lemma_)
        glosses.append(gloss)

    return [glosses]
