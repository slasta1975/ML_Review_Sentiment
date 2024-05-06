"""
This module contains functions for handling movie reviews in a sentiment analysis application.

Functions:
- `preprocess_review`: Processes a movie review into individual words, with an option for
  advanced processing that adds "not_" prefixes to words following negations.
- `enter_or_read_review_for_analysis`: Prompts the user to enter a new review for analysis
  or reads an existing review from a file. It also allows users to choose between basic
  and advanced sentiment analysis and includes options for saving the review and viewing
  detailed sentiment information.
"""

import re
from typing import List
from file_management import read_review_file, save_review
from word_counter import WordCounter, remove_punctuations
from sentiment_analysis import (
    compute_sentiment,
    print_sentiment,
    print_sentiment_details,
)


def preprocess_review(review: str, advanced: bool = False) -> List[str]:
    """
    Splits the review into words after removing punctuations.
    If 'advanced' is True, it adds a "not_" prefix to words following negations.
    """
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


def enter_or_read_review_for_analysis(
    word_counter: WordCounter, is_enter_review: bool
) -> None:
    """
    Prompts the user to enter or read a review for analysis.
    """
    if is_enter_review:
        review = input("\nProvide your review: ")
        if len(review) == 0:
            print("\nNo review for analysis.")
            return
    else:
        review = read_review_file("reviews")
        if not review:
            return

    advanced_analysis = input(
        "\nDo you want to perform advanced sentiment analysis? [y/n]: "
    )
    advanced = advanced_analysis.lower() == "y"

    preprocessed_review = preprocess_review(review, advanced=advanced)
    sentiment, sentiment_details = compute_sentiment(
        preprocessed_review, word_counter, advanced=advanced
    )

    print_sentiment(sentiment)

    if (
        input("\nAre you interested in per-word sentiment details? [y/n]: ").lower()
        == "y"
    ):
        print_sentiment_details(sentiment_details)

    if not advanced:
        advanced_analysis = input(
            "\nDo you want to perform advanced sentiment analysis after all? [y/n]: "
        )
        if advanced_analysis.lower() == "y":
            preprocessed_review = preprocess_review(review, advanced=True)
            sentiment, sentiment_details = compute_sentiment(
                preprocessed_review, word_counter, advanced=True
            )
            print_sentiment(sentiment)
            if (
                input(
                    "\nAre you interested in per-word sentiment details? [y/n]: "
                ).lower()
                == "y"
            ):
                print_sentiment_details(sentiment_details)

    if is_enter_review:
        if input("\nDo you want to save this review? [y/n]: ").lower() == "y":
            save_review(review, "reviews")

    input("\nPress a key to return to the main menu...")
