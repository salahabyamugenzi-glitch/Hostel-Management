"""
Student Service.
Handles student profile display, profile updates, and account deletion
(which releases the allocated hostel bed and deletes the record from students.json).
"""

import os
from typing import Optional, List, Dict, Any
from models.student import Student
from services.hostel_service import HostelService
from utilities.json_handler import JSONHandler
from utilities.menu_helpers import MenuHelpers
from utilities.password_helper import verify_password


class StudentService:
    """Service to handle student profile inquiries and account deletion."""

    def __init__(self, base_data_dir: Optional[str] = None):
        if base_data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.__data_dir = os.path.join(base_dir, "data")
        else:
            self.__data_dir = base_data_dir

        self.__students_file = os.path.join(self.__data_dir, "students.json")
        self.__hostel_service = HostelService(os.path.join(self.__data_dir, "hostels.json"))

    def view_profile(self, student: Student) -> None:
        """Display detailed student profile."""
        hostel = self.__hostel_service.get_hostel_by_id(student.get_hostel_id())
        hostel_name = hostel.get_hostel_name() if hostel else student.get_hostel_id()

        MenuHelpers.display_banner("STUDENT PROFILE")
        print(f" Registration Number : {student.get_registration_number()}")
        print(f" Full Name           : {student.get_full_name()}")
        print(f" Gender              : {student.get_gender()}")
        print(f" Course              : {student.get_course()}")
        print(f" Contact             : {student.get_contact()}")
        print(f" Address             : {student.get_address()}")
        print("-" * 50)
        print(f" Assigned Hostel     : {hostel_name} ({student.get_hostel_id()})")
        print(f" Room Number         : Room {student.get_room_number()}")
        print(f" Bed Number          : {student.get_bed_number()}")
        print("-" * 50)
        print(f" Next of Kin         : {student.get_next_of_kin()}")
        print(f" Next of Kin Contact : {student.get_next_of_kin_contact()}")
        print(f" Account Status      : {student.get_account_status()}")
        print(f" Registered On       : {student.get_registration_date()} at {student.get_registration_time()}")
        print("=" * 50)
        MenuHelpers.pause()

    def delete_account(self, student: Student) -> bool:
        """
        Delete Account workflow:
        Requires password confirmation + explicit confirmation.
        Frees allocated bed in hostels.json and removes student record from students.json.
        Returns True if account was deleted, False otherwise.
        """
        MenuHelpers.display_banner("DELETE STUDENT ACCOUNT")
        print("WARNING: This action is permanent!")
        print("All your hostel allocations will be released immediately.\n")

        # Confirm password
        entered_password = input("Enter your password to verify account ownership: ").strip()
        if not verify_password(entered_password, student.get_password()):
            print("\n[Error] Incorrect password. Account deletion aborted.")
            MenuHelpers.pause()
            return False

        # Final Confirmation
        confirm = input("Are you absolutely sure you want to delete your account? (Type 'YES' to confirm): ").strip()
        if confirm != "YES":
            print("\nAccount deletion cancelled.")
            MenuHelpers.pause()
            return False

        # 1. Free Bed in hostels.json
        self.__hostel_service.release_bed(
            student.get_hostel_id(),
            student.get_room_number(),
            student.get_bed_number(),
        )

        # 2. Remove record from students.json
        students_data: List[Dict[str, Any]] = JSONHandler.read_json(self.__students_file, default_data=[])
        updated_list = [
            s for s in students_data
            if s.get("registration_number", "").strip().upper() != student.get_registration_number().strip().upper()
        ]
        JSONHandler.write_json(self.__students_file, updated_list)

        print("\n[Success] Your account has been deleted and your bed has been freed.")
        MenuHelpers.pause()
        return True
