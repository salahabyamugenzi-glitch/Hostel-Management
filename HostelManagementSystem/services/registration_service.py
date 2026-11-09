"""
Registration Service.
Handles student and staff registration flows, ID auto-generation,
gender-based hostel/room/bed allocation, input validation, and JSON persistence.
"""

import os
from typing import Optional, List, Dict, Any
from models.student import Student
from models.staff import Staff
from services.hostel_service import HostelService
from utilities.id_generator import IDGenerator
from utilities.validators import Validators
from utilities.date_time_helper import get_current_date, get_current_time
from utilities.json_handler import JSONHandler
from utilities.menu_helpers import MenuHelpers
from utilities.password_helper import hash_password


class RegistrationService:
    """Service to handle student and staff registration procedures."""

    def __init__(self, base_data_dir: Optional[str] = None):
        if base_data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.__data_dir = os.path.join(base_dir, "data")
        else:
            self.__data_dir = base_data_dir

        self.__students_file = os.path.join(self.__data_dir, "students.json")
        self.__staff_file = os.path.join(self.__data_dir, "staff.json")
        self.__hostel_service = HostelService(os.path.join(self.__data_dir, "hostels.json"))

        # Ensure files exist with empty arrays
        JSONHandler.ensure_file_exists(self.__students_file, [])
        JSONHandler.ensure_file_exists(self.__staff_file, [])

    # --- Student Registration ---

    def register_student(self) -> Optional[Student]:
        """
        Interactive console registration workflow for students.
        Returns newly registered Student instance or None if cancelled/failed.
        """
        MenuHelpers.display_banner("STUDENT REGISTRATION")
        print("Please enter the required information accurately.\n")

        # 1. First Name
        while True:
            first_name = input("Enter First Name: ").strip()
            valid, msg = Validators.validate_name(first_name, "First Name")
            if valid:
                break
            print(f"[Error] {msg}")

        # 2. Last Name
        while True:
            last_name = input("Enter Last Name: ").strip()
            valid, msg = Validators.validate_name(last_name, "Last Name")
            if valid:
                break
            print(f"[Error] {msg}")

        # 3. Gender
        while True:
            print("\nSelect Gender:")
            print("1. Male")
            print("2. Female")
            g_choice = input("Enter choice (1/2): ").strip()
            if g_choice == "1":
                gender = "Male"
                break
            elif g_choice == "2":
                gender = "Female"
                break
            print("[Error] Please select 1 for Male or 2 for Female.")

        # 4. Contact
        while True:
            contact = input("\nEnter Contact Number (e.g. 0771234567 or +256771234567): ").strip()
            valid, msg = Validators.validate_contact(contact)
            if valid:
                break
            print(f"[Error] {msg}")

        # 5. Address
        while True:
            address = input("Enter Address/Home District: ").strip()
            valid, msg = Validators.validate_non_empty(address, "Address")
            if valid:
                break
            print(f"[Error] {msg}")

        # 6. Course
        while True:
            course = input("Enter Enrolled Course (e.g. BSc Computer Science): ").strip()
            valid, msg = Validators.validate_non_empty(course, "Course")
            if valid:
                break
            print(f"[Error] {msg}")

        # 7. Next of Kin Name
        while True:
            next_of_kin = input("Enter Next of Kin Full Name: ").strip()
            valid, msg = Validators.validate_name(next_of_kin, "Next of Kin")
            if valid:
                break
            print(f"[Error] {msg}")

        # 8. Next of Kin Contact
        while True:
            nok_contact = input("Enter Next of Kin Contact Number: ").strip()
            valid, msg = Validators.validate_contact(nok_contact)
            if valid:
                break
            print(f"[Error] {msg}")

        # 9. Password
        while True:
            password = input("Create Password (min 6 characters): ").strip()
            valid, msg = Validators.validate_password(password)
            if valid:
                break
            print(f"[Error] {msg}")

        # 10. Hostel, Room, and Bed Allocation
        MenuHelpers.display_sub_header(f"HOSTEL SELECTION (Gender Category: {gender})")
        matching_hostels = self.__hostel_service.get_hostels_by_gender(gender)
        if not matching_hostels:
            print(f"[Error] No hostels currently available for {gender} students.")
            MenuHelpers.pause()
            return None

        print("Available Hostels:")
        for idx, h in enumerate(matching_hostels, 1):
            print(f"{idx}. {h.get_hostel_name()} ({h.get_location()})")

        h_idx = MenuHelpers.get_menu_choice(1, len(matching_hostels), "Select Hostel: ")
        selected_hostel = matching_hostels[h_idx - 1]

        # Room Selection
        available_rooms = self.__hostel_service.get_available_rooms(selected_hostel.get_hostel_id())
        if not available_rooms:
            print(f"\n[Error] Sorry, {selected_hostel.get_hostel_name()} currently has no rooms with available beds.")
            MenuHelpers.pause()
            return None

        MenuHelpers.display_sub_header(f"ROOM SELECTION ({selected_hostel.get_hostel_name()})")
        print("Available Rooms:")
        for idx, r in enumerate(available_rooms, 1):
            print(f"{idx}. Room {r.get_room_number()} (Capacity: {r.get_capacity()}, Free Beds: {r.get_available_beds()})")

        r_idx = MenuHelpers.get_menu_choice(1, len(available_rooms), "Select Room: ")
        selected_room = available_rooms[r_idx - 1]

        # Bed Selection
        available_beds = self.__hostel_service.get_available_beds(
            selected_hostel.get_hostel_id(), selected_room.get_room_number()
        )
        if not available_beds:
            print("\n[Error] No available beds found in the selected room.")
            MenuHelpers.pause()
            return None

        MenuHelpers.display_sub_header(f"BED SELECTION (Room {selected_room.get_room_number()})")
        print("Available Beds:")
        for idx, b in enumerate(available_beds, 1):
            print(f"{idx}. {b.get_bed_number()} [Status: {b.get_status()}]")

        b_idx = MenuHelpers.get_menu_choice(1, len(available_beds), "Select Bed: ")
        selected_bed = available_beds[b_idx - 1]

        # Commit bed allocation
        alloc_success = self.__hostel_service.allocate_bed(
            selected_hostel.get_hostel_id(),
            selected_room.get_room_number(),
            selected_bed.get_bed_number(),
        )
        if not alloc_success:
            print("\n[Error] Failed to allocate bed. Please try again.")
            MenuHelpers.pause()
            return None

        # 11. ID Generation and Timestamps
        raw_students = JSONHandler.read_json(self.__students_file, default_data=[])
        existing_reg_nos = [s.get("registration_number", "") for s in raw_students]
        reg_number = IDGenerator.generate_student_registration_number(existing_reg_nos)

        reg_date = get_current_date()
        reg_time = get_current_time()

        # 12. Create encapsulated Student model
        new_student = Student(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            contact=contact,
            address=address,
            password=hash_password(password),
            registration_number=reg_number,
            course=course,
            next_of_kin=next_of_kin,
            next_of_kin_contact=nok_contact,
            hostel_id=selected_hostel.get_hostel_id(),
            room_number=selected_room.get_room_number(),
            bed_number=selected_bed.get_bed_number(),
            account_status="Active",
            registration_date=reg_date,
            registration_time=reg_time,
        )

        # 13. Persist to students.json
        raw_students.append(new_student.to_dict())
        if not JSONHandler.write_json(self.__students_file, raw_students):
            self.__hostel_service.release_bed(
                selected_hostel.get_hostel_id(),
                selected_room.get_room_number(),
                selected_bed.get_bed_number(),
            )
            print("\n[Error] Registration could not be saved; the bed was released.")
            MenuHelpers.pause()
            return None

        # 14. Display Success Banner
        MenuHelpers.display_banner("REGISTRATION SUCCESSFUL!")
        print(f" Full Name   : {new_student.get_full_name()}")
        print(f" Reg Number  : {new_student.get_registration_number()}")
        print(f" Hostel      : {selected_hostel.get_hostel_name()} ({selected_hostel.get_hostel_id()})")
        print(f" Room Number : Room {new_student.get_room_number()}")
        print(f" Bed Number  : {new_student.get_bed_number()}")
        print(f" Registered  : {new_student.get_registration_date()} at {new_student.get_registration_time()}")
        print("=" * 50)
        print("Note: Please keep your Registration Number and Password safe for login.")
        MenuHelpers.pause()
        return new_student

    # --- Staff Registration ---

    def register_staff(self) -> Optional[Staff]:
        """
        Interactive console registration workflow for staff members.
        Returns newly registered Staff instance or None if cancelled/failed.
        """
        MenuHelpers.display_banner("STAFF REGISTRATION")
        print("Please enter the required staff details.\n")

        # First Name
        while True:
            first_name = input("Enter First Name: ").strip()
            valid, msg = Validators.validate_name(first_name, "First Name")
            if valid:
                break
            print(f"[Error] {msg}")

        # Last Name
        while True:
            last_name = input("Enter Last Name: ").strip()
            valid, msg = Validators.validate_name(last_name, "Last Name")
            if valid:
                break
            print(f"[Error] {msg}")

        # Gender
        while True:
            print("\nSelect Gender:")
            print("1. Male")
            print("2. Female")
            g_choice = input("Enter choice (1/2): ").strip()
            if g_choice == "1":
                gender = "Male"
                break
            elif g_choice == "2":
                gender = "Female"
                break
            print("[Error] Please select 1 for Male or 2 for Female.")

        # Contact
        while True:
            contact = input("\nEnter Contact Number: ").strip()
            valid, msg = Validators.validate_contact(contact)
            if valid:
                break
            print(f"[Error] {msg}")

        # Address
        while True:
            address = input("Enter Residential Address: ").strip()
            valid, msg = Validators.validate_non_empty(address, "Address")
            if valid:
                break
            print(f"[Error] {msg}")

        # Role
        roles = ["Hostel Warden", "Assistant Warden", "Caretaker", "Maintenance Officer", "Matron"]
        print("\nSelect Staff Role:")
        for idx, r in enumerate(roles, 1):
            print(f"{idx}. {r}")
        r_choice = MenuHelpers.get_menu_choice(1, len(roles), "Select Role: ")
        role = roles[r_choice - 1]

        # Department
        departments = ["Hostel Administration", "Student Welfare", "Facilities & Maintenance", "Security & Safety"]
        print("\nSelect Department:")
        for idx, d in enumerate(departments, 1):
            print(f"{idx}. {d}")
        d_choice = MenuHelpers.get_menu_choice(1, len(departments), "Select Department: ")
        department = departments[d_choice - 1]

        # Password
        while True:
            password = input("\nCreate Password (min 6 characters): ").strip()
            valid, msg = Validators.validate_password(password)
            if valid:
                break
            print(f"[Error] {msg}")

        # ID Generation & Timestamps
        raw_staff = JSONHandler.read_json(self.__staff_file, default_data=[])
        existing_staff_ids = [s.get("staff_id", "") for s in raw_staff]
        staff_id = IDGenerator.generate_staff_id(existing_staff_ids)

        reg_date = get_current_date()
        reg_time = get_current_time()

        # Create encapsulated Staff model
        new_staff = Staff(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            contact=contact,
            address=address,
            password=hash_password(password),
            staff_id=staff_id,
            role=role,
            department=department,
            account_status="Active",
            registration_date=reg_date,
            registration_time=reg_time,
        )

        # Persist to staff.json
        raw_staff.append(new_staff.to_dict())
        JSONHandler.write_json(self.__staff_file, raw_staff)

        # Display Success Banner
        MenuHelpers.display_banner("STAFF REGISTRATION SUCCESSFUL!")
        print(f" Full Name   : {new_staff.get_full_name()}")
        print(f" Staff ID    : {new_staff.get_staff_id()}")
        print(f" Role        : {new_staff.get_role()}")
        print(f" Department  : {new_staff.get_department()}")
        print(f" Registered  : {new_staff.get_registration_date()} at {new_staff.get_registration_time()}")
        print("=" * 50)
        print("Note: Use your Staff ID and Password to login.")
        MenuHelpers.pause()
        return new_staff
