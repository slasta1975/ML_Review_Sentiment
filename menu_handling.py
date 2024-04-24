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