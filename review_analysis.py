from sentiment_analysis import WordCounter, compute_sentiment
from file_operations import read_review_file, save_review
from preprocessing import preprocess_review


def enter_or_read_review_for_analysis(word_counter: WordCounter, is_enter_review: bool):
    if is_enter_review:
        review = input("\nProvide your review: ")
        if len(review) == 0:
            print("\nNo review provided.")
            return
    else:
        review = read_review_file("reviews")
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

    rounded_sentiment = round(sentiment, 2)
    verdict = "positive" if rounded_sentiment > 0 else "neutral" if rounded_sentiment == 0 else "negative"
    
    print(f"\nThis review is {verdict}, sentiment = {sentiment:.2f}")

    if input("\nShow per-word sentiment? [y/n]: ").lower() == "y":
        print("\nPer-word sentiment details:")
        for word, word_sentiment in sentiment_details:
            print(f"{word}: {word_sentiment:.2f}")

    if not advanced:
        if input("\nPerform advanced sentiment analysis after all? [y/n]: ").lower() == "y":
            preprocessed_review = preprocess_review(review, advanced=True)
            sentiment, sentiment_details = compute_sentiment(
                preprocessed_review, word_counter, True
            )
            rounded_sentiment = round(sentiment, 2)
            verdict = "positive" if rounded_sentiment > 0 else "neutral" if rounded_sentiment == 0 else "negative"
            print(f"\nThis review is {verdict}, sentiment = {sentiment:.2f}")
            if input("\nShow per-word sentiment? [y/n]: ").lower() == "y":
                for word, word_sentiment in sentiment_details:
                    print(f"{word}: {word_sentiment:.2f}")

    if is_enter_review:
        if input("\nSave this review? [y/n]: ").lower() == "y":
            save_review(review, "reviews")

    input("\nPress enter to return to the main menu... ")