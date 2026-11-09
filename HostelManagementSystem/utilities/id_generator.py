"""
ID Generator Utility.
Generates unique identifiers for Students, Staff, Payments, Complaints, and Transactions.
"""

import random
from typing import List, Set


class IDGenerator:
    """Provides methods for unique ID creation according to system requirements."""

    @staticmethod
    def generate_student_registration_number(existing_numbers: List[str]) -> str:
        """
        Generate a unique student registration number in the format XXX-XXXXXX-XXX.
        Example: 202-123456-001
        """
        existing_set: Set[str] = set(existing_numbers)
        while True:
            part1 = f"{random.randint(200, 299):03d}"
            part2 = f"{random.randint(100000, 999999):06d}"
            part3 = f"{random.randint(1, 999):03d}"
            reg_no = f"{part1}-{part2}-{part3}"
            if reg_no not in existing_set:
                return reg_no

    @staticmethod
    def generate_staff_id(existing_ids: List[str]) -> str:
        """
        Generate a unique sequential Staff ID: STF001, STF002, ...
        """
        existing_numbers = []
        for sid in existing_ids:
            if sid.startswith("STF") and sid[3:].isdigit():
                existing_numbers.append(int(sid[3:]))

        next_number = max(existing_numbers, default=0) + 1
        return f"STF{next_number:03d}"

    @staticmethod
    def generate_payment_id(existing_ids: List[str]) -> str:
        """
        Generate a unique Payment ID: PAY001, PAY002, ...
        """
        existing_numbers = []
        for pid in existing_ids:
            if pid.startswith("PAY") and pid[3:].isdigit():
                existing_numbers.append(int(pid[3:]))

        next_number = max(existing_numbers, default=0) + 1
        return f"PAY{next_number:03d}"

    @staticmethod
    def generate_complaint_id(existing_ids: List[str]) -> str:
        """
        Generate a unique Complaint ID: CMP001, CMP002, ...
        """
        existing_numbers = []
        for cid in existing_ids:
            if cid.startswith("CMP") and cid[3:].isdigit():
                existing_numbers.append(int(cid[3:]))

        next_number = max(existing_numbers, default=0) + 1
        return f"CMP{next_number:03d}"

    @staticmethod
    def generate_transaction_reference() -> str:
        """
        Generate a random uppercase alphanumeric transaction reference.
        Example: TXN-8F4A2B9C
        """
        hex_digits = "".join(random.choices("0123456789ABCDEF", k=8))
        return f"TXN-{hex_digits}"
