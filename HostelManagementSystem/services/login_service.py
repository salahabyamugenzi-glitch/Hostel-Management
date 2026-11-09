"""
Login Service.
Handles student and staff authentication workflows with sub-menus offering:
1. Login
2. Reset Password
3. Back
"""

import os
from typing import Optional, Dict, Any, List
from models.student import Student
from models.staff import Staff
from services.password_reset_service import PasswordResetService
from utilities.json_handler import JSONHandler
from utilities.menu_helpers import MenuHelpers
from utilities.password_helper import verify_password


class LoginService:
    """Service to handle user authentication for Students and Staff."""

    def __init__(self, base_data_dir: Optional[str] = None):
        if base_data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.__data_dir = os.path.join(base_dir, "data")
        else:
            self.__data_dir = base_data_dir

        self.__students_file = os.path.join(self.__data_dir, "students.json")
        self.__staff_file = os.path.join(self.__data_dir, "staff.json")
        self.__reset_service = PasswordResetService(self.__data_dir)

    def handle_student_login_flow(self) -> Optional[Student]:
        """
        Sub-menu for Student Login:
        1. Login
        2. Reset Password
        3. Back
        """
        while True:
            MenuHelpers.display_menu(
                "STUDENT LOGIN MENU",
                ["Login", "Reset Password", "Back"]
            )
            choice = MenuHelpers.get_menu_choice(1, 3)

            if choice == 1:
                student = self.authenticate_student()
                if student:
                    return student
            elif choice == 2:
                self.__reset_service.reset_student_password()
            elif choice == 3:
                return None

    def handle_staff_login_flow(self) -> Optional[Staff]:
        """
        Sub-menu for Staff Login:
        1. Login
        2. Reset Password
        3. Back
        """
        while True:
            MenuHelpers.display_menu(
                "STAFF LOGIN MENU",
                ["Login", "Reset Password", "Back"]
            )
            choice = MenuHelpers.get_menu_choice(1, 3)

            if choice == 1:
                staff = self.authenticate_staff()
                if staff:
                    return staff
            elif choice == 2:
                self.__reset_service.reset_staff_password()
            elif choice == 3:
                return None

    def authenticate_student(self) -> Optional[Student]:
        """Verify Student registration number and password."""
        MenuHelpers.display_sub_header("STUDENT AUTHENTICATION")
        reg_number = input("Enter Registration Number: ").strip()
        password = input("Enter Password: ").strip()

        students: List[Dict[str, Any]] = JSONHandler.read_json(self.__students_file, default_data=[])
        for record in students:
            if (
                record.get("registration_number", "").strip().upper() == reg_number.upper()
                and verify_password(password, record.get("password", ""))
            ):
                if record.get("account_status", "Active") != "Active":
                    print("\n[Error] Your student account is marked inactive.")
                    MenuHelpers.pause()
                    return None
                print(f"\n[Success] Welcome back, {record.get('first_name')}!")
                MenuHelpers.pause()
                return Student.from_dict(record)

        print("\n[Error] Invalid registration number or password.")
        MenuHelpers.pause()
        return None

    def authenticate_staff(self) -> Optional[Staff]:
        """Verify Staff ID and password."""
        MenuHelpers.display_sub_header("STAFF AUTHENTICATION")
        staff_id = input("Enter Staff ID (e.g. STF001): ").strip().upper()
        password = input("Enter Password: ").strip()

        staff_list: List[Dict[str, Any]] = JSONHandler.read_json(self.__staff_file, default_data=[])
        for record in staff_list:
            if (
                record.get("staff_id", "").strip().upper() == staff_id
                and verify_password(password, record.get("password", ""))
            ):
                if record.get("account_status", "Active") != "Active":
                    print("\n[Error] Your staff account is marked inactive.")
                    MenuHelpers.pause()
                    return None
                print(f"\n[Success] Welcome back, {record.get('first_name')} ({record.get('role')})!")
                MenuHelpers.pause()
                return Staff.from_dict(record)

        print("\n[Error] Invalid Staff ID or password.")
        MenuHelpers.pause()
        return None
