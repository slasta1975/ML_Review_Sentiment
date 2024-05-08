from sentiment_analysis import WordCounter
from file_operations import delete_review_file
from review_analysis import enter_or_read_review_for_analysis


def main():
    word_counter = WordCounter()
    word_counter.count_words(r"train\pos\*.txt", True)
    word_counter.count_words(r"train\neg\*.txt", False)

    while True:
        print("\nMain Menu:")
        print("1. Enter a review for analysis")
        print("2. Read a review file for analysis")
        print("3. Delete a review file")
        print("4. Exit")

        choice = input("\nEnter your choice (1/2/3/4): ").strip()
        if choice == "1":
            enter_or_read_review_for_analysis(word_counter, True)
        elif choice == "2":
            enter_or_read_review_for_analysis(word_counter, False)
        elif choice == "3":
            delete_review_file("reviews")
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("\nInvalid choice, please try again.")


if __name__ == "__main__":
    main()