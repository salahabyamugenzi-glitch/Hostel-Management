"""
Staff Service.
Handles staff profile display and administrative records lookup.
"""

from typing import Optional
from models.staff import Staff
from utilities.menu_helpers import MenuHelpers


class StaffService:
    """Service to handle staff profile inquiries."""

    def view_profile(self, staff: Staff) -> None:
        """Display detailed staff profile."""
        MenuHelpers.display_banner("STAFF PROFILE")
        print(f" Staff ID       : {staff.get_staff_id()}")
        print(f" Full Name      : {staff.get_full_name()}")
        print(f" Gender         : {staff.get_gender()}")
        print(f" Role           : {staff.get_role()}")
        print(f" Department     : {staff.get_department()}")
        print(f" Contact Number : {staff.get_contact()}")
        print(f" Address        : {staff.get_address()}")
        print(f" Account Status : {staff.get_account_status()}")
        print(f" Registered On  : {staff.get_registration_date()} at {staff.get_registration_time()}")
        print("=" * 50)
        MenuHelpers.pause()
