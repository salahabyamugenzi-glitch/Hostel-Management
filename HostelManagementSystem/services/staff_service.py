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
        print(staff.get_profile_summary())
        print(f"Contact Number: {staff.get_contact()}")
        print(f"Address: {staff.get_address()}")
        print(f"Registered On: {staff.get_registration_date()} at {staff.get_registration_time()}")
        print("=" * 50)
        MenuHelpers.pause()
