"""
Menu Helpers Utility.
Provides formatted banners, navigation, input prompts, and console display utilities.
"""

import os
from typing import List, Tuple


class MenuHelpers:
    """Helper methods for console UI formatting and input collection."""

    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen safely across platforms."""
        # Use simple newline printing if inside non-interactive or web environment,
        # or call standard system clear
        try:
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")
        except Exception:
            print("\n" * 2)

    @staticmethod
    def display_banner(title: str, width: int = 50) -> None:
        """Display a formatted title banner."""
        print()
        print("=" * width)
        print(title.center(width))
        print("=" * width)

    @staticmethod
    def display_sub_header(title: str, width: int = 50) -> None:
        """Display a sub-header divider."""
        print("-" * width)
        print(f" {title}")
        print("-" * width)

    @staticmethod
    def display_menu(title: str, options: List[str], width: int = 50) -> None:
        """Display a standard menu with numbered options."""
        MenuHelpers.display_banner(title, width)
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")
        print("-" * width)

    @staticmethod
    def get_menu_choice(min_val: int, max_val: int, prompt_text: str = "Select an option: ") -> int:
        """Prompt user for a valid numerical menu choice within range."""
        while True:
            choice = input(prompt_text).strip()
            if not choice:
                print("Input cannot be empty. Please enter a valid number.")
                continue
            if choice.isdigit():
                val = int(choice)
                if min_val <= val <= max_val:
                    return val
                print(f"Please enter a number between {min_val} and {max_val}.")
            else:
                print("Invalid input. Please enter a numerical choice.")

    @staticmethod
    def pause(message: str = "Press Enter to continue...") -> None:
        """Pause execution until the user presses Enter."""
        try:
            input(f"\n{message}")
        except (EOFError, KeyboardInterrupt):
            pass
