"""
Payment Model.
Demonstrates Encapsulation with private attributes and public getters and setters.
"""

from typing import Dict, Any


class Payment:
    """
    Payment class representing a fee payment record.
    Encapsulates transaction details privately.
    """

    def __init__(
        self,
        payment_id: str = "",
        registration_number: str = "",
        amount: float = 0.0,
        payment_method: str = "",
        semester: str = "",
        academic_year: str = "",
        payment_date: str = "",
        payment_time: str = "",
        status: str = "Completed",
        transaction_reference: str = "",
    ):
        self.__payment_id: str = payment_id
        self.__registration_number: str = registration_number
        self.__amount: float = amount
        self.__payment_method: str = payment_method
        self.__semester: str = semester
        self.__academic_year: str = academic_year
        self.__payment_date: str = payment_date
        self.__payment_time: str = payment_time
        self.__status: str = status
        self.__transaction_reference: str = transaction_reference

    # --- Getters ---

    def get_payment_id(self) -> str:
        """Get payment ID."""
        return self.__payment_id

    def get_registration_number(self) -> str:
        """Get student registration number associated with payment."""
        return self.__registration_number

    def get_amount(self) -> float:
        """Get payment amount."""
        return self.__amount

    def get_payment_method(self) -> str:
        """Get payment method (e.g. MTN Mobile Money, Airtel Mobile Money, Credit card)."""
        return self.__payment_method

    def get_semester(self) -> str:
        """Get semester (e.g. Semester I, Semester II)."""
        return self.__semester

    def get_academic_year(self) -> str:
        """Get academic year (e.g. 2026/2027)."""
        return self.__academic_year

    def get_payment_date(self) -> str:
        """Get payment date."""
        return self.__payment_date

    def get_payment_time(self) -> str:
        """Get payment time."""
        return self.__payment_time

    def get_status(self) -> str:
        """Get payment status (e.g. Completed)."""
        return self.__status

    def get_transaction_reference(self) -> str:
        """Get unique transaction reference."""
        return self.__transaction_reference

    # --- Setters ---

    def set_payment_id(self, payment_id: str) -> None:
        """Set payment ID."""
        self.__payment_id = payment_id

    def set_registration_number(self, registration_number: str) -> None:
        """Set student registration number."""
        self.__registration_number = registration_number

    def set_amount(self, amount: float) -> None:
        """Set payment amount."""
        self.__amount = amount

    def set_payment_method(self, payment_method: str) -> None:
        """Set payment method."""
        self.__payment_method = payment_method

    def set_semester(self, semester: str) -> None:
        """Set semester."""
        self.__semester = semester

    def set_academic_year(self, academic_year: str) -> None:
        """Set academic year."""
        self.__academic_year = academic_year

    def set_payment_date(self, payment_date: str) -> None:
        """Set payment date."""
        self.__payment_date = payment_date

    def set_payment_time(self, payment_time: str) -> None:
        """Set payment time."""
        self.__payment_time = payment_time

    def set_status(self, status: str) -> None:
        """Set payment status."""
        self.__status = status

    def set_transaction_reference(self, transaction_reference: str) -> None:
        """Set transaction reference."""
        self.__transaction_reference = transaction_reference

    # --- Serialization Helpers ---

    def to_dict(self) -> Dict[str, Any]:
        """Convert payment object to dictionary representation."""
        return {
            "payment_id": self.get_payment_id(),
            "registration_number": self.get_registration_number(),
            "amount": self.get_amount(),
            "payment_method": self.get_payment_method(),
            "semester": self.get_semester(),
            "academic_year": self.get_academic_year(),
            "payment_date": self.get_payment_date(),
            "payment_time": self.get_payment_time(),
            "status": self.get_status(),
            "transaction_reference": self.get_transaction_reference(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Payment":
        """Instantiate Payment from dictionary representation."""
        return cls(
            payment_id=data.get("payment_id", ""),
            registration_number=data.get("registration_number", ""),
            amount=float(data.get("amount", 0.0)),
            payment_method=data.get("payment_method", ""),
            semester=data.get("semester", ""),
            academic_year=data.get("academic_year", ""),
            payment_date=data.get("payment_date", ""),
            payment_time=data.get("payment_time", ""),
            status=data.get("status", "Completed"),
            transaction_reference=data.get("transaction_reference", ""),
        )
