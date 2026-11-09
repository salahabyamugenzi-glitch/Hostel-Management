"""
Bed Model.
Demonstrates Encapsulation with private attributes and public getters and setters.
"""

from typing import Dict, Any


class Bed:
    """
    Bed class representing an individual bed inside a room.
    Encapsulates bed state privately.
    """

    def __init__(
        self,
        bed_number: str = "",
        room_number: str = "",
        status: str = "Available",
    ):
        self.__bed_number: str = bed_number
        self.__room_number: str = room_number
        self.__status: str = status

    # --- Getters ---

    def get_bed_number(self) -> str:
        """Get bed identifier/number."""
        return self.__bed_number

    def get_room_number(self) -> str:
        """Get associated room number."""
        return self.__room_number

    def get_status(self) -> str:
        """Get bed status (Occupied / Available)."""
        return self.__status

    # --- Setters ---

    def set_bed_number(self, bed_number: str) -> None:
        """Set bed identifier/number."""
        self.__bed_number = bed_number

    def set_room_number(self, room_number: str) -> None:
        """Set associated room number."""
        self.__room_number = room_number

    def set_status(self, status: str) -> None:
        """Set bed status (Occupied / Available)."""
        self.__status = status

    # --- Serialization Helpers ---

    def to_dict(self) -> Dict[str, Any]:
        """Convert bed object to dictionary representation."""
        return {
            "bed_number": self.get_bed_number(),
            "room_number": self.get_room_number(),
            "status": self.get_status(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Bed":
        """Instantiate Bed from dictionary representation."""
        return cls(
            bed_number=data.get("bed_number", ""),
            room_number=data.get("room_number", ""),
            status=data.get("status", "Available"),
        )
