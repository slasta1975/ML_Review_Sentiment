import pytest
import os
import glob
from main import (
    preprocess_review,
    WordCounter,
    compute_sentiment,
    list_review_files,
    save_review,

    get_next_review_file,
)

# Constants
POS_TEST_PATH = "test/pos"
NEG_TEST_PATH = "test/neg"
REVIEW_FILES_PATH = "test/reviews"
POS_FILES_FEED = "test/pos/*.txt"
NEG_FILES_FEED = "test/neg/*.txt"


@pytest.fixture(scope="module")
def setup_files():
    """
    Fixture to set up test files.
    """
    os.makedirs(POS_TEST_PATH, exist_ok=True)
    os.makedirs(NEG_TEST_PATH, exist_ok=True)
    os.makedirs(REVIEW_FILES_PATH, exist_ok=True)

    # Sample positive and negative test files
    with open(f"{POS_TEST_PATH}/pos_test.txt", "w") as pos_test_file:
        pos_test_file.write("This is a great movie.")

    with open(f"{NEG_TEST_PATH}/neg_test.txt", "w") as neg_test_file:
        neg_test_file.write("This is a terrible movie.")

    yield  # yield to test cases

    # Cleanup files after tests
    for file in glob.glob(f"{REVIEW_FILES_PATH}/*.txt"):
        os.remove(file)

    os.remove(f"{POS_TEST_PATH}/pos_test.txt")
    os.remove(f"{NEG_TEST_PATH}/neg_test.txt")
    os.rmdir(REVIEW_FILES_PATH)
    os.rmdir(POS_TEST_PATH)
    os.rmdir(NEG_TEST_PATH)



def test_preprocess_review():
    """
    Test the basic review preprocessing.
    """
    review = "Hello, World! This is a test. Isn't it great?"
    expected = ["hello", "world", "this", "is", "a", "test", "isn't", "it", "great"]
    assert preprocess_review(review) == expected


def test_advanced_preprocess_review():
    """
    Test advanced preprocessing with negations.
    """
    review = "I can't believe it! It is not true."
    expected = ["i", "can't", "not_believe", "not_it", "not_it", "not_is", "not", "not_true"]
    assert preprocess_review(review, advanced=True) == expected


def test_word_counter(setup_files):
    """
    Test word counting functionality for positive and negative reviews.
    """
    wc = WordCounter()
    wc.count_words(POS_FILES_FEED, is_positive=True)
    wc.count_words(NEG_FILES_FEED, is_positive=False)

    assert wc.pos_words_count["great"] == 1
    assert wc.neg_words_count["terrible"] == 1


def test_compute_sentiment():
    """
    Test sentiment computation with a word counter.
    """
    wc = WordCounter()
    wc.pos_words_count = {"great": 1}
    wc.neg_words_count = {"terrible": 1}

    review = ["great", "terrible"]
    sentiment, details = compute_sentiment(review, wc)

    # Check if the average sentiment is correct
    assert sentiment == 0.0  # Equal positive and negative
    assert len(details) == 2

def test_advanced_compute_sentiment():
    """
    Test sentiment computation with a word counter.
    """
    wc = WordCounter()
    wc.pos_words_count = {"not": 1, "or": 1}
    wc.neg_words_count = {"lousy": 5, "terrible": 5}

    review = [ "not", "not_lousy", "not_or", "not_terrible"]
    sentiment, details = compute_sentiment(review, wc, advanced=True)

    # Check if the average sentiment is correct
    assert sentiment == 0.5  
    assert len(details) == 4


def test_save_review(setup_files):
    """
    Test saving a review file and ensure it is created correctly.
    """
    review_text = "This is a test review."
    save_review(review_text, REVIEW_FILES_PATH)

    files = list_review_files(REVIEW_FILES_PATH)
    assert len(files) == 1  # Only one file should exist


def test_get_next_review_file(setup_files):
    """
    Test to get the name of the next review file.
    """
    next_file = get_next_review_file(REVIEW_FILES_PATH)
    assert next_file == "Review2.txt"  # The first file created in test_save_review is "Review1.txt", so the next should be "Review2.txt"