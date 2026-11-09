"""
Validators Utility.
Validates inputs such as passwords, contact numbers, payment amounts, and general strings.
"""

import re
import math
from typing import Optional, Tuple


class Validators:
    """Provides validation methods for user inputs."""

    @staticmethod
    def validate_name(name: str, field_name: str = "Name") -> Tuple[bool, str]:
        """Validate that a name contains only alphabetic characters, spaces, or hyphens."""
        cleaned = name.strip()
        if not cleaned:
            return False, f"{field_name} cannot be empty."
        if len(cleaned) < 2:
            return False, f"{field_name} must be at least 2 characters long."
        if not re.match(r"^[A-Za-z\s\-']+$", cleaned):
            return False, f"{field_name} can only contain letters, hyphens, and spaces."
        return True, ""

    @staticmethod
    def validate_contact(contact: str) -> Tuple[bool, str]:
        """
        Validate contact phone numbers (e.g., 0771234567, +256771234567, 10-15 digits).
        """
        cleaned = contact.strip().replace(" ", "").replace("-", "")
        if not cleaned:
            return False, "Contact number cannot be empty."
        if not re.match(r"^\+?[0-9]{10,15}$", cleaned):
            return False, "Contact must be a valid phone number (10 to 15 digits, optional + prefix)."
        return True, ""

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password requirements (at least 6 characters).
        """
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        if password.strip() == "":
            return False, "Password cannot be only whitespace."
        return True, ""

    @staticmethod
    def validate_amount(amount_input: str, min_amount: float = 150000.0) -> Tuple[bool, str, float]:
        """
        Validate monetary amount: must be numeric and meet or exceed min_amount (UGX 150,000).
        """
        cleaned = amount_input.strip().replace(",", "")
        try:
            val = float(cleaned)
            if not math.isfinite(val) or val < min_amount:
                return False, f"Minimum payment amount is UGX {min_amount:,.0f}.", 0.0
            return True, "", val
        except ValueError:
            return False, "Invalid amount. Please enter a valid numerical value.", 0.0

    @staticmethod
    def validate_non_empty(value: str, field_name: str) -> Tuple[bool, str]:
        """Ensure an input string is not empty or just whitespace."""
        cleaned = value.strip()
        if not cleaned:
            return False, f"{field_name} cannot be empty."
        return True, ""
