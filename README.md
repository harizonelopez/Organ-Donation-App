# LifeLink — Organ Donation Management System

LifeLink is a Django web application designed to demonstrate how organ-donation workflows can connect donors, hospitals, and administrators. It provides role-based dashboards for application review, appointment scheduling, medical document management, notifications, and system activity tracking.

> [!IMPORTANT]
> LifeLink is an educational and demonstration project. It is **not** a transplant registry, clinical system, medical service, or source of medical advice. Only qualified healthcare professionals and authorized organizations can determine medical suitability, eligibility, compatibility, and donation decisions.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [User Roles](#user-roles)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Application Workflow](#application-workflow)
- [Development Commands](#development-commands)
- [Testing](#testing)
- [Security and Privacy](#security-and-privacy)
- [Project Status](#project-status)
- [Contributing](#contributing)
- [License](#license)

## Overview

LifeLink organizes the administrative process around a donation application. Donors submit and monitor their applications, hospitals review only applications assigned to them, and administrators oversee accounts and system activity.

The project is intended for local development, demonstrations, learning, and further extension. Its interfaces, statuses, and policies may change as the application evolves.

## Key Features

### Donor Portal
- Register and authenticate using donor credentials.
- Create and maintain a user profile.
- Submit donation applications.
- View application status and assigned-hospital activity.
- Review appointments and system notifications.
- Upload and manage relevant medical documents where enabled.

### Hospital Portal
- Register a hospital account for administrator review.
- Access a hospital-specific dashboard after verification.
- View applications assigned to the hospital.
- Review applicant information and uploaded documents.
- Schedule appointments and update appointment statuses.
- Update review or application statuses as permitted by the workflow.

### Administrator Portal
- Verify or reject hospital registrations.
- Monitor system users and hospital accounts.
- Review application assignments and important activity.
- Access Django's built-in administration interface when enabled.

### Shared Application Features
- Role-based access control.
- Account authentication and session management.
- Application and appointment status tracking.
- Notification support.
- Activity or audit logging.
- Responsive HTML interfaces styled with CSS and Bootstrap.
- SQLite database support for local development.

## User Roles

| Role | Access and responsibilities |
| --- | --- |
| **Donor** | Creates an account, maintains a profile, submits applications, and tracks appointments and notifications. |
| **Hospital** | Reviews assigned applications, manages supported appointment and record workflows, and requires administrator verification. |
| **Administrator** | Verifies hospitals and oversees accounts and operational activity. Has elevated permissions within the system. |

Data access is intended to follow role and assignment boundaries. A hospital should not treat the portal as a general directory and should only access applications assigned to it.

## Technology Stack

| Area | Technology |
| --- | --- |
| Backend | Python and Django |
| Database | SQLite for development |
| Templates | Django template engine with HTML5 |
| Styling | CSS3 and Bootstrap |
| Client-side behavior | JavaScript |
| Environment | Python virtual environment |

*Exact framework and package versions should be taken from `requirements.txt` and Django settings in the repo.*

## Getting Started

### Prerequisites

- Git
- Python 3.12
- `pip`
- A supported Django version installed from `requirements.txt`

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/harizonelopez/Organ-Donation-App.git
   cd Organ-Donation-App
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .env
   ```

3. Activate it:

   **Windows Cmd Prompt:**

   ```bat
   .env\Scripts\activate
   ```

   **Windows PowerShell:**

   ```powershell
   .env\Scripts\Activate.ps1
   ```

   **macOS or Linux:**

   ```bash
   source .env/bin/activate
   ```

4. Upgrade packaging tools and install dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Create or update the required configuration files described below.

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

9. Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

Press `Ctrl+C` to stop the server. Run `deactivate` to leave the virtual environment.

## Configuration

The project includes configuration managed through Django settings and may use `secrets.env` or environment variables. Consult `settings.py` and the repository's dependency setup for the exact variable names.

Never commit real credentials, secret keys, passwords, API keys, or populated environment files.

Recommended local setup:

- Use a unique Django `SECRET_KEY` for development.
- Keep `DEBUG=True` only for local development.
- Restrict `ALLOWED_HOSTS` outside local development.
- Use development-only database credentials if external services are introduced.
- Store secrets outside version control.
- Verify media, upload, email, database, cache, and security settings before deployment.

A sample configuration `secrets.env` may contain placeholders only, ie:

```env
DJANGO_SECRET_KEY=replace-with-a-local-development-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

Use only names and formats supported by the current settings implementation.

## Application Workflow

1. A visitor registers or signs in using the appropriate role.
2. A donor completes a profile and submits a donation application.
3. An administrator verifies an eligible hospital account.
4. The application is assigned to a hospital for administrative review.
5. Authorized hospital staff review the submission and any supported medical documents.
6. The hospital schedules an appointment or updates the application status according to its workflow.
7. The donor receives in-app notifications & an email and can track the current status.
8. Administrator accounts and activity logs provide broader oversight of system operations.

Available statuses and actions depend on the current implementation and should not be interpreted as medical decisions.

## Development Commands

Run commands from the directory containing `manage.py`.

```bash
# Validate project configuration and models
python manage.py check

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Start the development server
python manage.py runserver

# Open an interactive Django shell
python manage.py shell

# Collect static files for a deployment setup
python manage.py collectstatic
```

## Testing

Use Django's test runner where tests are available:

```bash
python manage.py test
```

For useful coverage, test:

- Login and logout behavior.
- Role-specific access restrictions.
- Hospital account verification.
- Application creation and assignment.
- Appointment lifecycle changes.
- Notification delivery.
- Medical document upload validation.
- Unauthorized URL and direct-object access attempts.

Use only fictional information and disposable files in tests and development.

## Security and Privacy

- Apply authorization checks on every protected view and sensitive object lookup.
- Prevent hospitals from browsing unassigned applications or unrelated records.
- Validate and restrict uploaded file types, names, sizes, and storage locations.
- Serve uploads with appropriate authentication and caching rules.
- Keep Django and all dependencies up to date.
- Use HTTPS and secure cookies for deployment.
- Configure CSRF, password, session, backup, and database protections.
- Review third-party packages before deployment.
- Restrict administrator privileges.
- Do not log sensitive medical or personal information.

A role-based interface is not sufficient to make LifeLink secure or compliant with applicable healthcare, privacy, or record-retention requirements. The project must undergo legal, clinical, security, infrastructure, and accessibility reviews before any real-world use.

LifeLink registration or application approval does not establish donor eligibility or medical clearance.

## Project Status

LifeLink is under active development. Features, database models, routes, configuration, UI screens, and workflow rules may change without notice.

Before relying on the application, document the exact version, test it with representative role scenarios, and verify the implementation against the requirements of the environment in which it will run.

## Contributing

Contributions are welcome, with the following expectations:

1. Create a focused branch for your change.
2. Keep changes consistent with the existing Django app structure and style.
3. Run migrations when changing models.
4. Add or update tests for security and workflow changes.
5. Do not include real credentials or personal or medical data.
6. Review migrations and configuration differences before submitting.
7. Describe the purpose and testing performed for any pull request.

## License

No formal license is specified in this README or confirmed by the repository content. Check the repository for an existing license file and obtain the owner's permission before reuse or redistribution.

