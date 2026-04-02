# Student Management System

A web-based Student Management System built using the Django framework. This application allows users to perform Create, Read, Update, and Delete (CRUD) operations on student records, complete with user authentication and search functionalities.

## Features

- **User Authentication:** Secure signup and login for both regular users and admins.
- **Student Records Management:** Add, view, edit, and delete student details (Name, Age, Email, Course).
- **Filtering & Search:** Easily search for students based on their enrolled course.
- **Pagination:** Structured rendering of lists showing up to 5 students per page.
- **Role-based Redirection:** Automatically routes admin users to a dedicated dashboard (`home0`) and regular users to a standard view (`home2`).
- **Relational Database:** Now uses **MySQL** as its backend database for enhanced reliability and performance.

## Prerequisites

Before running this project, ensure you have the following installed on your machine:
- Python 3.x
- pip (Python package installer)
- MySQL Server

## Setup and Installation

Follow these steps to get the development environment running:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rizwanrichu87/Student_Management.git
   cd Student_Management
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   Since a `requirements.txt` might be missing, make sure you install Django and the mysqlclient:
   ```bash
   pip install django mysqlclient
   ```

4. **Configure the Database:**
   - Create a MySQL database for the project (e.g., `student_management`).
   - Update the `DATABASES` dictionary in `Project2/settings.py` with your MySQL user, password, and database name.

5. **Run Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser (Optional but recommended):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Folder Structure

```
Student_Management/
│
├── Project2/              # Core Django settings and URL configurations
├── student/               # Main app handling views, models, and UI templates
├── manage.py              # CLI utility for Django
└── .gitignore             # Ignored files for git version control
```

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---
*Built with ❤️ utilizing Django & MySQL.*
