""" Decides whether a given reivew is positive or negative based on analyzing a sentiment of a given review against a simple model based on 25 thousand opinions.

Usage: python ML_Review_Sentiment.py
"""
import glob
import sys

POS_FILES_FEED = r"PP\M03\data\aclImdb\train\pos\*.txt"
NEG_FILES_FEED = r"PP\M03\data\aclImdb\train\neg\*.txt"
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
    Adds a "not_" prefix to words following a negation in the sentence.
    """
    sentences = review.split(".")
    advanced_review = []
    for punctuation in PUNCTUATIONS:
            review = review.replace(punctuation, ' ')
    for sentence in sentences:
        words = sentence.lower().split()
        negate = False
        for word in words:
            if word in ["not", "no", "never", "neither", "nor"] or "n't" in word:
                negate = True
            elif negate:
                word = "not_" + word
            advanced_review.append(word)
    return advanced_review


class WordCounter:
    def __init__(self):
        self.pos_words_count = {}
        self.neg_words_count = {}

    def count_words(self, path_pattern):
        """
        Calculates number of how many times a word has been used in defined 'files'.
        Updates dictionaries with review and usage counter.
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
            pos_counter = pos_words_count.get(original_word, 0)
            neg_counter = neg_words_count.get(original_word, 0)
        else:
            pos_counter = pos_words_count.get(word, 0)
            neg_counter = neg_words_count.get(word, 0)
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


def main():
    word_counter = WordCounter()
    word_counter.count_words(POS_FILES_FEED)
    word_counter.count_words(NEG_FILES_FEED)

    while True:
        review = input("\nProvide your review (or enter 'exit' to quit): ")
        if review.lower() == "exit":
            print("Exiting program...")
            break

        if len(review) == 0:
            print("No review for analysis")
            continue

        advanced_analysis = input("\nDo you want to perform advanced sentiment analysis? [y/n]: ")
        if advanced_analysis.lower() == "y":
            review = advanced_preprocess_review(review)
            advanced = True
        else:
            review = preprocess_review(review)
            advanced = False

        sentiment, sentiment_details = compute_sentiment(review, word_counter.pos_words_count, word_counter.neg_words_count, advanced)
        print_sentiment(sentiment)

        preference = input("\nAre you interested in per word sentiment details? [y/n]: ")
        if preference.lower() == "y":
            print_sentiment_details(sentiment_details)

        choice = input("\nDo you want to analyze another review? [y/n]: ")
        if choice.lower() != "y":
            print("Exiting program...")
            break


if __name__ == "__main__":
    main()