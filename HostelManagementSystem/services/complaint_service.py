"""
Complaint Service.
Handles raising complaints by students, querying, searching,
and status updates by staff members.
Encapsulates complaints in models and JSON persistence.
"""

import os
from typing import List, Dict, Any, Optional
from models.complaint import Complaint
from utilities.id_generator import IDGenerator
from utilities.validators import Validators
from utilities.date_time_helper import get_current_date, get_current_time, get_timestamp
from utilities.json_handler import JSONHandler
from utilities.menu_helpers import MenuHelpers


class ComplaintService:
    """Service to manage complaint creation, lifecycle, and resolution."""

    def __init__(self, base_data_dir: Optional[str] = None):
        if base_data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.__data_dir = os.path.join(base_dir, "data")
        else:
            self.__data_dir = base_data_dir

        self.__complaints_file = os.path.join(self.__data_dir, "complaints.json")
        JSONHandler.ensure_file_exists(self.__complaints_file, [])

    def raise_complaint(self, registration_number: str) -> Optional[Complaint]:
        """
        Interactive workflow for a student to submit a complaint.
        """
        MenuHelpers.display_banner("RAISE A COMPLAINT")

        # 1. Title
        while True:
            title = input("Enter Complaint Title (e.g. Broken Water Pipe, Faulty Light): ").strip()
            valid, msg = Validators.validate_non_empty(title, "Complaint Title")
            if valid:
                break
            print(f"[Error] {msg}")

        # 2. Description
        while True:
            description = input("Enter Detailed Description: ").strip()
            valid, msg = Validators.validate_non_empty(description, "Description")
            if valid:
                break
            print(f"[Error] {msg}")

        # 3. Priority
        priorities = ["Low", "Medium", "High"]
        print("\nSelect Priority Level:")
        for idx, p in enumerate(priorities, 1):
            print(f"{idx}. {p}")
        p_choice = MenuHelpers.get_menu_choice(1, len(priorities))
        priority = priorities[p_choice - 1]

        # 4. Auto ID and Timestamps
        complaints_data = JSONHandler.read_json(self.__complaints_file, default_data=[])
        existing_ids = [c.get("complaint_id", "") for c in complaints_data]
        complaint_id = IDGenerator.generate_complaint_id(existing_ids)
        c_date = get_current_date()
        c_time = get_current_time()

        new_complaint = Complaint(
            complaint_id=complaint_id,
            registration_number=registration_number,
            title=title,
            description=description,
            complaint_date=c_date,
            complaint_time=c_time,
            status="Pending",
            priority=priority,
            assigned_staff="Unassigned",
            resolution_comment="Awaiting review by hostel staff",
        )

        complaints_data.append(new_complaint.to_dict())
        JSONHandler.write_json(self.__complaints_file, complaints_data)

        print("\n[Success] Your complaint has been submitted successfully.")
        print(f"Complaint ID: {new_complaint.get_complaint_id()} (Priority: {new_complaint.get_priority()})")
        print("Our hostel warden/caretaker staff will review it shortly.")
        MenuHelpers.pause()
        return new_complaint

    def get_complaints_by_student(self, registration_number: str) -> List[Complaint]:
        """Get list of complaints filed by a particular student."""
        all_data = JSONHandler.read_json(self.__complaints_file, default_data=[])
        res = []
        for c in all_data:
            if c.get("registration_number", "").strip().upper() == registration_number.strip().upper():
                res.append(Complaint.from_dict(c))
        return res

    def get_latest_complaint_date(self, registration_number: str) -> str:
        """Get date/time of student's latest complaint."""
        student_complaints = self.get_complaints_by_student(registration_number)
        if not student_complaints:
            return "No complaints registered"
        latest = student_complaints[-1]
        return f"{latest.get_complaint_date()} ({latest.get_complaint_time()})"

    def get_all_complaints(self) -> List[Complaint]:
        """Return all complaints in the system."""
        all_data = JSONHandler.read_json(self.__complaints_file, default_data=[])
        return [Complaint.from_dict(c) for c in all_data]

    def display_all_complaints(self) -> None:
        """Display all complaints in a formatted table for staff."""
        complaints = self.get_all_complaints()
        MenuHelpers.display_banner("ALL LODGED COMPLAINTS")
        if not complaints:
            print("No complaints have been lodged yet.")
            MenuHelpers.pause()
            return

        print(f"{'ID':<8} | {'Reg Number':<16} | {'Title':<20} | {'Priority':<8} | {'Status':<12} | {'Staff':<10}")
        print("-" * 84)
        for c in complaints:
            title_trunc = c.get_title()[:18] + ".." if len(c.get_title()) > 18 else c.get_title()
            print(
                f"{c.get_complaint_id():<8} | "
                f"{c.get_registration_number():<16} | "
                f"{title_trunc:<20} | "
                f"{c.get_priority():<8} | "
                f"{c.get_status():<12} | "
                f"{c.get_assigned_staff():<10}"
            )
        print("-" * 84)
        MenuHelpers.pause()

    def search_complaints(self) -> None:
        """Search complaints by Complaint ID or Student Registration Number."""
        MenuHelpers.display_banner("SEARCH COMPLAINTS")
        query = input("Enter Complaint ID or Student Reg Number to search: ").strip()
        if not query:
            print("[Error] Search term cannot be empty.")
            MenuHelpers.pause()
            return

        all_complaints = self.get_all_complaints()
        matches = [
            c for c in all_complaints
            if query.upper() in c.get_complaint_id().upper()
            or query.upper() in c.get_registration_number().upper()
        ]

        if not matches:
            print(f"\nNo complaints matched query '{query}'.")
            MenuHelpers.pause()
            return

        print(f"\nFound {len(matches)} matching complaint(s):\n")
        for idx, c in enumerate(matches, 1):
            print(f"--- Result {idx} ---")
            print(f"Complaint ID   : {c.get_complaint_id()}")
            print(f"Student Reg No : {c.get_registration_number()}")
            print(f"Title          : {c.get_title()}")
            print(f"Description    : {c.get_description()}")
            print(f"Priority       : {c.get_priority()}")
            print(f"Status         : {c.get_status()}")
            print(f"Lodged On      : {c.get_complaint_date()} at {c.get_complaint_time()}")
            print(f"Assigned Staff : {c.get_assigned_staff()}")
            print(f"Resolution Note: {c.get_resolution_comment()}")
            print()

        MenuHelpers.pause()

    def update_complaint_status_workflow(self, staff_id: str) -> bool:
        """Staff workflow to update a complaint's status and add resolution remarks."""
        MenuHelpers.display_banner("UPDATE COMPLAINT STATUS")
        complaints_data = JSONHandler.read_json(self.__complaints_file, default_data=[])
        if not complaints_data:
            print("No complaints available to update.")
            MenuHelpers.pause()
            return False

        # Show pending or all complaints
        print(f"{'No.':<4} | {'ID':<8} | {'Reg Number':<16} | {'Title':<20} | {'Status':<12}")
        print("-" * 70)
        for idx, c in enumerate(complaints_data, 1):
            title = c.get("title", "")
            title_trunc = title[:18] + ".." if len(title) > 18 else title
            print(
                f"{idx:<4} | "
                f"{c.get('complaint_id', ''):<8} | "
                f"{c.get('registration_number', ''):<16} | "
                f"{title_trunc:<20} | "
                f"{c.get('status', ''):<12}"
            )
        print("-" * 70)

        choice = MenuHelpers.get_menu_choice(1, len(complaints_data), "Select complaint to update: ")
        selected_record = complaints_data[choice - 1]

        print(f"\nUpdating Complaint: {selected_record.get('complaint_id')} - {selected_record.get('title')}")
        print("Select New Status:")
        print("1. Pending")
        print("2. In Progress")
        print("3. Resolved")
        status_choice = MenuHelpers.get_menu_choice(1, 3)
        status_map = {1: "Pending", 2: "In Progress", 3: "Resolved"}
        new_status = status_map[status_choice]

        comment = input("Enter resolution / staff progress comments: ").strip()
        if not comment:
            comment = f"Status updated to {new_status} by {staff_id}."

        selected_record["status"] = new_status
        selected_record["assigned_staff"] = staff_id
        selected_record["resolution_comment"] = comment
        selected_record["last_updated"] = get_timestamp()

        JSONHandler.write_json(self.__complaints_file, complaints_data)
        print(f"\n[Success] Complaint {selected_record.get('complaint_id')} updated to '{new_status}'.")
        MenuHelpers.pause()
        return True

    def get_staff_complaints_stats(self, staff_id: str) -> Dict[str, Any]:
        """Compute complaints handled by this staff and last update date."""
        complaints_data = JSONHandler.read_json(self.__complaints_file, default_data=[])
        handled_count = 0
        last_updated_time = "None"

        for c in complaints_data:
            if c.get("assigned_staff", "").strip().upper() == staff_id.strip().upper():
                handled_count += 1
                rec_update = c.get("last_updated") or f"{c.get('complaint_date')} {c.get('complaint_time')}"
                if last_updated_time == "None" or rec_update > last_updated_time:
                    last_updated_time = rec_update

        return {
            "total_handled": handled_count,
            "last_updated": last_updated_time,
        }
