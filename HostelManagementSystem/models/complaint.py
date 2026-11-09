"""
Complaint Model.
Demonstrates Encapsulation with private attributes and public getters and setters.
"""

from typing import Dict, Any


class Complaint:
    """
    Complaint class representing an issue reported by a student.
    Encapsulates complaint details privately.
    """

    def __init__(
        self,
        complaint_id: str = "",
        registration_number: str = "",
        title: str = "",
        description: str = "",
        complaint_date: str = "",
        complaint_time: str = "",
        status: str = "Pending",
        priority: str = "Medium",
        assigned_staff: str = "Unassigned",
        resolution_comment: str = "None",
    ):
        self.__complaint_id: str = complaint_id
        self.__registration_number: str = registration_number
        self.__title: str = title
        self.__description: str = description
        self.__complaint_date: str = complaint_date
        self.__complaint_time: str = complaint_time
        self.__status: str = status
        self.__priority: str = priority
        self.__assigned_staff: str = assigned_staff
        self.__resolution_comment: str = resolution_comment

    # --- Getters ---

    def get_complaint_id(self) -> str:
        """Get complaint ID."""
        return self.__complaint_id

    def get_registration_number(self) -> str:
        """Get student registration number who raised the complaint."""
        return self.__registration_number

    def get_title(self) -> str:
        """Get complaint title."""
        return self.__title

    def get_description(self) -> str:
        """Get complaint description."""
        return self.__description

    def get_complaint_date(self) -> str:
        """Get date the complaint was raised."""
        return self.__complaint_date

    def get_complaint_time(self) -> str:
        """Get time the complaint was raised."""
        return self.__complaint_time

    def get_status(self) -> str:
        """Get complaint status (Pending / In Progress / Resolved)."""
        return self.__status

    def get_priority(self) -> str:
        """Get complaint priority (Low / Medium / High)."""
        return self.__priority

    def get_assigned_staff(self) -> str:
        """Get assigned staff ID."""
        return self.__assigned_staff

    def get_resolution_comment(self) -> str:
        """Get resolution comment / feedback."""
        return self.__resolution_comment

    # --- Setters ---

    def set_complaint_id(self, complaint_id: str) -> None:
        """Set complaint ID."""
        self.__complaint_id = complaint_id

    def set_registration_number(self, registration_number: str) -> None:
        """Set student registration number."""
        self.__registration_number = registration_number

    def set_title(self, title: str) -> None:
        """Set complaint title."""
        self.__title = title

    def set_description(self, description: str) -> None:
        """Set complaint description."""
        self.__description = description

    def set_complaint_date(self, complaint_date: str) -> None:
        """Set complaint date."""
        self.__complaint_date = complaint_date

    def set_complaint_time(self, complaint_time: str) -> None:
        """Set complaint time."""
        self.__complaint_time = complaint_time

    def set_status(self, status: str) -> None:
        """Set complaint status."""
        self.__status = status

    def set_priority(self, priority: str) -> None:
        """Set complaint priority."""
        self.__priority = priority

    def set_assigned_staff(self, assigned_staff: str) -> None:
        """Set assigned staff ID."""
        self.__assigned_staff = assigned_staff

    def set_resolution_comment(self, resolution_comment: str) -> None:
        """Set resolution comment."""
        self.__resolution_comment = resolution_comment

    # --- Serialization Helpers ---

    def to_dict(self) -> Dict[str, Any]:
        """Convert complaint object to dictionary representation."""
        return {
            "complaint_id": self.get_complaint_id(),
            "registration_number": self.get_registration_number(),
            "title": self.get_title(),
            "description": self.get_description(),
            "complaint_date": self.get_complaint_date(),
            "complaint_time": self.get_complaint_time(),
            "status": self.get_status(),
            "priority": self.get_priority(),
            "assigned_staff": self.get_assigned_staff(),
            "resolution_comment": self.get_resolution_comment(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Complaint":
        """Instantiate Complaint from dictionary representation."""
        return cls(
            complaint_id=data.get("complaint_id", ""),
            registration_number=data.get("registration_number", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            complaint_date=data.get("complaint_date", ""),
            complaint_time=data.get("complaint_time", ""),
            status=data.get("status", "Pending"),
            priority=data.get("priority", "Medium"),
            assigned_staff=data.get("assigned_staff", "Unassigned"),
            resolution_comment=data.get("resolution_comment", "None"),
        )
