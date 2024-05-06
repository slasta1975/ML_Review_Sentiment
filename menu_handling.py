"""
This module provides functions for handling and displaying menus for user interaction
in a sentiment analysis application.

The `display_menu` function displays the main menu to the user and retrieves their choice.
The menu offers options for entering a review for analysis, reading a review file, deleting
a review file, or exiting the program. The user's choice is returned as a string for further
processing.
"""

def display_menu() -> str:
    """
    Display the main menu and return the user's choice.
    """
    print("\n----------")
    print("Main Menu:")
    print("----------")
    print("1. Enter your review for analysis")
    print("2. Read a review file for analysis")
    print("3. Delete a review file")
    print("4. Exit")
    print("----------")

    return input("Enter your choice (1/2/3/4): ")