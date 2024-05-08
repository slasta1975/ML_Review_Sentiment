from typing import List, Tuple, Dict
from preprocessing import preprocess_review, remove_punctuations


class WordCounter:
    def __init__(self):
        self.pos_words_count: Dict[str, int] = {}
        self.neg_words_count: Dict[str, int] = {}

    def count_words(self, path_pattern: str, is_positive: bool) -> None:
        import glob
        
        files = glob.glob(path_pattern)
        for file in files:
            with open(file, encoding="utf-8") as stream:
                content = stream.read()
            preprocessed_review = remove_punctuations(content).lower().split()
            for word in set(preprocessed_review):
                if is_positive:
                    self.pos_words_count[word] = (
                        self.pos_words_count.get(word, 0) + 1
                    )
                else:
                    self.neg_words_count[word] = (
                        self.neg_words_count.get(word, 0) + 1
                    )


def compute_sentiment(
    review: List[str],
    word_counter: WordCounter,
    advanced: bool = False,
) -> Tuple[float, List[Tuple[str, float]]]:
    cumulative_sentiment = 0
    sentiment_details = []

    for word in review:
        if advanced and word.startswith("not_"):
            original_word = word[4:]
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