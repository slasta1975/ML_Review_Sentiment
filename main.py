import glob
import os
import re
from typing import List, Tuple, Dict

POS_FILES_FEED: str = r"train\pos\*.txt"
NEG_FILES_FEED: str = r"train\neg\*.txt"
REVIEW_FILES_PATH: str = r"reviews"
PUNCTUATIONS: List[str] = [
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


class WordCounter:
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
            preprocessed_review = remove_punctuations(content).lower().split()
            for word in set(preprocessed_review):
                if is_positive:
                    self.pos_words_count[word] = self.pos_words_count.get(word, 0) + 1
                else:
                    self.neg_words_count[word] = self.neg_words_count.get(word, 0) + 1


def remove_punctuations(review: str) -> str:
    """
    Removes specified punctuations from a given sentence.
    """
    for punctuation in PUNCTUATIONS:
        review = review.replace(punctuation, " ")
    return review


def preprocess_review(review: str, advanced: bool = False) -> List[str]:
    """
    Splits the review into sentences using a regular expression to account for multiple delimiters.
    Returns a list of lower-case words without punctuations listed in PUNCTUATIONS.
    If 'advanced' is True, it adds a "not_" prefix to words following negations and processes negation-related words within the processed sentence.
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
            if word in ["not", "no", "never", "neither", "nor"] or "n't" in word:
                negate = True
            elif (
                "far" in word
                and len(words) > words.index(word) + 1
                and words[words.index(word) + 1] == "from"
            ):
                negate = True
            elif negate and word == "only":
                negate = False
            elif negate and word not in ["but", "however", "nevertheless"]:
                word = "not_" + word
            else:
                negate = False

            advanced_words.append(word)

        all_words.extend(advanced_words)

    return all_words


def compute_sentiment(
    review: List[str],
    word_counter: WordCounter,
    advanced: bool = False,
) -> Tuple[float, List[Tuple[str, float]]]:
    """
    Compute the sentiment of a review based on positive and negative word counts.
    """
    cumulative_sentiment = 0
    sentiment_details = []
    for word in review:
        if advanced and word.startswith("not_"):
            original_word = word[4:]  # Remove "not_" prefix
        else:
            original_word = word
        pos_counter = word_counter.pos_words_count.get(original_word, 0)
        neg_counter = word_counter.neg_words_count.get(original_word, 0)
        total = pos_counter + neg_counter
        if total == 0:
            word_sentiment = 0
        else:
            if advanced and word.startswith("not_"):
                word_sentiment = -1 * (pos_counter - neg_counter) / total
            else:
                word_sentiment = (pos_counter - neg_counter) / total
        cumulative_sentiment += word_sentiment
        sentiment_details.append((word, word_sentiment))
    average_sentiment = cumulative_sentiment / len(review)
    return average_sentiment, sentiment_details


def print_sentiment(sentiment: float) -> None:
    rounded_sentiment = round(sentiment, 2)
    if rounded_sentiment > 0:
        verdict = "positive"
    elif rounded_sentiment == 0:
        verdict = "neutral"
    else:
        verdict = "negative"
    print("\n------------------------------------------")
    print(f"This review is {verdict}, sentiment = {sentiment:.2f}")
    print("------------------------------------------")


def print_sentiment_details(sentiment_details: List[Tuple[str, float]]) -> None:
    print("\n---------------------------")
    print("Per word sentiment details:")
    print("---------------------------")
    for word, word_sentiment in sentiment_details:
        print(f"{word}: {word_sentiment:.2f}")
    print("---------------------------")


def list_review_files(review_files_path: str) -> List[str]:
    """
    Lists the review files available in the provided path along with their first sentences.
    """
    try:
        files = [
            file for file in os.listdir(review_files_path) if file.endswith(".txt")
        ]
        if not files:
            print("\nNo review files found.")
            input("\nPress a key to the main menu... ")
            return None
        sorted_files = sorted(
            files, key=lambda x: int(x.split("Review")[1].split(".")[0])
        )
        print("\n--------------------------------------")
        print("Review files found in the directory:")
        print("--------------------------------------")
        for i, file_name in enumerate(sorted_files, 1):
            with open(
                os.path.join(review_files_path, file_name), "r", encoding="utf-8"
            ) as file:
                content = file.read()
                sentences = re.split(r"[.!?]", content)
                if len(sentences) > 1:
                    first_sentence = sentences[0] + ("..." if sentences[1] else "")
                else:
                    first_sentence = content.strip()
                print(f"{i}. {file_name} - {first_sentence}")
        print("--------------------------------------")
        return sorted_files
    except FileNotFoundError:

        print("\nDirectory not found. Please make sure the directory exists.\n")
        return None


def get_user_choice(files: List[str], prompt: str) -> int:
    """
    Prompts the user to enter a choice and validates the input.
    Returns a valid choice as an integer or None if the user chooses to exit.
    """
    print(prompt, end="")
    while True:
        choice = input().strip()
        if choice == "":
            print("\nReturning to the main menu...")
            return None

        try:
            choice_int = int(choice)
            if 1 <= choice_int <= len(files):
                return choice_int
            else:
                print(
                    "\nInvalid choice. Please enter a number within the range:", end=""
                )
        except ValueError:
            print("\nInvalid input. Please enter a valid number:", end="")


def read_review_file(review_files_path: str) -> str:
    """
    Reads a review file from the provided path and returns its content.
    """
    files = list_review_files(review_files_path)
    if not files:
        return None

    choice = get_user_choice(
        files,
        "\nEnter the number of the review file you want to read (press Enter to return to the main menu): ",
    )
    if choice is None:
        return None

    chosen_file = os.path.join(review_files_path, files[choice - 1])
    with open(chosen_file, "r", encoding="utf-8") as stream:
        review_content = stream.read()

    print("\n--------------------------------------")
    print("Review file content:")
    print("--------------------------------------")
    print(review_content)
    print("--------------------------------------")
    return review_content


def enter_or_read_review_for_analysis(
    word_counter: WordCounter, is_enter_review: bool
) -> None:
    """
    Prompts the user to enter a review for analysis or reads a review file for analysis based on the is_enter_review parameter.
    """
    if is_enter_review:
        review = input("\nProvide your review: ")
        if len(review) == 0:
            print("\nNo review for analysis")
            input("\nPress a key to return to the main menu... ")
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

    preference = input("\nAre you interested in per word sentiment details? [y/n]: ")
    if preference.lower() == "y":
        print_sentiment_details(sentiment_details)

    if not advanced:
        advanced_choice = input(
            "\nDo you want to perform advanced sentiment analysis after all? [y/n]: "
        )
        if advanced_choice.lower() == "y":
            preprocessed_review = preprocess_review(review, advanced=True)
            advanced_sentiment, advanced_sentiment_details = compute_sentiment(
                preprocessed_review, word_counter, True
            )
            print_sentiment(advanced_sentiment)
            preference = input(
                "\nAre you interested in per word sentiment details? [y/n]: "
            )
            if preference.lower() == "y":
                print_sentiment_details(advanced_sentiment_details)

    if is_enter_review:
        save_review_choice = input("\nDo you want to save this review? [y/n]: ")
        if save_review_choice.lower() == "y":
            save_review(review, REVIEW_FILES_PATH)

    input("\nPress a key to return to the main menu... ")


def get_next_review_file(review_files_path: str) -> str:
    """
    Returns the name of the next available review file (ReviewX.txt) in the REVIEW_FILES_PATH directory, where X is the smallest available integer starting with 1.
    """
    try:
        files = os.listdir(review_files_path)
        existing_numbers = [
            int(file.split("Review")[1].split(".")[0])
            for file in files
            if file.startswith("Review")
        ]
        next_number = 1
        while next_number in existing_numbers:
            next_number += 1
        return f"Review{next_number}.txt"
    except FileNotFoundError:
        print("Directory not found. Please make sure the directory exists.")
        return None


def save_review(review: str, review_files_path: str) -> None:
    """
    Saves the provided review in the REVIEW_FILES_PATH location using the ReviewX.txt pattern,
    where X is the smallest available integer starting with 1 if there is no review file yet.
    """
    next_file = get_next_review_file(review_files_path)
    with open(
        os.path.join(review_files_path, next_file), "w", encoding="utf-8"
    ) as stream:
        stream.write(review)
    print("\n--------------------------------------")
    print(f"Review saved to {next_file}.")
    print("--------------------------------------")
    return None


def delete_review_file(review_files_path: str) -> None:
    """
    Deletes a review file from the provided path.
    """
    files = list_review_files(review_files_path)
    if not files:
        return None

    choice = get_user_choice(
        files,
        "\nEnter the number of the review file you want to delete (press Enter to return to the main menu): ",
    )
    if choice is None:
        return None

    chosen_file = os.path.join(review_files_path, files[choice - 1])
    os.remove(chosen_file)

    print("\n--------------------------------------")
    print(f"Review file '{files[choice - 1]}' has been deleted.")
    print("--------------------------------------")
    input("\nPress a key to return to the main menu...")


def main() -> None:

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

        elif choice == "4" or choice == "":
            print("Exiting program...")
            break

        else:
            print("\nInvalid choice. Please enter a valid option (1/2/3/4).")


if __name__ == "__main__":
    main()
