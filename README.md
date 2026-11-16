# LifeLink – Organ Donation Management System

LifeLink is a Django-based web application designed to streamline organ donation management by connecting potential donors with verified hospitals through a secure and organized platform.

## Features

- **Donor Management:** Donor registration, authentication, profile management, and donation applications.
- **Hospital Management:** Hospital registration, account verification, and dedicated hospital dashboards.
- **Donation Management:** Submission, assignment, review, approval, and rejection of donation applications.
- **Appointment Management:** Hospital appointment scheduling and status tracking.
- **Medical Records:** Secure management of donor medical documents.
- **Notifications:** System notifications for important activities.
- **Activity Logging:** Records important system activities for accountability.

## User Roles

- **Donors:** Register, manage profiles, submit donation applications, and view appointments.
- **Hospitals:** Manage assigned applications, review submissions, schedule appointments, and manage donor records.
- **Administrators:** Verify hospital accounts and oversee system operations.

## Technology Stack

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Bootstrap

## Installation

1. Clone the repository:

   ```bash
    git clone https://github.com/harizonelopez/Organ-Donation-App.git
   ```

2. Navigate into the project directory:

   ```bash
    cd Organ-Donation-App
   ```

3. Create and activate a virtual environment:

   ```bash
    python -m venv .env
   ```

   Windows:

   ```bash
    .env\Scripts\activate
   ```

4. Install dependencies:

   ```bash
    pip install -r requirements.txt
   ```

5. Configure the environment variables in `secrets.env`.

6. Apply database migrations:

   ```bash
    python manage.py migrate
   ```

7. Create an administrator account:

   ```bash
    python manage.py createsuperuser
   ```

8. Start the development server:

   ```bash
    python manage.py runserver
   ```

9. Open `http://127.0.0.1:8000` in your browser.

## Security and Privacy

LifeLink uses role-based access control to restrict access to sensitive information. Hospital accounts require administrator verification, and hospitals can only access applications assigned to them.

Medical suitability and final donation decisions must be determined by qualified medical professionals. Registration or application approval does not constitute medical clearance or confirmation of donor eligibility.

## Project Status

LifeLink is under active development.

## License

Project intended for educational and demonstration purposes.