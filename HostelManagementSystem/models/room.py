"""
Room Model.
Demonstrates Encapsulation with private attributes and public getters and setters.
"""

from typing import Dict, Any


class Room:
    """
    Room class representing a student accommodation unit.
    Encapsulates room details privately.
    """

    def __init__(
        self,
        room_number: str = "",
        hostel_id: str = "",
        capacity: int = 0,
        occupied_beds: int = 0,
        room_status: str = "Empty",
        available_beds: int = 0,
    ):
        self.__room_number: str = room_number
        self.__hostel_id: str = hostel_id
        self.__capacity: int = capacity
        self.__occupied_beds: int = occupied_beds
        self.__room_status: str = room_status
        self.__available_beds: int = available_beds

    # --- Getters ---

    def get_room_number(self) -> str:
        """Get room number."""
        return self.__room_number

    def get_hostel_id(self) -> str:
        """Get hostel ID to which the room belongs."""
        return self.__hostel_id

    def get_capacity(self) -> int:
        """Get total bed capacity of room."""
        return self.__capacity

    def get_occupied_beds(self) -> int:
        """Get number of occupied beds."""
        return self.__occupied_beds

    def get_room_status(self) -> str:
        """Get room status (Empty, Available, or Filled)."""
        return self.__room_status

    def get_available_beds(self) -> int:
        """Get number of remaining available beds."""
        return self.__available_beds

    # --- Setters ---

    def set_room_number(self, room_number: str) -> None:
        """Set room number."""
        self.__room_number = room_number

    def set_hostel_id(self, hostel_id: str) -> None:
        """Set hostel ID."""
        self.__hostel_id = hostel_id

    def set_capacity(self, capacity: int) -> None:
        """Set total bed capacity."""
        self.__capacity = capacity

    def set_occupied_beds(self, occupied_beds: int) -> None:
        """Set occupied beds count."""
        self.__occupied_beds = occupied_beds

    def set_room_status(self, room_status: str) -> None:
        """Set room status."""
        self.__room_status = room_status

    def set_available_beds(self, available_beds: int) -> None:
        """Set available beds count."""
        self.__available_beds = available_beds

    # --- Business Logic Helpers ---

    def update_occupancy(self, occupied: int) -> None:
        """Update bed counts and set room status accordingly."""
        self.__occupied_beds = occupied
        self.__available_beds = max(0, self.__capacity - occupied)
        if self.__occupied_beds >= self.__capacity:
            self.__room_status = "Filled"
        elif self.__occupied_beds == 0:
            self.__room_status = "Empty"
        else:
            self.__room_status = "Available"

    # --- Serialization Helpers ---

    def to_dict(self) -> Dict[str, Any]:
        """Convert room object to dictionary representation."""
        return {
            "room_number": self.get_room_number(),
            "hostel_id": self.get_hostel_id(),
            "capacity": self.get_capacity(),
            "occupied_beds": self.get_occupied_beds(),
            "room_status": self.get_room_status(),
            "available_beds": self.get_available_beds(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Room":
        """Instantiate Room from dictionary representation."""
        return cls(
            room_number=data.get("room_number", ""),
            hostel_id=data.get("hostel_id", ""),
            capacity=int(data.get("capacity", 0)),
            occupied_beds=int(data.get("occupied_beds", 0)),
            room_status=data.get("room_status", "Empty"),
            available_beds=int(data.get("available_beds", 0)),
        )
