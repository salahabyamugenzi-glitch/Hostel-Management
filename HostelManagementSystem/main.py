import sys
import os

# Add the project root to sys.path to allow clean relative package imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from services.registration_service import RegistrationService
from services.login_service import LoginService
from dashboards.student_dashboard import StudentDashboard
from dashboards.staff_dashboard import StaffDashboard
from utilities.menu_helpers import MenuHelpers


class HostelApp:
    
    #Main application controller managing top-level menus and navigation.
    

    def __init__(self):
        # Initialise services
        self.__registration_service = RegistrationService()
        self.__login_service = LoginService()

    def run(self) -> None:
        # Main application lifecycle loop.
        while True:
            try:
                # Top-level prompt menu required by specifications:
                # =================================
                # HOSTEL MANAGEMENT SYSTEM
                # 1. Register
                # 2. Login
                # 3. Exit
                print()
                print("=================================")
                print("HOSTEL MANAGEMENT SYSTEM")
                print("1. Register")
                print("2. Login")
                print("3. Exit")
                print("=================================")

                choice = MenuHelpers.get_menu_choice(1, 3)

                if choice == 1:
                    self.__handle_register_menu()
                elif choice == 2:
                    self.__handle_login_menu()
                elif choice == 3:
                    print("\nThank you for using the Hostel Management System. Goodbye!")
                    sys.exit(0)

            except KeyboardInterrupt:
                print("\n\nOperation interrupted by user. Returning to main menu...")
            except Exception as e:
                print(f"\n[System Error] An unexpected error occurred: {e}")
                MenuHelpers.pause()

    def __handle_register_menu(self) -> None:
        """
        Handle the Register Sub-Menu:
        1. Student Registration
        2. Staff Registration
        3. Back
        """
        while True:
            MenuHelpers.display_menu(
                "REGISTER MENU",
                [
                    "Student Registration",
                    "Staff Registration",
                    "Back",
                ],
                width=40
            )
            choice = MenuHelpers.get_menu_choice(1, 3)

            if choice == 1:
                student = self.__registration_service.register_student()
                if student:
                    # After successful registration, offer immediate dashboard entry
                    print("\nWould you like to enter your Student Dashboard now? (y/n): ", end="")
                    ans = input().strip().lower()
                    if ans == "y":
                        dashboard = StudentDashboard(student)
                        dashboard.run()
                return

            elif choice == 2:
                staff = self.__registration_service.register_staff()
                if staff:
                    print("\nWould you like to enter your Staff Dashboard now? (y/n): ", end="")
                    ans = input().strip().lower()
                    if ans == "y":
                        dashboard = StaffDashboard(staff)
                        dashboard.run()
                return

            elif choice == 3:
                return

    def __handle_login_menu(self) -> None:
        """
        Handle the Login Sub-Menu:
        1. Student Login
        2. Staff Login
        3. Back
        """
        while True:
            MenuHelpers.display_menu(
                "LOGIN MENU",
                [
                    "Student Login",
                    "Staff Login",
                    "Back",
                ],
                width=40
            )
            choice = MenuHelpers.get_menu_choice(1, 3)

            if choice == 1:
                student = self.__login_service.handle_student_login_flow()
                if student:
                    dashboard = StudentDashboard(student)
                    dashboard.run()
                return

            elif choice == 2:
                staff = self.__login_service.handle_staff_login_flow()
                if staff:
                    dashboard = StaffDashboard(staff)
                    dashboard.run()
                return

            elif choice == 3:
                return


def main():
    """Application entry point."""
    app = HostelApp()
    app.run()


if __name__ == "__main__":
    main()
