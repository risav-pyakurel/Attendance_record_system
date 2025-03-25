#  Attendance Record System

## Overview

The  Attendance Record System is a Django-based application tailored to manage employee attendance efficiently for Bottle. This system includes user-friendly views to manage employee attendance, CSV import for bulk record creation, and email-based login using a custom user model. It incorporates multiple libraries to support custom forms, multi-select fields, and Nepali date functionality.

## Features

- **Employee Attendance Management**: Add, update, delete, and list attendance records.
- **Custom User Authentication**: Login with email as the primary identifier (no username required).
- **Attendance Record CRUD Operations**: Use the `AttendanceRecordListView`, `AttendanceRecordCreateView`, `AttendanceRecordUpdateView`, and `AttendanceRecordDeleteView` to manage records.
- **CSV Import**: Bulk import attendance data from a CSV file, creating employee entries and attendance records.
- **Nepali Date Support**: Integration of Nepali date fields using `django-nepali-datetime-field` and `nepali-datetime`.
- **Base Model Inheritance**: Common fields (created_at, updated_at, is_archived) are inherited from `BaseModel` in the `common` app.
- **Automatic Work Hour Calculation**: Calculates work hours based on check-in and check-out times.
- **JavaScript Confirmation for Deletion**: A JavaScript confirmation dialog in the employee list view for delete actions.

## Technologies and Dependencies

- **Backend**: Django 5.1.2
- **Database**: PostgreSQL (requires `psycopg2`)
- **Frontend**: Django Templates, JavaScript (for confirmation dialog)
- **Utilities**:
  - `asgiref==3.8.1`
  - `django-crispy-forms==2.3`
  - `crispy-bootstrap5==2024.10`
  - `django-environ==0.11.2`
  - `django-multiselectfield==0.1.13`
  - `django-nepali-datetime-field==0.7.1`
  - `nepali-datetime==1.0.8.3`
  - `pillow==11.0.0` (for image handling if needed)
  - `requests==2.32.3`
  - `sqlparse==0.5.1`
  - `typing_extensions==4.12.2`

For a full list of dependencies, refer to `requirements.txt`.

## Getting Started

### Prerequisites

- Python 3.x
- PostgreSQL

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Bottle-Techology/attendance_record_system.git
   cd attendance_record_system

2. **Set up the virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows use `venv\Scripts\activate`

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt

4. **Set up environment variables**:

   Copy `.env.example` to `.env` and update the database settings and other configurations as needed.

5. **Run Migrations:**:

   ```bash
   python manage.py migrate

7. **Run the development server**:

   ```bash
   python manage.py runserver

## Note

**Add these two files in the project**:


 ```bash
 https://bottleit-my.sharepoint.com/:f:/g/personal/risav_bottle_com_np/EkFkI0Lm_ZZIgljLBa-pW4MB_v_UR-YsVF3VFcZnGnfKbQ?e=DecrPS

 ## Where keep src file in templates/dashboard

