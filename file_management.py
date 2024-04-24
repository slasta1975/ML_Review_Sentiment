
import os
import re
from typing import List


def list_review_files(review_files_path: str) -> List[str]:
    """
    Lists the review files available in the provided path along with their first sentences.
    """
    try:
        files = [
            file for file in os.listdir(review_files_path) if file.endswith(".txt")
        ]
        if not files:
            print("\nNo review files found.")
            return None

        sorted_files = sorted(
            files, key=lambda x: int(x.split("Review")[1].split(".")[0])
        )

        for i, file_name in enumerate(sorted_files, 1):
            with open(
                os.path.join(review_files_path, file_name), "r", encoding="utf-8"
            ) as file:
                content = file.read()
                sentences = re.split(r"[.!?]", content)
                first_sentence = sentences[0] + ("..." if len(sentences) > 1 else "")
                print(f"{i}. {file_name} - {first_sentence}")

        return sorted_files
    except FileNotFoundError:
        print("\nDirectory not found. Please make sure the directory exists.\n")
        return None


def get_user_choice(files: List[str], prompt: str) -> int:
    """
    Prompts the user to enter a choice and validates the input.
    """
    while True:
        choice = input(prompt).strip()
        if choice == "":
            print("\nReturning to the main menu...")
            return None

        try:
            choice_int = int(choice)
            if 1 <= choice_int <= len(files):
                return choice_int
            else:
                print("\nInvalid choice. Please enter a number within the range:")
        except ValueError:
            print("\nInvalid input. Please enter a valid number:")


def read_review_file(review_files_path: str) -> str:
    """
    Reads a review file from the provided path and returns its content.
    """
    files = list_review_files(review_files_path)
    if not files:
        return None

    choice = get_user_choice(
        files,
        "\nEnter the number of the review file you want to read (press Enter to return to the main menu): ",
    )

    if choice is None:
        return None

    chosen_file = os.path.join(review_files_path, files[choice - 1])
    with open(chosen_file, "r", encoding="utf-8") as stream:
        review_content = stream.read()

    print(f"\nReview file content:\n{review_content}")
    return review_content


def save_review(review: str, review_files_path: str) -> None:
    """
    Saves the provided review in the REVIEW_FILES_PATH location using the ReviewX.txt pattern.
    """
    files = list_review_files(review_files_path)
    next_file_number = len(files) + 1 if files else 1
    file_name = f"Review{next_file_number}.txt"

    with open(
        os.path.join(review_files_path, file_name), "w", encoding="utf-8"
    ) as stream:
        stream.write(review)

    print(f"Review saved to {file_name}.")


def delete_review_file(review_files_path: str) -> None:
    """
    Deletes a review file from the provided path.
    """
    files = list_review_files(review_files_path)

    if not files:
        return None

    choice = get_user_choice(
        files,
        "\nEnter the number of the review file you want to delete (press Enter to return to the main menu): ",
    )

    if choice is None:
        return None

    chosen_file = os.path.join(review_files_path, files[choice - 1])
    os.remove(chosen_file)

    print(f"Review file '{files[choice - 1]}' has been deleted.")