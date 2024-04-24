
from typing import List, Tuple
from word_counter import WordCounter


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
        original_word = word[4:] if advanced and word.startswith("not_") else word
        pos_counter = word_counter.pos_words_count.get(original_word, 0)
        neg_counter = word_counter.neg_words_count.get(original_word, 0)
        total = pos_counter + neg_counter
        if total == 0:
            word_sentiment = 0
        else:
            word_sentiment = (-1 if advanced and word.startswith("not_") else 1) * (pos_counter - neg_counter) / total
        cumulative_sentiment += word_sentiment
        sentiment_details.append((word, word_sentiment))
    
    average_sentiment = cumulative_sentiment / len(review)
    return average_sentiment, sentiment_details


def print_sentiment(sentiment: float) -> None:
    rounded_sentiment = round(sentiment, 2)
    verdict = "positive" if rounded_sentiment > 0 else ("negative" if rounded_sentiment < 0 else "neutral")
    print(f"\n------------------------------------------")
    print(f"This review is {verdict}, sentiment = {sentiment:.2f}")
    print("------------------------------------------")


def print_sentiment_details(sentiment_details: List[Tuple[str, float]]) -> None:
    print("\n---------------------------")
    print("Per word sentiment details:")
    print("---------------------------")
    for word, word_sentiment in sentiment_details:
        print(f"{word}: {word_sentiment:.2f}")
    print("---------------------------")