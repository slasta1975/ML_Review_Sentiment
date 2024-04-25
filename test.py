import pytest
from main import *
from sentiment_analysis import *
from file_management import *
from review_handling import *
from menu_handling import *
from word_counter import *


@pytest.fixture
def temp_review_files_path(tmpdir):
    return tmpdir.mkdir("review_files")


def test_preprocess_review():
    review = "This is a sample review, with punctuations! And special characters?"
    preprocessed_review = preprocess_review(review, advanced=False)
    expected_result = ['this', 'is', 'a', 'sample', 'review', 'with', 'punctuations', 'and', 'special', 'characters']
    assert preprocessed_review == expected_result


def test_advanced_preprocess_review():
    review = "This is not a bad movie. It's far from bad."
    advanced_preprocessed_review = preprocess_review(review, advanced=True)
    expected_result = ['this', 'is', 'not', 'not_a', 'not_bad', 'not_movie', "it's", 'far', 'not_from', 'not_bad']
    assert advanced_preprocessed_review == expected_result


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



