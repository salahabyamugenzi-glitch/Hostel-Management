"""
Student Model (Child Class of User).
Demonstrates Inheritance (inherits from User) and Encapsulation.
Contains private attributes specific to students with public getters and setters.
"""

from typing import Dict, Any
from models.user import User


class Student(User):
    """
    Student class inheriting from User.
    Encapsulates student-specific attributes privately.
    """

    def __init__(
        self,
        first_name: str = "",
        last_name: str = "",
        gender: str = "",
        contact: str = "",
        address: str = "",
        password: str = "",
        registration_number: str = "",
        course: str = "",
        next_of_kin: str = "",
        next_of_kin_contact: str = "",
        hostel_id: str = "",
        room_number: str = "",
        bed_number: str = "",
        account_status: str = "Active",
        registration_date: str = "",
        registration_time: str = "",
    ):
        # Call parent class constructor to initialize inherited attributes
        super().__init__(first_name, last_name, gender, contact, address, password)

        # Student-specific private attributes
        self.__registration_number: str = registration_number
        self.__course: str = course
        self.__next_of_kin: str = next_of_kin
        self.__next_of_kin_contact: str = next_of_kin_contact
        self.__hostel_id: str = hostel_id
        self.__room_number: str = room_number
        self.__bed_number: str = bed_number
        self.__account_status: str = account_status
        self.__registration_date: str = registration_date
        self.__registration_time: str = registration_time

    # --- Getters ---

    def get_registration_number(self) -> str:
        """Get student registration number."""
        return self.__registration_number

    def get_course(self) -> str:
        """Get student enrolled course."""
        return self.__course

    def get_next_of_kin(self) -> str:
        """Get name of next of kin."""
        return self.__next_of_kin

    def get_next_of_kin_contact(self) -> str:
        """Get contact phone number of next of kin."""
        return self.__next_of_kin_contact

    def get_hostel_id(self) -> str:
        """Get assigned hostel ID."""
        return self.__hostel_id

    def get_room_number(self) -> str:
        """Get assigned room number."""
        return self.__room_number

    def get_bed_number(self) -> str:
        """Get assigned bed number."""
        return self.__bed_number

    def get_account_status(self) -> str:
        """Get student account status."""
        return self.__account_status

    def get_registration_date(self) -> str:
        """Get account registration date."""
        return self.__registration_date

    def get_registration_time(self) -> str:
        """Get account registration time."""
        return self.__registration_time

    # --- Setters ---

    def set_registration_number(self, registration_number: str) -> None:
        """Set student registration number."""
        self.__registration_number = registration_number

    def set_course(self, course: str) -> None:
        """Set student enrolled course."""
        self.__course = course

    def set_next_of_kin(self, next_of_kin: str) -> None:
        """Set name of next of kin."""
        self.__next_of_kin = next_of_kin

    def set_next_of_kin_contact(self, next_of_kin_contact: str) -> None:
        """Set contact of next of kin."""
        self.__next_of_kin_contact = next_of_kin_contact

    def set_hostel_id(self, hostel_id: str) -> None:
        """Set assigned hostel ID."""
        self.__hostel_id = hostel_id

    def set_room_number(self, room_number: str) -> None:
        """Set assigned room number."""
        self.__room_number = room_number

    def set_bed_number(self, bed_number: str) -> None:
        """Set assigned bed number."""
        self.__bed_number = bed_number

    def set_account_status(self, account_status: str) -> None:
        """Set account status."""
        self.__account_status = account_status

    def set_registration_date(self, registration_date: str) -> None:
        """Set account registration date."""
        self.__registration_date = registration_date

    def set_registration_time(self, registration_time: str) -> None:
        """Set account registration time."""
        self.__registration_time = registration_time

    # --- Serialization Helpers ---

    def to_dict(self) -> Dict[str, Any]:
        """Convert student object to dictionary representation for JSON persistence."""
        data = self.to_user_dict()
        data.update({
            "registration_number": self.get_registration_number(),
            "course": self.get_course(),
            "next_of_kin": self.get_next_of_kin(),
            "next_of_kin_contact": self.get_next_of_kin_contact(),
            "hostel_id": self.get_hostel_id(),
            "room_number": self.get_room_number(),
            "bed_number": self.get_bed_number(),
            "account_status": self.get_account_status(),
            "registration_date": self.get_registration_date(),
            "registration_time": self.get_registration_time(),
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Instantiate a Student object from a dictionary using public setters/constructors."""
        return cls(
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            gender=data.get("gender", ""),
            contact=data.get("contact", ""),
            address=data.get("address", ""),
            password=data.get("password", ""),
            registration_number=data.get("registration_number", ""),
            course=data.get("course", ""),
            next_of_kin=data.get("next_of_kin", ""),
            next_of_kin_contact=data.get("next_of_kin_contact", ""),
            hostel_id=data.get("hostel_id", ""),
            room_number=data.get("room_number", ""),
            bed_number=data.get("bed_number", ""),
            account_status=data.get("account_status", "Active"),
            registration_date=data.get("registration_date", ""),
            registration_time=data.get("registration_time", ""),
        )
