# Hostel Management System (Python OOP)

A complete, fully functional, production-ready console-based Hostel Management System implemented in **pure Python** using the Python standard library.

This application strictly adheres to the requested Object-Oriented Programming (OOP) constraints:
1. **Encapsulation**: Every single class attribute is strictly private (`__attribute`). Access and modification occur exclusively through explicit public getter and setter methods.
2. **Inheritance**: `Student` and `Staff` inherit from the foundational `User` parent class via `super().__init__()`.
3. **Strict Constraints Compliance**:
   - **Polymorphism**: `Student` and `Staff` override `get_profile_summary()`, allowing the same `User` reference to produce role-specific profile details through dynamic dispatch.
   - **Abstraction**: `User` is an abstract base class that defines the common user contract, while `Student` and `Staff` provide concrete implementations.
   - **NO Databases**: Persistent storage is handled entirely through standard JSON files (`data/*.json`).
   - **NO External Packages**: 100% powered by the Python Standard Library (`json`, `os`, `sys`, `datetime`, `random`, `re`).

---

## Project Structure

```text
HostelManagementSystem/
├── main.py                         # Single executable entry point for the entire application
├── test_system.py                  # Comprehensive automated unit test suite
├── models/                         # Domain models with strict encapsulation
│   ├── user.py                     # Parent User class (first_name, last_name, gender, etc.)
│   ├── student.py                  # Student class (inherits User, reg_no, room, bed, etc.)
│   ├── staff.py                    # Staff class (inherits User, staff_id, role, dept, etc.)
│   ├── hostel.py                   # Hostel model (hostel_id, name, gender_category, etc.)
│   ├── room.py                     # Room model (room_number, capacity, room_status, etc.)
│   ├── bed.py                      # Bed model (bed_number, status: Occupied/Available)
│   ├── payment.py                  # Payment model (amount, method, txn_ref, dates, etc.)
│   └── complaint.py                # Complaint model (title, description, priority, status)
├── services/                       # Business logic services
│   ├── registration_service.py     # Student & Staff interactive registration & allocation
│   ├── login_service.py            # Authentication workflows with submenus
│   ├── hostel_service.py           # Gender filtering, room/bed lookup, allocation & release
│   ├── payment_service.py          # Fee processing (min UGX 150k, mobile money/card)
│   ├── complaint_service.py        # Filing, tracking, searching, and updating issues
│   ├── password_reset_service.py   # Identity verification (ID + contact) & password updates
│   ├── student_service.py          # Student profile view and account deletion
│   └── staff_service.py            # Staff profile view and records
├── dashboards/                     # Terminal interactive dashboards
│   ├── student_dashboard.py        # Profile, Payment, Payment History, Complaint, Delete
│   └── staff_dashboard.py          # Profile, View Complaints, Search, Update Status
├── utilities/                      # Shared helper utilities
│   ├── json_handler.py             # File I/O, auto-initialization, error handling
│   ├── id_generator.py             # Unique ID generation (XXX-XXXXXX-XXX, STF001, etc.)
│   ├── validators.py               # Phone, password, amount, and name validators
│   ├── menu_helpers.py             # Console menus, headers, prompts, input sanitization
│   ├── password_helper.py          # Password hashing and verification
│   └── date_time_helper.py         # Standardized date, time, and timestamp captures
├── data/                           # Persistent JSON database files
│   ├── hostels.json                # Pre-defined hostels, rooms, and bed statuses
│   ├── students.json               # Registered student accounts
│   ├── staff.json                  # Registered staff accounts (includes sample STF001)
│   ├── payments.json               # Transaction logs and receipts
│   └── complaints.json             # Lodged complaints and resolution remarks
└── README.md                       # Comprehensive system documentation
```

---

## OOP Architecture & Class Hierarchy

```
User (Parent Class)
├── Student (Child Class)
└── Staff (Child Class)
```

### 1. `User` (Abstract Parent Class)
- **Private Attributes**:
  - `__first_name`, `__last_name`, `__gender`, `__contact`, `__address`, `__password`
- **Public Methods**:
  - Getters: `get_first_name()`, `get_last_name()`, `get_gender()`, `get_contact()`, `get_address()`, `get_password()`, `get_full_name()`
  - Abstract polymorphic operation: `get_profile_summary()`
  - `User` cannot be instantiated directly; concrete subclasses must implement `get_profile_summary()`.
  - Setters: `set_first_name()`, `set_last_name()`, `set_gender()`, `set_contact()`, `set_address()`, `set_password()`

