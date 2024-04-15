""" Decides whether a given opion is positive or negative based on analyzing a sentiment of a given review against a model based on 25 thousand opinions.

Usage: python ML_Review_Sentiment.py
"""


import glob
import sys

POS_FILES_FEED = r"PP\M03\data\aclImdb\train\pos\*.txt"
NEG_FILES_FEED = r"PP\M03\data\aclImdb\train\neg\*.txt"
PUNCTUATIONS = ['.', ',', '?', '!', ':', ';', '-','"','<br />' ]


def preprocess_review(review):
    """
    Returns a list of lower case words from provided review without punctuations or special characters defined in 'PUNCTUATIONS'.
    """
    for punctuation in PUNCTUATIONS:
        review = review.replace(punctuation, ' ')
    return review.lower().split()


def count_words(path_pattern):
    """
    Calculates number of how many times a word has been used in defined 'files'. 
    Returns dictionary with review and usage counter. 
    """
    words_count = {}
    files = glob.glob(path_pattern)
    for file in files:
        with open(file,encoding = 'utf-8') as stream:
            content = stream.read()
        review = preprocess_review(content)
        for word in set(review):
            words_count[word] = words_count.get(word,0) + 1
    return words_count    

def compute_sentiment(review, pos_words_count, neg_words_count, detailing=False):
    # calculating sentiment of provided review
    cumulative_sentiment = 0
    for word in review:
        pos_counter = pos_words_count.get(word,0)
        neg_counter = neg_words_count.get(word,0)
        total = pos_counter + neg_counter    
        if total == 0:
            word_sentiment = 0
        else:
            word_sentiment = (pos_counter - neg_counter)/total
        cumulative_sentiment += word_sentiment
        if detailing:
            print(word, word_sentiment)
    return cumulative_sentiment/len(review)


def print_sentiment(sentiment):
            # Final statement
    if sentiment > 0:
        verdict = "positive"
    else:
        verdict = "negative"
    print("---")
    print("This review is", verdict, ", sentiment =", sentiment)


def main():

    pos_words_count = count_words(POS_FILES_FEED)
    neg_words_count = count_words(NEG_FILES_FEED)

        # getting review for analysis
    review = input ("Provide your review: ")
    if len(review) == 0:
        print("No review for analysis")
        sys.exit(1)
    else:
        preference = input("Interested in details? [y/n] ")
        if preference.lower() == "y":
            detailing = True
        else:
            detailing = False
        review = preprocess_review(review)
        sentiment = compute_sentiment(review, pos_words_count, neg_words_count, detailing)
        print_sentiment(sentiment)

    
if __name__ == "__main__":
    main()
