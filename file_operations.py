import os
import re
from typing import List

REVIEW_FILES_PATH = r"reviews"


def list_review_files(review_files_path: str) -> List[str]:
    try:
        files = [
            file for file in os.listdir(review_files_path) if file.endswith(".txt")
        ]
        if not files:
            print("\nNo review files found.")
            return []
        
        sorted_files = sorted(
            files, key=lambda x: int(x.split("Review")[1].split(".")[0])
        )
        
        for i, file_name in enumerate(sorted_files, 1):
            with open(
                os.path.join(review_files_path, file_name), "r", encoding="utf-8"
            ) as file:
                content = file.read()
                sentences = re.split(r"[.!?]", content)
                if len(sentences) > 1:
                    first_sentence = sentences[0] + ("..." if sentences[1] else "")
                else:
                    first_sentence = content.strip()
                print(f"{i}. {file_name} - {first_sentence}")
                
        return sorted_files

    except FileNotFoundError:
        print("\nDirectory not found. Please make sure the directory exists.\n")
        return []


def get_user_choice(files, prompt):
    while True:
        choice = input(prompt).strip()
        if choice == "":
            return None
        
        try:
            choice_int = int(choice)
            if 1 <= choice_int <= len(files):
                return choice_int
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Try again.")

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

    print("\n--------------------------------------")
    print("Review file content:")
    print("--------------------------------------")
    print(review_content)
    print("--------------------------------------")
    return review_content


def save_review(review: str, review_files_path: str) -> None:
    def get_next_review_file() -> str:
        try:
            files = os.listdir(review_files_path)
            existing_numbers = [
                int(file.split("Review")[1].split(".")[0])
                for file in files
                if file.startswith("Review")
            ]
            next_number = 1
            while next_number in existing_numbers:
                next_number += 1
            return f"Review{next_number}.txt"
        except FileNotFoundError:
            print("Directory not found.")
            return None

    next_file = get_next_review_file()
    if not next_file:
        return
    
    with open(os.path.join(review_files_path, next_file), "w", encoding="utf-8") as stream:
        stream.write(review)
    
    print(f"\nReview saved to {next_file}.")


def delete_review_file(review_files_path: str) -> None:
    files = list_review_files(review_files_path)
    if not files:
        return

    choice = get_user_choice(
        files, "\nEnter the number of the review file you want to delete or press <enter> to return to Main Menu: "
    )
    if choice is None:
        return

    chosen_file = os.path.join(review_files_path, files[choice - 1])
    os.remove(chosen_file)

    print(f"\nReview file '{files[choice - 1]}' has been deleted.")
    input("\nPress <enter> to return to the Main Menu... ")