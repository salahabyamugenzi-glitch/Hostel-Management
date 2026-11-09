"""
Staff Dashboard.
Interactive dashboard for logged-in staff members.
Requirements:
- Menu items:
  1. View Profile
  2. View All Complaints
  3. Search Complaint (by Complaint ID or Reg Number)
  4. Update Complaint Status (Pending / In Progress / Resolved)
  5. Logout
- Displays registration date, total complaints handled, and most recent update date.
"""

from models.staff import Staff
from services.staff_service import StaffService
from services.complaint_service import ComplaintService
from utilities.menu_helpers import MenuHelpers


class StaffDashboard:
    """Dashboard controller for authenticated staff sessions."""

    def __init__(self, staff: Staff):
        self.__staff = staff
        self.__staff_service = StaffService()
        self.__complaint_service = ComplaintService()

    def run(self) -> None:
        """Run the main staff dashboard loop."""
        while True:
            # Fetch dynamic staff stats
            stats = self.__complaint_service.get_staff_complaints_stats(self.__staff.get_staff_id())
            reg_date = f"{self.__staff.get_registration_date()} {self.__staff.get_registration_time()}"

            MenuHelpers.display_banner("STAFF DASHBOARD")
            print(f" Staff: {self.__staff.get_full_name()} | ID: {self.__staff.get_staff_id()} | Role: {self.__staff.get_role()}")
            print(f" Department: {self.__staff.get_department()}")
            print("-" * 50)
            print(f" • Registration Date : {reg_date}")
            print(f" • Handled Complaints: {stats['total_handled']}")
            print(f" • Most Recent Update: {stats['last_updated']}")
            print("-" * 50)
            print("1. View Profile")
            print("2. View All Complaints")
            print("3. Search Complaint (by Complaint ID or Reg Number)")
            print("4. Update Complaint Status (Pending / In Progress / Resolved)")
            print("5. Logout")
            print("-" * 50)

            choice = MenuHelpers.get_menu_choice(1, 5)

            if choice == 1:
                self.__staff_service.view_profile(self.__staff)
            elif choice == 2:
                self.__complaint_service.display_all_complaints()
            elif choice == 3:
                self.__complaint_service.search_complaints()
            elif choice == 4:
                self.__complaint_service.update_complaint_status_workflow(self.__staff.get_staff_id())
            elif choice == 5:
                print(f"\nGoodbye, {self.__staff.get_first_name()}! Logged out successfully.")
                MenuHelpers.pause()
                break
