import glob
import os

POS_FILES_FEED = r"..\..\PP\M03\data\aclImdb\train\pos\*.txt"
NEG_FILES_FEED = r"..\..\PP\M03\data\aclImdb\train\neg\*.txt"
PUNCTUATIONS = ['.', ',', '?', '!', ':', ';', '-', '"', '<br />']


def preprocess_review(review):
    """
    Returns a list of lower case words from provided review without punctuations or special characters defined in 'PUNCTUATIONS'.
    """
    for punctuation in PUNCTUATIONS:
        review = review.replace(punctuation, ' ')
    return review.lower().split()


def advanced_preprocess_review(review):
    """
    Returns a list of lower case words from provided review without punctuations or special characters defined in 'PUNCTUATIONS'.
    Adds a "not_" prefix to words following a negation in the sentence and cancels negation when detects so.
    """
    sentences = review.split(".")
    advanced_review = []
    for sentence in sentences:
        for punctuation in PUNCTUATIONS:
            sentence = sentence.replace(punctuation, ' ')
        words = sentence.lower().split()
        negate = False
        for word in words:
            if word in ["not", "no", "never", "neither", "nor"] or "n't" in word:
                negate = True
            elif word == "far" and "from" in words[words.index(word) + 1]:
                negate = True
            elif negate and word == "only":
                negate = False
            elif negate and word not in ["but", "however", "nevertheless"]:
                word = "not_" + word
            else:
                negate = False
            advanced_review.append(word)
    return advanced_review


class WordCounter:
    def __init__(self):
        self.pos_words_count = {}
        self.neg_words_count = {}

    def count_words(self, path_pattern):
        """
        Calculates number of how many times a word has been used in training positive and negative reviews kept in POS_FILES_FEED and NEG_FILES_FEED locations.
        Updates dictionaries with review words and usage counters.
        """
        files = glob.glob(path_pattern)
        for file in files:
            with open(file, encoding='utf-8') as stream:
                content = stream.read()
            preprocessed_review = preprocess_review(content)
            for word in set(preprocessed_review):
                if path_pattern == POS_FILES_FEED:
                    self.pos_words_count[word] = self.pos_words_count.get(word, 0) + 1
                else:
                    self.neg_words_count[word] = self.neg_words_count.get(word, 0) + 1


def compute_sentiment(review, pos_words_count, neg_words_count, advanced=False):
    cumulative_sentiment = 0
    sentiment_details = []
    for word in review:
        if advanced and word.startswith("not_"):
            original_word = word[4:]  # Remove "not_" prefix
        else:
            original_word = word
        pos_counter = pos_words_count.get(original_word, 0)
        neg_counter = neg_words_count.get(original_word, 0)
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


def print_sentiment(sentiment):
    if sentiment > 0:
        verdict = "positive"
    elif sentiment == 0:
        verdict = "neutral"
    else:
        verdict = "negative"
    print("\n---")
    print(f"This review is {verdict}, sentiment = {sentiment:.2f}")
    print("---")


def print_sentiment_details(sentiment_details):
    print("\n---")
    print("Per word sentiment details:")
    for word, word_sentiment in sentiment_details:
        print(f"{word}: {word_sentiment:.2f}")
    print("---\n")


def get_next_review_file(review_files_path):
    """
    Returns the name of the next available review file (ReviewX.txt) in the REVIEW_FILES_PATH directory,
    where X is the smallest available integer starting with 1.
    """
    files = os.listdir(review_files_path)
    if not files:
        return "Review1.txt"
    else:
        file_numbers = [int(file.split("Review")[1].split(".")[0]) for file in files if file.startswith("Review")]
        if not file_numbers:
            return "Review1.txt"
        next_file_number = max(file_numbers) + 1
        return f"Review{next_file_number}.txt"


def save_review(review, review_files_path):
    """
    Saves the provided review in the REVIEW_FILES_PATH location using the ReviewX.txt pattern,
    where X is the smallest available integer starting with 1 if there is no review file yet.
    """
    next_file = get_next_review_file(review_files_path)
    with open(os.path.join(review_files_path, next_file), 'w', encoding='utf-8') as file:
        file.write(review)
    print(f"Review saved to {next_file}")


