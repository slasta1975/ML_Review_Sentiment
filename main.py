"""
This Python project performs sentiment analysis on movie reviews using a basic bag-of-words approach. It counts the occurrences of positive and negative words in the reviews to determine their sentiment. Reviews can be manually entered or loaded from saved text files. An advanced mode analysis is also possible which can detect negation in the analysed review and inverse sentiments of affected words thus improving the whole review sentiment analysis.
"""

from word_counter import WordCounter
from sentiment_analysis import preprocess_review, compute_sentiment, print_sentiment, print_sentiment_details
from  file_management  import read_review_file, save_review, delete_review_file

POS_FILES_FEED = r"train\pos\*.txt"
NEG_FILES_FEED = r"train\neg\*.txt"
REVIEW_FILES_PATH = r"reviews"

def enter_or_read_review_for_analysis(
    word_counter: WordCounter, is_enter_review: bool
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


def main() -> None:
    """
    Main program flow for sentiment analysis.
    """
    word_counter = WordCounter()
    word_counter.count_words(POS_FILES_FEED, is_positive=True)
    word_counter.count_words(NEG_FILES_FEED, is_positive=False)

    while True:
        print("\n----------")
        print("Main Menu:")
        print("----------")
        print("1. Enter your review for analysis")
        print("2. Read a review file for analysis")
        print("3. Delete a review file")
        print("4. Exit")
        print("----------")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            enter_or_read_review_for_analysis(word_counter, is_enter_review=True)

        elif choice == "2":
            enter_or_read_review_for_analysis(word_counter, is_enter_review=False)

        elif choice == "3":
            delete_review_file(REVIEW_FILES_PATH)

        elif choice == "4":
            print("Exiting program...")
            break

        else:
            print("\nInvalid choice. Please enter a valid option (1/2/3/4).")

if __name__ == "__main__":
    main()