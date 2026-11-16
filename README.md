# LifeLink – Organ Donation Management System

LifeLink is a Django-based web application for organizing organ donation workflows between potential donors and hospitals. It provides role-specific account areas for donors, hospitals, and administrators, with tools for managing applications, appointments, medical documents, and notifications.

> **Important:** LifeLink is an educational and demonstration project. It is not a medical service, a donor registry, or a substitute for professional medical advice. Medical suitability and all donation decisions must be assessed by qualified medical professionals and appropriate authorities.

## Contents

- [Features](#features)
- [User roles](#user-roles)
- [Technology stack](#technology-stack)
- [Getting started](#getting-started)
- [Configuration](#configuration)
- [Typical workflow](#typical-workflow)
- [Security and privacy](#security-and-privacy)
- [Development notes](#development-notes)
- [Project status](#project-status)
- [License](#license)

## Features

- **Donor accounts:** Registration, authentication, profile management, and donation application submission.
- **Hospital accounts:** Registration, administrator verification, and hospital dashboards.
- **Donation applications:** Submission, assignment to hospitals, review, and approval or rejection.
- **Appointments:** Hospital appointment scheduling and status tracking.
- **Medical records:** Management of donor medical documents within the application.
- **Notifications:** Updates about important application and appointment activity.
- **Activity logging:** Records important system activities for accountability.

## User roles

| Role              | Main capabilities                                                                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Donor**         | Create and manage an account, submit donation applications, and view appointments.                                                                     |
| **Hospital**      | Manage assigned applications, review submissions, schedule appointments, and manage donor records. Hospital access requires dministrator verification. |
| **Administrator** | Verify hospital accounts and oversee system operations.                                                                                                |

Access to application information is intended to follow these roles. Hospitals can access applications assigned to them; they cannot browse all applications.

## Technology stack

- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap

## Getting started

### Prerequisites

- Python installed and available from your command line.
- Git, to clone the repository.
- A terminal or command prompt.

Use a Python version supported by the Django version specified in the project's dependencies.

### Installation

1. Clone the repository and enter its directory:

   ```bash
   git clone https://github.com/harizonelopez/Organ-Donation-App.git
   cd Organ-Donation-App
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .env
   ```

3. Activate the environment.

   **Windows (Command Prompt):**

   ```bat
   .env\Scripts\activate
   ```

   **Windows (PowerShell):**

   ```powershell
   .env\Scripts\Activate.ps1
   ```

   **macOS or Linux:**

   ```bash
   source .env/bin/activate
   ```

4. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Configure the required environment variables as described in [Configuration](#configuration).

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Create an administrator account when prompted:

   ```bash
   python manage.py createsuperuser
   ```

8. Start the local development server:

   ```bash
   python manage.py runserver
   ```

9. Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in a browser.

To stop the development server, press `Ctrl+C` in the terminal. To leave the virtual environment, run `deactivate`.

## Configuration

The project setup expects configuration values to be provided through `secrets.env`. Check the project's settings and dependency documentation for the exact variable names and required values; they are not specified here because they depend on the current code configuration.

- Keep secret keys, passwords, and other credentials private.
- Do not commit populated secret files to a public repository.
- Use development-only credentials locally, and use appropriately managed secrets for any deployment.
- If a `secrets.env` template is provided in the repository, use it as the source of truth and replace example values before running the application.

## Typical workflow

1. A donor creates an account, manages their profile, and submits an application.
2. An administrator verifies hospital accounts.
3. An application is assigned to a hospital for review.
4. The hospital reviews its assigned application and may schedule an appointment or update the application status.
5. The donor can follow relevant application and appointment updates through the available account features and notifications.

Exact screens, status names, and available actions depend on the current implementation.

## Security and privacy

LifeLink is designed to use role-based access control for sensitive information. Hospital accounts require administrator verification, and hospitals are limited to applications assigned to them. These design goals do not, by themselves, guarantee that a deployment is secure or compliant with privacy regulations.

Medical documents and donor information are sensitive. Use only appropriate test data in development, protect credentials, and review access controls, file handling, database backups, and deployment settings before handling real personal or medical information. Do not use this educational project to make medical eligibility decisions.

Registration or application approval is not medical clearance and does not confirm donor eligibility. Final suitability and donation decisions belong to qualified medical professionals and relevant authorities.

## Development notes

- Run commands from the directory containing `manage.py`.
- After model changes, create and apply migrations using `python manage.py makemigrations` and `python manage.py migrate`.
- Use Django's development server only for local development; it is not intended for production hosting.
- Check the project settings and installed dependencies for deployment-specific requirements before deploying.

## Project status

LifeLink is under active development. Features, workflows, and configuration may change.

## License

This project is intended for educational and demonstration purposes. No formal license is specified in this README; check the repository for license terms before reuse or distribution.

