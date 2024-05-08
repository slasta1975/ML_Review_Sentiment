import re
from typing import List

PUNCTUATIONS = [
    ".",
    ",",
    "?",
    "!",
    ":",
    ";",
    " - ",
    " '",
    "' ",
    '"',
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "<br />",
]

def remove_punctuations(review: str) -> str:
    for punctuation in PUNCTUATIONS:
        review = review.replace(punctuation, " ")
    return review


def preprocess_review(review: str, advanced: bool = False) -> List[str]:
    sentences = re.split(r"[.!?]", review)
    all_words = []

    for sentence in sentences:
        sentence = sentence.strip()
        sentence = remove_punctuations(sentence)
        words = sentence.lower().split()

        if not advanced:
            all_words.extend(words)
            continue

        advanced_words = []
        negate = False

        for word in words:
            if (word in ["not", "no", "never", "neither", "nor"] or "n't" in word) or (
                "far" in word
                and len(words) > words.index(word) + 1
                and words[words.index(word) + 1] == "from"
            ):
                negate = True
            elif word == "only" and words[words.index(word) - 1] == "not":
                negate = False
            elif negate and word not in ["but", "however", "nevertheless"]:
                word = "not_" + word
            else:
                negate = False

            advanced_words.append(word)

        all_words.extend(advanced_words)

    return all_words