### 2. `Student` (Child Class inherits `User`)
- **Private Attributes**:
  - `__registration_number`, `__course`, `__next_of_kin`, `__next_of_kin_contact`, `__hostel_id`, `__room_number`, `__bed_number`, `__account_status`, `__registration_date`, `__registration_time`
- **Constructor**:
  - Invokes `super().__init__(first_name, last_name, gender, contact, address, password)`
- **Public Methods**:
  - Getters and setters for all student-specific fields.
  - Overrides `get_profile_summary()` with registration, course, hostel, room, bed, and account details.

### 3. `Staff` (Child Class inherits `User`)
- **Private Attributes**:
  - `__staff_id`, `__role`, `__department`, `__account_status`, `__registration_date`, `__registration_time`
- **Constructor**:
  - Invokes `super().__init__(first_name, last_name, gender, contact, address, password)`
- **Public Methods**:
  - Getters and setters for all staff-specific fields.
  - Overrides `get_profile_summary()` with staff ID, role, department, and account details.

### Polymorphism in profile display
The profile services call `get_profile_summary()` on a concrete user object without branching on its type. Python dispatches the call to the appropriate implementation: students receive student-specific information, while staff receive staff-specific information.

### 4. Supporting Models
- **`Hostel`**: `__hostel_id`, `__hostel_name`, `__gender_category`, `__location`, `__total_rooms`, `__warden_id`, `__status`
- **`Room`**: `__room_number`, `__hostel_id`, `__capacity`, `__occupied_beds`, `__room_status` ("Filled" / "Empty" / "Available"), `__available_beds`
- **`Bed`**: `__bed_number`, `__room_number`, `__status` ("Occupied" / "Available")
- **`Payment`**: `__payment_id`, `__registration_number`, `__amount`, `__payment_method`, `__semester`, `__academic_year`, `__payment_date`, `__payment_time`, `__status`, `__transaction_reference`
- **`Complaint`**: `__complaint_id`, `__registration_number`, `__title`, `__description`, `__complaint_date`, `__complaint_time`, `__status` ("Pending" / "In Progress" / "Resolved"), `__priority`, `__assigned_staff`, `__resolution_comment`

---

## Key System Features & Rules

### Pre-defined Hostels
- **Male Hostels**:
  - Hostel A (`HST-M01`): North Campus - Block A (Rooms A101, A102, A201, A202)
  - Hostel B (`HST-M02`): North Campus - Block B (Rooms B101, B102, B201, B202)
- **Female Hostels**:
  - Hostel C (`HST-F01`): South Campus - Block C (Rooms C101, C102, C201, C202)
  - Hostel D (`HST-F02`): South Campus - Block D (Rooms D101, D102, D201, D202)

### Automated ID Generation
- **Student Registration Number**: Format `XXX-XXXXXX-XXX` (e.g. `202-123456-001`), guaranteed unique against all existing records.
- **Staff ID**: `STF001`, `STF002`, `STF003`, etc.
- **Payment ID**: `PAY001`, `PAY002`, ...
- **Complaint ID**: `CMP001`, `CMP002`, ...
- **Transaction Reference**: `TXN-XXXXXXXX`

### Fee Payment Rules
- **Minimum Amount**: UGX 150,000 (strictly enforced by validator).
- **Accepted Methods**: MTN Mobile Money, Airtel Mobile Money, Credit card (**Cash is prohibited**).
- **Semesters**: Semester I, Semester II.
- **Academic Years**: 2026/2027, 2027/2028, 2028/2029.
- **Timestamps**: Automatically captured via `date_time_helper.py`.

### Bed Allocation & Deallocation
1. During student registration, hostels are strictly filtered by student's gender.
2. The student selects an available hostel, selects a room with available beds, and selects a free bed.
3. The selected bed is flagged as `Occupied` and the room's occupancy counts and status (`Filled` / `Available` / `Empty`) are automatically updated.
4. If a student chooses **Delete Account** in their dashboard, they confirm password and intent; the allocated bed is immediately freed in `hostels.json`, the room capacity recalculated, and the student's record deleted from `students.json`.

---

## How to Run the Application

### 1. Requirements
- Python 3.8+ (No `pip install` required! Pure Python Standard Library only).

### 2. Execution
Navigate to the directory and run:
```bash
python3 main.py
```

### 3. Run Automated Tests
To run the automated OOP test suite verifying encapsulation, inheritance, validations, and ID formats:
```bash
python3 test_system.py
```

---

## Seed Staff Credentials for Testing
A default staff account is pre-configured in `data/staff.json`:
- **Staff ID**: `STF001`
- **Password**: `password123`
- **Role**: Hostel Warden (Robert Kato)
- **Department**: Hostel Administration
