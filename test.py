import pytest
import os
import tempfile
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
    pos_words_count = {"good": 5, "great": 3}
    neg_words_count = {"bad": 2, "terrible": 4}
    review = ["good", "movie"]
    sentiment, sentiment_details = compute_sentiment(review, pos_words_count, neg_words_count)
    assert round(sentiment, 2) == 0.5
    expected_sentiment_details = [("good", 1.0), ("movie", 0.0)]
    assert sentiment_details == expected_sentiment_details

# def test_list_review_files(temp_review_files_path):
#     # Create test review files
#     file1 = temp_review_files_path.join("Review1.txt")
#     file1.write("Sample review 1")
#     file2 = temp_review_files_path.join("Review2.txt")
#     file2.write("Sample review 2")

#     with tempfile.TemporaryDirectory() as tmpdir:
#         list_review_files(tmpdir)

# def test_read_review_file(temp_review_files_path):
#     # Create test review files
#     file1 = temp_review_files_path.join("Review1.txt")
#     file1.write("Sample review 1")
#     file2 = temp_review_files_path.join("Review2.txt")
#     file2.write("Sample review 2")

#     with tempfile.TemporaryDirectory() as tmpdir:
#         review_content = read_review_file(tmpdir)
#         assert review_content == "Sample review 1"

# def test_delete_review_file(temp_review_files_path):
#     # Create test review files
#     file1 = temp_review_files_path.join("Review1.txt")
#     file1.write("Sample review 1")
#     file2 = temp_review_files_path.join("Review2.txt")
#     file2.write("Sample review 2")
#
#    delete_review_file(temp_review_files_path)
#
#    # Check if the file was deleted
#    assert not os.listdir(temp_review_files_path)