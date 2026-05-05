# 📚 Library Management System 

Library Management System built with **Python**, **SQLAlchemy ORM**, and **MySQL**. This project demonstrates advanced database concepts including relational design, SQL Triggers, role-based access control (RBAC), and statistical reporting.

## ✨ Key Features

*   **🛡️ Role-Based Security**: Dual-user architecture at the database level.
    *   `librarian_user`: Full CRUD access for library administration.
    *   `reader_user`: Read-only access for searching books and authors.
*   **⚙️ Smart Inventory Management**: Automated tracking of `AvailableQuantity` and `TotalQuantity`. SQL Triggers automatically deduct/add books to the shelf when a borrowing/returning transaction occurs.
*   **🧠 Intelligent Data Entry**: When adding a new book, the system automatically checks and creates new Authors and Categories if they don't exist, utilizing `session.flush()` and `session.rollback()` to prevent database junk.
*   **📊 Analytics Dashboard**: Real-time statistical calculation of library usage (percentage of books borrowed, active readers) and overdue tracking (> 14 days).
*   **🔒 Data Integrity**: Prevents the deletion of books that have an existing borrowing history to maintain accurate historical records.

## Technologies Used

*   **Language**: Python 3.13
*   **Database**: MySQL 8.0
*   **ORM**: SQLAlchemy (Protects against SQL Injection)
*   **Driver**: `mysql-connector-python` (with `use_pure=True` to prevent C-extension crashes)

## Project Structure

```text
├── library_database.sql       # Database schema, Triggers, Sample Data, and User Grants
├── library_database.py        # Main application logic and CLI menus
└── README.md                  # Project documentation

## Installation & Setup
Follow these steps to run the project on your local machine:

1. Database Setup
Open MySQL Workbench.

Open the database.sql file and execute the entire script.

This script will automatically:

Create the lib database.

Set up all tables, foreign keys, and triggers.

Insert 10 sample records for each table.

Create two database users: librarian_user and reader_user.

2. Python Environment Setup
Ensure you have Python installed.

Open your terminal/command prompt and install the required libraries:

pip install sqlalchemy mysql-connector-python

3. Run the Application

Navigate to the project directory in your terminal.
Run the Python application:
   
python library_database.py
   
📖 Usage Guide
Once the application is running, you will be greeted by a Multi-level Main Menu. Here is how to navigate the system:

📚 1. Book Management (Option 1)
View All / Search: Browse the entire catalog or search by book title/author name.

Add Book: Enter a new book. Note: If you enter an Author or Category that doesn't exist, the system will smartly create them for you in the background!

Edit Book: Update details. If you change the Total Quantity, the system automatically calculates and adjusts the Available Quantity on the shelf.

Delete Book: Remove a book (only if it has never been borrowed to protect historical data).

👤 2. Readers & Transactions (Option 2)
Borrow Book: Enter the Reader ID and Book ID. The database trigger will automatically decrease the book's available stock.

Return Book: Enter the Borrow ID. The system marks it as returned and automatically increases the available stock.

Register Reader: Add a new reader to the library system.

✍️ 3. Author & Category Management (Option 3)
View all registered authors and categories.

Fix typos or update author names directly.

📊 4. Reports & Statistics (Option 4)
Currently Borrowed: View a list of all books that are currently out of the library.

Overdue Report: Instantly flag transactions that have been borrowed for more than 14 days.

Library Dashboard: View live statistics, including the percentage (%) of your inventory currently borrowed and the percentage of active readers.

💡 How to Test User Roles (Security Demo)
By default, the application is configured to run as the Librarian. To test the system's database-level security, open app.py and modify the DATABASE_URI at the top of the file:

Run as Librarian (Full Access):

Python
DATABASE_URI = 'mysql+mysqlconnector://librarian_user:StrongPass_Lib2026!@127.0.0.1:3306/lib'
Run as Reader (Read-Only Access):

Python
DATABASE_URI = 'mysql+mysqlconnector://reader_user:StrongPass_Read2026!@127.0.0.1:3306/lib'
Note: If you run as reader_user and attempt to add/edit/borrow a book, the application will catch an Access Denied error from MySQL, proving the backend security works perfectly.

Developed by: Ta Quang Huy
Student ID  : 11247175

Project: Database Management Systems
