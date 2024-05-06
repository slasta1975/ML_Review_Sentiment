"""
This Python project performs sentiment analysis on movie reviews using a basic bag-of-words approach. 
It counts the occurrences of positive and negative words in the reviews to determine their sentiment. 
Reviews can be manually entered or loaded from saved text files. An advanced mode analysis is also possible, 
detecting negations in the analyzed review and inverting the sentiments of affected words, improving overall review analysis.

This script uses the following modules:
- `word_counter`: To count the occurrences of positive and negative words.
- `menu_handling`: To display the main menu and get user input.
- `review_handling`: To enter or read a review for analysis.
- `sentiment_analysis`: To calcualte review sentiment in either standard or advanced mode.
- `file_management`: To delete a review file.
"""

from word_counter import WordCounter
from menu_handling import display_menu
from review_handling import enter_or_read_review_for_analysis
from file_management import delete_review_file

POS_FILES_FEED = r"train\pos\*.txt"
NEG_FILES_FEED = r"train\neg\*.txt"

def main() -> None:
    """
    Main program flow for sentiment analysis.
    """
    word_counter = WordCounter()
    word_counter.count_words(POS_FILES_FEED, is_positive=True)
    word_counter.count_words(NEG_FILES_FEED, is_positive=False)

    while True:
        choice = display_menu()

        if choice == "1":
            enter_or_read_review_for_analysis(word_counter, is_enter_review=True)

        elif choice == "2":
            enter_or_read_review_for_analysis(word_counter, is_enter_review=False)

        elif choice == "3":
            delete_review_file()

        elif choice == "4":
            print("Exiting program...")
            break

        else:
            print("\nInvalid choice. Please enter a valid option (1/2/3/4).")

if __name__ == "__main__":
    main()