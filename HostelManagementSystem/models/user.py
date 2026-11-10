"""
User Model (Parent Class).
Demonstrates Encapsulation and acts as the Parent class for Student and Staff.
Strictly encapsulates all attributes using private fields (__attribute)
with public getter and setter methods.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class User(ABC):
    """
    Parent class representing a general system user.
    Uses strict encapsulation with private attributes and public getters/setters.
    """

    def __init__(
        self,
        first_name: str = "",
        last_name: str = "",
        gender: str = "",
        contact: str = "",
        address: str = "",
        password: str = "",
    ):
        self.__first_name: str = first_name
        self.__last_name: str = last_name
        self.__gender: str = gender
        self.__contact: str = contact
        self.__address: str = address
        self.__password: str = password

    # --- Getters ---

    def get_first_name(self) -> str:
        """Get user's first name."""
        return self.__first_name

    def get_last_name(self) -> str:
        """Get user's last name."""
        return self.__last_name

    def get_gender(self) -> str:
        """Get user's gender."""
        return self.__gender

    def get_contact(self) -> str:
        """Get user's contact number."""
        return self.__contact

    def get_address(self) -> str:
        """Get user's residential address."""
        return self.__address

    def get_password(self) -> str:
        """Get user's password."""
        return self.__password

    def get_full_name(self) -> str:
        """Get user's concatenated full name."""
        return f"{self.__first_name} {self.__last_name}".strip()

    @abstractmethod
    def get_profile_summary(self) -> str:
        """Return a role-specific profile summary."""
        raise NotImplementedError

    # --- Setters ---

    def set_first_name(self, first_name: str) -> None:
        """Set user's first name."""
        self.__first_name = first_name

    def set_last_name(self, last_name: str) -> None:
        """Set user's last name."""
        self.__last_name = last_name

    def set_gender(self, gender: str) -> None:
        """Set user's gender."""
        self.__gender = gender

    def set_contact(self, contact: str) -> None:
        """Set user's contact number."""
        self.__contact = contact

    def set_address(self, address: str) -> None:
        """Set user's address."""
        self.__address = address

    def set_password(self, password: str) -> None:
        """Set user's password."""
        self.__password = password

    # --- Serialization Helpers ---

    def to_user_dict(self) -> Dict[str, Any]:
        """Convert encapsulated parent user attributes to dictionary representation."""
        return {
            "first_name": self.get_first_name(),
            "last_name": self.get_last_name(),
            "gender": self.get_gender(),
            "contact": self.get_contact(),
            "address": self.get_address(),
            "password": self.get_password(),
        }

    def load_user_dict(self, data: Dict[str, Any]) -> None:
        """Populate parent user attributes from dictionary using public setters."""
        self.set_first_name(data.get("first_name", ""))
        self.set_last_name(data.get("last_name", ""))
        self.set_gender(data.get("gender", ""))
        self.set_contact(data.get("contact", ""))
        self.set_address(data.get("address", ""))
        self.set_password(data.get("password", ""))
