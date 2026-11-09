"""
Payment Service.
Handles student fee payments, validations, payment history queries,
and JSON persistence.
Rules:
- Minimum amount: UGX 150,000
- Semesters: Semester I / Semester II
- Academic years: e.g. 2026/2027, 2027/2028
- Methods: Credit card, MTN Mobile Money, Airtel Mobile Money (no cash)
- Auto-capture date & time.
"""

import os
from typing import List, Dict, Any, Optional
from models.payment import Payment
from utilities.id_generator import IDGenerator
from utilities.validators import Validators
from utilities.date_time_helper import get_current_date, get_current_time
from utilities.json_handler import JSONHandler
from utilities.menu_helpers import MenuHelpers


class PaymentService:
    """Service to process payments and inspect transaction logs."""

    def __init__(self, base_data_dir: Optional[str] = None):
        if base_data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.__data_dir = os.path.join(base_dir, "data")
        else:
            self.__data_dir = base_data_dir

        self.__payments_file = os.path.join(self.__data_dir, "payments.json")
        JSONHandler.ensure_file_exists(self.__payments_file, [])

    def process_payment(self, registration_number: str) -> Optional[Payment]:
        """
        Interactive payment flow for a student.
        Enforces amount limits, allowed payment methods, academic semester, and auto dates.
        """
        MenuHelpers.display_banner("HOSTEL FEE PAYMENT")
        print(f"Payer Registration Number: {registration_number}")
        print("Note: Minimum payment amount is UGX 150,000. Cash is not accepted.\n")

        # 1. Amount Validation
        while True:
            amt_str = input("Enter Amount in UGX (e.g. 250000): ").strip()
            valid, msg, amount = Validators.validate_amount(amt_str, min_amount=150000.0)
            if valid:
                break
            print(f"[Error] {msg}")

        # 2. Semester
        print("\nSelect Academic Semester:")
        print("1. Semester I")
        print("2. Semester II")
        sem_choice = MenuHelpers.get_menu_choice(1, 2)
        semester = "Semester I" if sem_choice == 1 else "Semester II"

        # 3. Academic Year
        years = ["2026/2027", "2027/2028", "2028/2029"]
        print("\nSelect Academic Year:")
        for idx, yr in enumerate(years, 1):
            print(f"{idx}. {yr}")
        yr_choice = MenuHelpers.get_menu_choice(1, len(years))
        academic_year = years[yr_choice - 1]

        # 4. Payment Method (strictly no cash!)
        methods = ["MTN Mobile Money", "Airtel Mobile Money", "Credit card"]
        print("\nSelect Payment Method (Strictly Electronic - No Cash):")
        for idx, m in enumerate(methods, 1):
            print(f"{idx}. {m}")
        m_choice = MenuHelpers.get_menu_choice(1, len(methods))
        payment_method = methods[m_choice - 1]

        # Account / Card confirmation prompt based on method
        if "Mobile Money" in payment_method:
            while True:
                phone = input(f"Enter {payment_method} Phone Number: ").strip()
                valid, msg = Validators.validate_contact(phone)
                if valid:
                    break
                print(f"[Error] {msg}")
        else:
            while True:
                card_last4 = input("Enter last 4 digits of Credit Card: ").strip()
                if len(card_last4) == 4 and card_last4.isdigit():
                    break
                print("[Error] Please enter exactly 4 numerical digits.")

        # 5. Auto generate ID, Transaction Ref, Date, and Time
        existing_payments = JSONHandler.read_json(self.__payments_file, default_data=[])
        existing_ids = [p.get("payment_id", "") for p in existing_payments]
        payment_id = IDGenerator.generate_payment_id(existing_ids)
        txn_ref = IDGenerator.generate_transaction_reference()
        pay_date = get_current_date()
        pay_time = get_current_time()

        new_payment = Payment(
            payment_id=payment_id,
            registration_number=registration_number,
            amount=amount,
            payment_method=payment_method,
            semester=semester,
            academic_year=academic_year,
            payment_date=pay_date,
            payment_time=pay_time,
            status="Completed",
            transaction_reference=txn_ref,
        )

        existing_payments.append(new_payment.to_dict())
        JSONHandler.write_json(self.__payments_file, existing_payments)

        # Receipt
        MenuHelpers.display_banner("OFFICIAL PAYMENT RECEIPT")
        print(f" Receipt / Payment ID : {new_payment.get_payment_id()}")
        print(f" Transaction Ref      : {new_payment.get_transaction_reference()}")
        print(f" Registration Number  : {new_payment.get_registration_number()}")
        print(f" Amount Paid          : UGX {new_payment.get_amount():,.2f}")
        print(f" Payment Method       : {new_payment.get_payment_method()}")
        print(f" Semester / Year      : {new_payment.get_semester()} ({new_payment.get_academic_year()})")
        print(f" Status               : {new_payment.get_status()}")
        print(f" Timestamp            : {new_payment.get_payment_date()} {new_payment.get_payment_time()}")
        print("=" * 50)
        MenuHelpers.pause()
        return new_payment

    def get_payments_by_student(self, registration_number: str) -> List[Payment]:
        """Retrieve all payment records belonging to a student."""
        all_payments = JSONHandler.read_json(self.__payments_file, default_data=[])
        student_payments: List[Payment] = []
        for p in all_payments:
            if p.get("registration_number", "").strip().upper() == registration_number.strip().upper():
                student_payments.append(Payment.from_dict(p))
        return student_payments

    def get_last_payment_date(self, registration_number: str) -> str:
        """Return the date of the most recent payment, or 'No payments made'."""
        payments = self.get_payments_by_student(registration_number)
        if not payments:
            return "No payments made yet"
        # Since payments are appended chronologically
        last = payments[-1]
        return f"{last.get_payment_date()} ({last.get_payment_time()})"

    def display_payment_history(self, registration_number: str) -> None:
        """Display formatted table of all payments made by student."""
        payments = self.get_payments_by_student(registration_number)
        MenuHelpers.display_banner("PAYMENT HISTORY")
        if not payments:
            print("No transaction records found for your account.")
            MenuHelpers.pause()
            return

        total_paid = sum(p.get_amount() for p in payments)
        print(f"Total Transactions: {len(payments)} | Total Paid: UGX {total_paid:,.2f}\n")
        print(f"{'Payment ID':<10} | {'Txn Ref':<14} | {'Amount (UGX)':<14} | {'Semester':<12} | {'Method':<18} | {'Date':<10}")
        print("-" * 88)
        for p in payments:
            print(
                f"{p.get_payment_id():<10} | "
                f"{p.get_transaction_reference():<14} | "
                f"{p.get_amount():>12,.0f}   | "
                f"{p.get_semester():<12} | "
                f"{p.get_payment_method():<18} | "
                f"{p.get_payment_date():<10}"
            )
        print("-" * 88)
        MenuHelpers.pause()
