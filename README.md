# Organ Donation Project

This project is a web application built using Django to facilitate and manage organ donation processes. It aims to connect donors, recipients, and healthcare providers efficiently.

## Features

- User authentication and role-based access (Donor, Recipient, Admin).
- Donor registration and organ availability tracking.
- Recipient registration and organ request management.
- Matching system for donors and recipients.
- Admin dashboard for managing users and organ donation records.
- Notifications and updates for users.

## Installation

1. Clone the repository:
    ```sh
    git clone `https://github.com/harizonelopez/Organ-Donation-App.git`
    ```
2. Navigate to the project directory:
    ```bash
    cd Organ_Donation_App
    ```
3. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: source venv\Scripts\activate
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- Register as a donor or recipient to start using the platform.
- Admins can log in to manage the system.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Django documentation
- Open-source contributors
