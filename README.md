# Sentiment Analysis of Movie Reviews

This Python project performs sentiment analysis on movie reviews using a basic bag-of-words approach. 
It counts the occurrences of positive and negative words in the reviews to determine their sentiment. 
Reviews can be manually entered or loaded from saved text files. 
An advanced mode analysis is also possible which can detect negation in the analysed review and inverse sentiments of affected words thus improving the outcome. 

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

## Dependencies

Python 3.x
Required Python packages: glob, os, typing

## Acknowledgment

This project uses the [Large Movie Review Dataset v1.0](http://ai.stanford.edu/~amaas/data/sentiment/). This project is licensed under the MIT License.
