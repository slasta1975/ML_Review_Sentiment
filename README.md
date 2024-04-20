# Sentiment Analysis of Movie Reviews

This Python project performs sentiment analysis on movie reviews using a basic bag-of-words approach. It counts the occurrences of positive and negative words in the reviews to determine their sentiment.

## Features

- **Enter Your Review for Analysis**: Allows users to enter their own review for sentiment analysis.
- **Read a Review File for Analysis**: Enables users to read a review file from a directory and analyze its sentiment.
- **Delete a Review File**: Allows users to delete review files from the directory.
- **Save Review**: Saves the provided review to a file for future analysis.
- **View Review Files**: Lists the review files available in the specified directory along with their first sentences.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/slasta1975/ML_Review_Sentiment.git
    ```

## Usage

1. Run the `main.py` script:

    ```bash
    python main.py
    ```

2. Follow the on-screen instructions to enter your review, read a review file, delete a review file, or exit the program.

## Acknowledgment

This project is using the Large Movie Review Dataset v1.0:
@InProceedings{maas-EtAl:2011:ACL-HLT2011,
  author    = {Maas, Andrew L.  and  Daly, Raymond E.  and  Pham, Peter T.  and  Huang, Dan  and  Ng, Andrew Y.  and  Potts, Christopher},
  title     = {Learning Word Vectors for Sentiment Analysis},
  booktitle = {Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies},
  month     = {June},
  year      = {2011},
  address   = {Portland, Oregon, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {142--150},
  url       = {http://www.aclweb.org/anthology/P11-1015}
}