def read_review_file(review_files_path):
    """
    Reads a review file from the provided path.
    """
    try:
        files = [file for file in os.listdir(review_files_path) if file.endswith('.txt')]
        if not files:
            print("No review files found.")
            return None

        print("\nReview files found in the directory:")
        for i, file_name in enumerate(files, 1):
            print(f"{i}. {file_name}")

        choice = input("Enter the number of the review file you want to read: ")
        try:
            choice = int(choice)
            if choice < 1 or choice > len(files):
                print("Invalid choice. Please enter a number within the range.")
                return None
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return None

        chosen_file = os.path.join(review_files_path, files[choice - 1])
        with open(chosen_file, 'r', encoding='utf-8') as file:
            review_content = file.read()
            print("\nReview content:")
            print(review_content)
        return review_content
    except FileNotFoundError:
        print("Directory not found. Please make sure the directory exists.")
        return None


def main():
    REVIEW_FILES_PATH = os.path.dirname(os.path.abspath(__file__))

    word_counter = WordCounter()
    word_counter.count_words(POS_FILES_FEED)
    word_counter.count_words(NEG_FILES_FEED)

    while True:
        print("\nMain Menu:")
        print("1. Enter your review for analysis")
        print("2. Load a review file for analysis")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            review = input("\nProvide your review (or enter 'exit' to return to the main menu): ")
            if review.lower() == "exit":
                continue

            if len(review) == 0:
                print("No review for analysis")
                continue

            advanced_analysis = input("\nDo you want to perform advanced sentiment analysis? [y/n]: ")
            if advanced_analysis.lower() == "y":
                preprocessed_review = advanced_preprocess_review(review)
                advanced = True
            else:
                preprocessed_review = preprocess_review(review)
                advanced = False

            sentiment, sentiment_details = compute_sentiment(preprocessed_review, word_counter.pos_words_count,
                                                             word_counter.neg_words_count, advanced)
            print_sentiment(sentiment)

            preference = input("\nAre you interested in per word sentiment details? [y/n]: ")
            if preference.lower() == "y":
                print_sentiment_details(sentiment_details)

            if advanced_analysis.lower() != "y":
                advanced_option = input("\nWould you like to perform advanced analysis on this review? [y/n]: ")
                if advanced_option.lower() == "y":
                    advanced_sentiment, advanced_sentiment_details = compute_sentiment(
                        advanced_preprocess_review(review), word_counter.pos_words_count,
                        word_counter.neg_words_count, True
                    )
                    print_sentiment(advanced_sentiment)
                    advanced_preference = input("\nAre you interested in per word sentiment details? [y/n]: ")
                    if advanced_preference.lower() == "y":
                        print_sentiment_details(advanced_sentiment_details)

            save_review_choice = input("\nDo you want to save this review? [y/n]: ")
            if save_review_choice.lower() == "y":
                save_review(review, REVIEW_FILES_PATH)

        elif choice == "2":
            read_review_content = read_review_file(REVIEW_FILES_PATH)
            if read_review_content:
                review = read_review_content

                advanced_analysis = input("\nDo you want to perform advanced sentiment analysis? [y/n]: ")
                if advanced_analysis.lower() == "y":
                    preprocessed_review = advanced_preprocess_review(review)
                    advanced = True
                else:
                    preprocessed_review = preprocess_review(review)
                    advanced = False

                sentiment, sentiment_details = compute_sentiment(preprocessed_review, word_counter.pos_words_count,
                                                                 word_counter.neg_words_count, advanced)
                print_sentiment(sentiment)

                preference = input("\nAre you interested in per word sentiment details? [y/n]: ")
                if preference.lower() == "y":
                    print_sentiment_details(sentiment_details)

                if advanced_analysis.lower() != "y":
                    advanced_option = input("\nWould you like to perform advanced analysis after all? [y/n]: ")
                    if advanced_option.lower() == "y":
                        advanced_sentiment, advanced_sentiment_details = compute_sentiment(
                            advanced_preprocess_review(review), word_counter.pos_words_count,
                            word_counter.neg_words_count, True
                        )
                        print_sentiment(advanced_sentiment)
                        advanced_preference = input("\nAre you interested in per word sentiment details? [y/n]: ")
                        if advanced_preference.lower() == "y":
                            print_sentiment_details(advanced_sentiment_details)

        elif choice == "3":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please enter a valid option (1/2/3).")

if __name__ == "__main__":
    main()