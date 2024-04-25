"""
This module defines the `WordCounter` class for counting word occurrences in a set of text files,
which can be used for sentiment analysis. It also provides a utility function to remove specified
punctuations from text.

The `WordCounter` class maintains separate dictionaries for positive and negative reviews, allowing
for word-based sentiment analysis. It supports reading text files to count word occurrences and stores
the results in dictionaries for later retrieval.

The `remove_punctuations` function allows removing various punctuations from text to normalize it
for easier processing.
"""

import glob
from typing import Dict

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


def remove_punctuations(text: str) -> str:
    """
    Removes specified punctuations from the given text.
    """
    for punctuation in PUNCTUATIONS:
        text = text.replace(punctuation, " ")
    return text


class WordCounter:
    """
    A class to count word occurrences in a set of text files. It maintains separate
    dictionaries to store word counts for positive and negative reviews, allowing
    for sentiment analysis based on these counts.
    """

    def __init__(self):
        self.pos_words_count: Dict[str, int] = {}
        self.neg_words_count: Dict[str, int] = {}

    def count_words(self, path_pattern: str, is_positive: bool) -> None:
        """
        Calculates the number of times a word has been used in training positive and negative reviews.
        Updates dictionaries with review words and usage counters.
        """
        files = glob.glob(path_pattern)
        for file in files:
            with open(file, encoding="utf-8") as stream:
                content = stream.read()
            preprocessed_content = remove_punctuations(content).lower().split()
            for word in set(preprocessed_content):
                if is_positive:
                    self.pos_words_count[word] = self.pos_words_count.get(word, 0) + 1
                else:
                    self.neg_words_count[word] = self.neg_words_count.get(word, 0) + 1