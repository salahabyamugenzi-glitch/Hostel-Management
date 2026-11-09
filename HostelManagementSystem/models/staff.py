"""
Staff Model (Child Class of User).
Demonstrates Inheritance (inherits from User) and Encapsulation.
Contains private attributes specific to staff members with public getters and setters.
"""

from typing import Dict, Any
from models.user import User


class Staff(User):
    """
    Staff class inheriting from User.
    Encapsulates staff-specific attributes privately.
    """

    def __init__(
        self,
        first_name: str = "",
        last_name: str = "",
        gender: str = "",
        contact: str = "",
        address: str = "",
        password: str = "",
        staff_id: str = "",
        role: str = "",
        department: str = "",
        account_status: str = "Active",
        registration_date: str = "",
        registration_time: str = "",
    ):
        # Call parent class constructor to initialize inherited attributes
        super().__init__(first_name, last_name, gender, contact, address, password)

        # Staff-specific private attributes
        self.__staff_id: str = staff_id
        self.__role: str = role
        self.__department: str = department
        self.__account_status: str = account_status
        self.__registration_date: str = registration_date
        self.__registration_time: str = registration_time

    # --- Getters ---

    def get_staff_id(self) -> str:
        """Get staff ID."""
        return self.__staff_id

    def get_role(self) -> str:
        """Get staff role (e.g. Warden, Caretaker)."""
        return self.__role

    def get_department(self) -> str:
        """Get staff department."""
        return self.__department

    def get_account_status(self) -> str:
        """Get staff account status."""
        return self.__account_status

    def get_registration_date(self) -> str:
        """Get staff registration date."""
        return self.__registration_date

    def get_registration_time(self) -> str:
        """Get staff registration time."""
        return self.__registration_time

    def get_profile_summary(self) -> str:
        """Return the staff-specific profile summary."""
        return (
            f"Staff: {self.get_full_name()}\n"
            f"Staff ID: {self.get_staff_id()}\n"
            f"Role: {self.get_role()}\n"
            f"Department: {self.get_department()}\n"
            f"Account Status: {self.get_account_status()}"
        )

    # --- Setters ---

    def set_staff_id(self, staff_id: str) -> None:
        """Set staff ID."""
        self.__staff_id = staff_id

    def set_role(self, role: str) -> None:
        """Set staff role."""
        self.__role = role

    def set_department(self, department: str) -> None:
        """Set staff department."""
        self.__department = department

    def set_account_status(self, account_status: str) -> None:
        """Set staff account status."""
        self.__account_status = account_status

    def set_registration_date(self, registration_date: str) -> None:
        """Set registration date."""
        self.__registration_date = registration_date

    def set_registration_time(self, registration_time: str) -> None:
        """Set registration time."""
        self.__registration_time = registration_time

    # --- Serialization Helpers ---

    def to_dict(self) -> Dict[str, Any]:
        """Convert staff object to dictionary representation for JSON persistence."""
        data = self.to_user_dict()
        data.update({
            "staff_id": self.get_staff_id(),
            "role": self.get_role(),
            "department": self.get_department(),
            "account_status": self.get_account_status(),
            "registration_date": self.get_registration_date(),
            "registration_time": self.get_registration_time(),
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Staff":
        """Instantiate a Staff object from a dictionary using public setters/constructors."""
        return cls(
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            gender=data.get("gender", ""),
            contact=data.get("contact", ""),
            address=data.get("address", ""),
            password=data.get("password", ""),
            staff_id=data.get("staff_id", ""),
            role=data.get("role", ""),
            department=data.get("department", ""),
            account_status=data.get("account_status", "Active"),
            registration_date=data.get("registration_date", ""),
            registration_time=data.get("registration_time", ""),
        )
