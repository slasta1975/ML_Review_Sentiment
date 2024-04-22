import pytest
from main import *


@pytest.fixture
def temp_review_files_path(tmpdir):
    return tmpdir.mkdir("review_files")


def test_preprocess_review():
    review = "This is a sample review, with punctuations! And special characters?"
    preprocessed_review = preprocess_review(review)
    expected_result = ['this', 'is', 'a', 'sample', 'review', 'with', 'punctuations', 'and', 'special', 'characters']
    assert preprocessed_review == expected_result

def test_advanced_preprocess_review():
    review = "This is not a bad movie. It's far from bad."
    advanced_preprocessed_review = advanced_preprocess_review(review)
    expected_result = ['this', 'is', 'not', 'not_a', 'not_bad', 'not_movie', "it's", 'far', 'not_from', 'not_bad']
    assert advanced_preprocessed_review == expected_result

def test_get_next_review_file(temp_review_files_path):
    # Create test review files
    file1 = temp_review_files_path.join("Review1.txt")
    file1.write("Sample review 1")
    file2 = temp_review_files_path.join("Review2.txt")
    file2.write("Sample review 2")

    next_review_file = get_next_review_file(temp_review_files_path)
    expected_result = "Review3.txt"
    assert next_review_file == expected_result

def test_compute_sentiment():
    word_counter = [{"good": 5, "great": 3}, {"bad": 2, "terrible": 4}]
    review = ["good", "movie"]
    sentiment, sentiment_details = compute_sentiment(review, word_counter)
    assert round(sentiment, 2) == 0.5
    expected_sentiment_details = [("good", 1.0), ("movie", 0.0)]
    assert sentiment_details == expected_sentiment_details

