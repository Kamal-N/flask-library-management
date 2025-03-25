# Library Management System

![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![Flask](https://img.shields.io/badge/flask-2.0%2B-green) ![SQLite](https://img.shields.io/badge/sqlite-3-lightgrey)

## Overview

This is a web-based Library Management System built with Flask. It allows users to register, search for books, borrow books, and manage their library accounts. Admins can oversee books and users, ensuring smooth operations.

## Features

- ✅ User authentication (Register/Login/Logout)
- 🔍 Book search using Google Books API
- 📚 Book borrowing and return functionality
- ⏳ Overdue book status tracking
- 🛠️ Admin dashboard for managing users and books
- ✨ Flash messages for an improved user experience

## Technologies Used

- **Flask** (Web Framework)
- **Flask-Login** (User Authentication)
- **Flask-WTF** (Forms & CSRF Protection)
- **Flask-Bootstrap** (UI Styling)
- **SQLAlchemy** (Database ORM)
- **SQLite** (Database)
- **Google Books API** (Book Search)

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/Kamal-N/flask-library-management.git
cd flask-library-management
```

### 2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Run the application:

Open the project in an IDE like VS Code, then run:

```bash
python main.py
```

### 5. Open a browser and navigate to:

```
http://127.0.0.1:5000/
```

## Usage

### 📝 User Registration & Login

- Users can register an account and log in to access the system.
- Flash messages provide guidance on login failures and successes.

### 🔍 Book Search

- Users can search for books using the Google Books API.
- Books can be added to the library from search results.

### 📖 Borrowing & Returning Books

- Users can borrow available books.
- Overdue books trigger a warning message upon login.
- Borrowed books can be tracked from the user dashboard.

### 🛠️ Admin Features

- Admins can view, edit, and delete users and books.
- Borrowed books can be managed to ensure timely returns.
- **Note**: The role of a user is set as user by default. To make a user an admin, manually modify the role via the IDE and the database extension.

## Environment Variables

The project requires a Google Books API Key. Paste it directly into `main.py` in the appropriate field:

```python
GOOGLE_API_KEY = "your_api_key_here"
```

## 📜 License

This project is licensed under the MIT License.

