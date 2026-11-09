"""
Password Reset Service.
Verifies user identity by matching ID (Student Reg No or Staff ID) with contact number,
validates the new password, updates the JSON file, and records the reset timestamp.
"""

import os
from typing import Optional, List, Dict, Any
from utilities.validators import Validators
from utilities.date_time_helper import get_timestamp
from utilities.json_handler import JSONHandler
from utilities.menu_helpers import MenuHelpers
from utilities.password_helper import hash_password


class PasswordResetService:
    """Service handling password recovery and update workflows."""

    def __init__(self, base_data_dir: Optional[str] = None):
        if base_data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.__data_dir = os.path.join(base_dir, "data")
        else:
            self.__data_dir = base_data_dir

        self.__students_file = os.path.join(self.__data_dir, "students.json")
        self.__staff_file = os.path.join(self.__data_dir, "staff.json")

    def reset_student_password(self) -> bool:
        """Interactive password reset workflow for students."""
        MenuHelpers.display_banner("STUDENT PASSWORD RESET")
        reg_no = input("Enter your Registration Number: ").strip()
        contact = input("Enter your registered Contact Number: ").strip()

        if not contact:
            print("\n[Error] Contact number cannot be empty.")
            MenuHelpers.pause()
            return False

        students: List[Dict[str, Any]] = JSONHandler.read_json(self.__students_file, default_data=[])
        target_student: Optional[Dict[str, Any]] = None

        for s in students:
            # Normalize contact for robust matching
            s_contact = s.get("contact", "").strip().replace(" ", "").replace("-", "")
            entered_contact = contact.replace(" ", "").replace("-", "")
            if s.get("registration_number", "").strip().upper() == reg_no.upper() and (
                s_contact == entered_contact
                or (len(entered_contact) >= 9 and s_contact.endswith(entered_contact[-9:]))
            ):
                target_student = s
                break

        if not target_student:
            print("\n[Error] Verification failed. Registration number and contact number do not match our records.")
            MenuHelpers.pause()
            return False

        print(f"\nIdentity Verified for: {target_student.get('first_name')} {target_student.get('last_name')}")

        while True:
            new_password = input("Enter New Password (min 6 characters): ").strip()
            valid, msg = Validators.validate_password(new_password)
            if not valid:
                print(f"[Error] {msg}")
                continue

            confirm_password = input("Confirm New Password: ").strip()
            if new_password != confirm_password:
                print("[Error] Passwords do not match. Please try again.")
                continue
            break

        # Update record
        target_student["password"] = hash_password(new_password)
        target_student["last_password_reset"] = get_timestamp()

        JSONHandler.write_json(self.__students_file, students)
        print("\n[Success] Your password has been successfully reset!")
        print(f"Timestamp: {target_student['last_password_reset']}")
        MenuHelpers.pause()
        return True

    def reset_staff_password(self) -> bool:
        """Interactive password reset workflow for staff members."""
        MenuHelpers.display_banner("STAFF PASSWORD RESET")
        staff_id = input("Enter your Staff ID (e.g. STF001): ").strip().upper()
        contact = input("Enter your registered Contact Number: ").strip()

        if not contact:
            print("\n[Error] Contact number cannot be empty.")
            MenuHelpers.pause()
            return False

        staff_list: List[Dict[str, Any]] = JSONHandler.read_json(self.__staff_file, default_data=[])
        target_staff: Optional[Dict[str, Any]] = None

        for s in staff_list:
            s_contact = s.get("contact", "").strip().replace(" ", "").replace("-", "")
            entered_contact = contact.replace(" ", "").replace("-", "")
            if s.get("staff_id", "").strip().upper() == staff_id and (
                s_contact == entered_contact
                or (len(entered_contact) >= 9 and s_contact.endswith(entered_contact[-9:]))
            ):
                target_staff = s
                break

        if not target_staff:
            print("\n[Error] Verification failed. Staff ID and contact number do not match our records.")
            MenuHelpers.pause()
            return False

        print(f"\nIdentity Verified for: {target_staff.get('first_name')} {target_staff.get('last_name')}")

        while True:
            new_password = input("Enter New Password (min 6 characters): ").strip()
            valid, msg = Validators.validate_password(new_password)
            if not valid:
                print(f"[Error] {msg}")
                continue

            confirm_password = input("Confirm New Password: ").strip()
            if new_password != confirm_password:
                print("[Error] Passwords do not match. Please try again.")
                continue
            break

        # Update record
        target_staff["password"] = hash_password(new_password)
        target_staff["last_password_reset"] = get_timestamp()

        JSONHandler.write_json(self.__staff_file, staff_list)
        print("\n[Success] Your staff password has been successfully reset!")
        print(f"Timestamp: {target_staff['last_password_reset']}")
        MenuHelpers.pause()
        return True
