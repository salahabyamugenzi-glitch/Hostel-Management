"""
Student Dashboard.
Interactive dashboard for logged-in students.
Requirements:
- Menu items:
  1. View Profile
  2. Make Payment
  3. View Payment History
  4. Raise Complaint
  5. Delete Account
  6. Logout
- Displays account creation date, last payment date, and latest complaint date.
"""

from models.student import Student
from services.student_service import StudentService
from services.payment_service import PaymentService
from services.complaint_service import ComplaintService
from utilities.menu_helpers import MenuHelpers


class StudentDashboard:
    """Dashboard controller for authenticated student sessions."""

    def __init__(self, student: Student):
        self.__student = student
        self.__student_service = StudentService()
        self.__payment_service = PaymentService()
        self.__complaint_service = ComplaintService()

    def run(self) -> None:
        """Run the main student dashboard loop."""
        while True:
            # Fetch dynamic dashboard metrics
            reg_date = f"{self.__student.get_registration_date()} {self.__student.get_registration_time()}"
            last_payment = self.__payment_service.get_last_payment_date(self.__student.get_registration_number())
            latest_complaint = self.__complaint_service.get_latest_complaint_date(self.__student.get_registration_number())

            MenuHelpers.display_banner("STUDENT DASHBOARD")
            print(f" Welcome, {self.__student.get_full_name()} | Reg No: {self.__student.get_registration_number()}")
            print(f" Room: {self.__student.get_room_number()} ({self.__student.get_bed_number()}) | Hostel: {self.__student.get_hostel_id()}")
            print("-" * 50)
            print(f" • Account Created  : {reg_date}")
            print(f" • Last Payment     : {last_payment}")
            print(f" • Latest Complaint : {latest_complaint}")
            print("-" * 50)
            print("1. View Profile")
            print("2. Make Payment")
            print("3. View Payment History")
            print("4. Raise Complaint")
            print("5. Delete Account")
            print("6. Logout")
            print("-" * 50)

            choice = MenuHelpers.get_menu_choice(1, 6)

            if choice == 1:
                self.__student_service.view_profile(self.__student)
            elif choice == 2:
                self.__payment_service.process_payment(self.__student.get_registration_number())
            elif choice == 3:
                self.__payment_service.display_payment_history(self.__student.get_registration_number())
            elif choice == 4:
                self.__complaint_service.raise_complaint(self.__student.get_registration_number())
            elif choice == 5:
                deleted = self.__student_service.delete_account(self.__student)
                if deleted:
                    print("Exiting to Main Menu...")
                    break
            elif choice == 6:
                print(f"\nGoodbye, {self.__student.get_first_name()}! Logged out successfully.")
                MenuHelpers.pause()
                break
