"""
Hostel Model.
Demonstrates Encapsulation with private attributes and public getters and setters.
"""

from typing import Dict, Any


class Hostel:
    """
    Hostel class representing a residential building.
    Encapsulates hostel details privately.
    """

    def __init__(
        self,
        hostel_id: str = "",
        hostel_name: str = "",
        gender_category: str = "",
        location: str = "",
        total_rooms: int = 0,
        warden_id: str = "",
        status: str = "Active",
    ):
        self.__hostel_id: str = hostel_id
        self.__hostel_name: str = hostel_name
        self.__gender_category: str = gender_category
        self.__location: str = location
        self.__total_rooms: int = total_rooms
        self.__warden_id: str = warden_id
        self.__status: str = status

    # --- Getters ---

    def get_hostel_id(self) -> str:
        """Get hostel ID."""
        return self.__hostel_id

    def get_hostel_name(self) -> str:
        """Get hostel name."""
        return self.__hostel_name

    def get_gender_category(self) -> str:
        """Get gender category (Male or Female)."""
        return self.__gender_category

    def get_location(self) -> str:
        """Get hostel physical location."""
        return self.__location

    def get_total_rooms(self) -> int:
        """Get total number of rooms in hostel."""
        return self.__total_rooms

    def get_warden_id(self) -> str:
        """Get assigned warden's staff ID."""
        return self.__warden_id

    def get_status(self) -> str:
        """Get hostel status (Active/Inactive)."""
        return self.__status

    # --- Setters ---

    def set_hostel_id(self, hostel_id: str) -> None:
        """Set hostel ID."""
        self.__hostel_id = hostel_id

    def set_hostel_name(self, hostel_name: str) -> None:
        """Set hostel name."""
        self.__hostel_name = hostel_name

    def set_gender_category(self, gender_category: str) -> None:
        """Set gender category."""
        self.__gender_category = gender_category

    def set_location(self, location: str) -> None:
        """Set hostel location."""
        self.__location = location

    def set_total_rooms(self, total_rooms: int) -> None:
        """Set total rooms."""
        self.__total_rooms = total_rooms

    def set_warden_id(self, warden_id: str) -> None:
        """Set warden staff ID."""
        self.__warden_id = warden_id

    def set_status(self, status: str) -> None:
        """Set hostel status."""
        self.__status = status

    # --- Serialization Helpers ---

    def to_dict(self) -> Dict[str, Any]:
        """Convert hostel object to dictionary representation."""
        return {
            "hostel_id": self.get_hostel_id(),
            "hostel_name": self.get_hostel_name(),
            "gender_category": self.get_gender_category(),
            "location": self.get_location(),
            "total_rooms": self.get_total_rooms(),
            "warden_id": self.get_warden_id(),
            "status": self.get_status(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Hostel":
        """Instantiate Hostel from dictionary representation."""
        return cls(
            hostel_id=data.get("hostel_id", ""),
            hostel_name=data.get("hostel_name", ""),
            gender_category=data.get("gender_category", ""),
            location=data.get("location", ""),
            total_rooms=int(data.get("total_rooms", 0)),
            warden_id=data.get("warden_id", ""),
            status=data.get("status", "Active"),
        )
