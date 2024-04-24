from sentiment_analysis import preprocess_review, compute_sentiment, print_sentiment, print_sentiment_details
from file_management import read_review_file, save_review

REVIEW_FILES_PATH = r"reviews"


def enter_or_read_review_for_analysis(
    word_counter, is_enter_review: bool
) -> None:
    """
    Prompts the user to enter a review for analysis or reads a review file for analysis.
    """
    if is_enter_review:
        review = input("\nProvide your review: ")
        if len(review) == 0:
            print("\nNo review for analysis")
            input("\nPress a key to return to the main menu...")
            return
    else:
        review = read_review_file(REVIEW_FILES_PATH)
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

    if input("\nAre you interested in per-word sentiment details? [y/n]: ").lower() == "y":
        print_sentiment_details(sentiment_details)

    if is_enter_review:
        if input("\nDo you want to save this review? [y/n]: ").lower() == "y":
            save_review(review, REVIEW_FILES_PATH)

    input("\nPress a key to return to the main menu...")