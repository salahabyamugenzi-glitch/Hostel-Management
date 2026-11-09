

import unittest
import sys
import os
from typing import List

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from models.user import User
from models.student import Student
from models.staff import Staff
from models.hostel import Hostel
from models.room import Room
from models.bed import Bed
from models.payment import Payment
from models.complaint import Complaint
from utilities.id_generator import IDGenerator
from utilities.validators import Validators
from utilities.date_time_helper import get_current_date, get_current_time, get_timestamp
from utilities.password_helper import hash_password, verify_password
from services.hostel_service import HostelService


class TestHostelManagementSystemOOP(unittest.TestCase):
    """Test OOP rules and system functionality."""

    def test_encapsulation_and_getters_setters(self):
        """Verify strict encapsulation: private fields and functional getters/setters."""
        user = User("John", "Doe", "Male", "0771234567", "Kampala", "secret123")

        # Verify attributes are private (mangled in Python as _User__first_name)
        self.assertFalse(hasattr(user, "first_name"))
        self.assertTrue(hasattr(user, "_User__first_name"))
        self.assertEqual(user.get_first_name(), "John")
        self.assertEqual(user.get_full_name(), "John Doe")

        user.set_first_name("Jonathan")
        self.assertEqual(user.get_first_name(), "Jonathan")
        self.assertEqual(user.get_full_name(), "Jonathan Doe")

    def test_inheritance(self):
        """Verify Student and Staff inherit properly from User."""
        student = Student(
            first_name="Alice",
            last_name="Nambi",
            gender="Female",
            contact="0709876543",
            address="Entebbe",
            password="passAlice123",
            registration_number="202-123456-001",
            course="Computer Science",
            next_of_kin="Grace Nambi",
            next_of_kin_contact="0701112233",
            hostel_id="HST-F01",
            room_number="C101",
            bed_number="Bed 1",
            account_status="Active",
            registration_date=get_current_date(),
            registration_time=get_current_time(),
        )

        self.assertIsInstance(student, User)
        self.assertEqual(student.get_full_name(), "Alice Nambi")
        self.assertEqual(student.get_registration_number(), "202-123456-001")
        self.assertTrue(hasattr(student, "_Student__registration_number"))

        staff = Staff(
            first_name="Robert",
            last_name="Kato",
            gender="Male",
            contact="0781122334",
            address="Mukono",
            password="staffPass456",
            staff_id="STF001",
            role="Hostel Warden",
            department="Hostel Administration",
            account_status="Active",
            registration_date=get_current_date(),
            registration_time=get_current_time(),
        )

        self.assertIsInstance(staff, User)
        self.assertEqual(staff.get_full_name(), "Robert Kato")
        self.assertEqual(staff.get_staff_id(), "STF001")
        self.assertTrue(hasattr(staff, "_Staff__staff_id"))

    def test_polymorphic_profile_summaries(self):
        """Verify User references dispatch to each subclass implementation."""
        student = Student(
            first_name="Alice",
            last_name="Nambi",
            registration_number="202-123456-001",
            course="Computer Science",
            hostel_id="HST-F01",
            room_number="C101",
            bed_number="Bed 1",
        )
        staff = Staff(
            first_name="Robert",
            last_name="Kato",
            staff_id="STF001",
            role="Hostel Warden",
            department="Hostel Administration",
        )

        users: List[User] = [student, staff]
        summaries = [user.get_profile_summary() for user in users]

        self.assertIn("Student: Alice Nambi", summaries[0])
        self.assertIn("Registration Number: 202-123456-001", summaries[0])
        self.assertIn("Staff: Robert Kato", summaries[1])
        self.assertIn("Role: Hostel Warden", summaries[1])

    def test_id_generator_formats(self):
        """Verify unique ID generation formats."""
        reg_no = IDGenerator.generate_student_registration_number([])
        parts = reg_no.split("-")
        self.assertEqual(len(parts), 3)
        self.assertEqual(len(parts[0]), 3)
        self.assertEqual(len(parts[1]), 6)
        self.assertEqual(len(parts[2]), 3)

        staff_id1 = IDGenerator.generate_staff_id([])
        self.assertEqual(staff_id1, "STF001")
        staff_id2 = IDGenerator.generate_staff_id(["STF001", "STF002"])
        self.assertEqual(staff_id2, "STF003")

        pay_id = IDGenerator.generate_payment_id([])
        self.assertTrue(pay_id.startswith("PAY"))

        cmp_id = IDGenerator.generate_complaint_id([])
        self.assertTrue(cmp_id.startswith("CMP"))

        txn_ref = IDGenerator.generate_transaction_reference()
        self.assertTrue(txn_ref.startswith("TXN-"))

    def test_validators(self):
        """Verify input validation rules."""
        # Password
        v, _ = Validators.validate_password("12345")
        self.assertFalse(v)
        v, _ = Validators.validate_password("123456")
        self.assertTrue(v)

        # Contact
        v, _ = Validators.validate_contact("0771234567")
        self.assertTrue(v)
        v, _ = Validators.validate_contact("abc")
        self.assertFalse(v)

        # Amount (minimum UGX 150,000)
        v, msg, amt = Validators.validate_amount("100000", min_amount=150000.0)
        self.assertFalse(v)
        v, msg, amt = Validators.validate_amount("150000", min_amount=150000.0)
        self.assertTrue(v)
        self.assertEqual(amt, 150000.0)

        v, _, _ = Validators.validate_amount("nan", min_amount=150000.0)
        self.assertFalse(v)
        v, _, _ = Validators.validate_amount("inf", min_amount=150000.0)
        self.assertFalse(v)

    def test_password_hashing_and_legacy_verification(self):
        hashed = hash_password("secret123")
        self.assertNotEqual(hashed, "secret123")
        self.assertTrue(verify_password("secret123", hashed))
        self.assertFalse(verify_password("wrong", hashed))
        self.assertTrue(verify_password("password123", "password123"))

    def test_hostel_service_gender_filtering_and_allocation(self):
        """Verify gender filtering and bed allocation logic."""
        service = HostelService()
        male_hostels = service.get_hostels_by_gender("Male")
        female_hostels = service.get_hostels_by_gender("Female")

        self.assertTrue(any(h.get_hostel_name() == "Hostel A" for h in male_hostels))
        self.assertTrue(any(h.get_hostel_name() == "Hostel B" for h in male_hostels))
        self.assertTrue(any(h.get_hostel_name() == "Hostel C" for h in female_hostels))
        self.assertTrue(any(h.get_hostel_name() == "Hostel D" for h in female_hostels))


if __name__ == "__main__":
    unittest.main()
