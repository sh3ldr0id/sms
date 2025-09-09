# SMS - Shop Management System

Lightweight POS / shop management system built in Python + MySQL. Provides customer, employee, product and billing management with simple CLI/printable bill output.

## Features
- Customer management (create, view, delete)
- Employee management and email/password login
- Product management (stock, price, cost)
- Create bills: calculates totals, applies discount, updates product stock
- View and delete bills
- Printable text bill layout

## Requirements
- Windows 10/11
- Python 3.10+ (recommended)
- MySQL server
- Virtual environment (recommended)
- Python packages (see requirements.txt)
  - mysql-connector-python

## Quick setup (Windows)

1. Clone repo and change into project folder
   ```
   cd "c:\Users\sh3ld\Dev\Gen7\SMS - Shop Management System"
   ```

2. Create and activate a venv, then install deps
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create the database and seed sample data
   - Using MySQL client:
     ```
     mysql -u root -p < db.sql
     ```
   - Or open `db.sql` in MySQL Workbench and run it.

4. Configure database credentials
   - Edit `app/__init__.py` and set your MySQL connection details (host, user, password, database).
   - Example connection snippet to place in `app/__init__.py` (edit credentials before use):
     ```python
     # filepath: c:\Users\sh3ld\Dev\Gen7\SMS - Shop Management System\app\__init__.py
     import mysql.connector
     connection = mysql.connector.connect(
         host="127.0.0.1",
         user="your_mysql_user",
         password="your_mysql_password",
         database="smsdb",
         autocommit=False
     )
     cursor = connection.cursor()
     def start():
         # existing start() entrypoint in the package
         ...
     ```
   - If the package already creates connection here, update the credentials only.

5. Run the app
   ```
   python run.py
   ```

## Notes
- Default admin (from db.sql): email `sh3ldr0id@gmail.com`, password `password`. Change password after first login.
- Discounts in billing are treated as percentage values (e.g. `10` => 10%). The code expects `discount` as a percent when computing totals (it divides by 100).
- The printable bill is plain-text and aligned to a fixed-width layout. If product names are longer than the column width they will be truncated.
- If you see ImportError due to circular imports (app imports employee which imports app), ensure `connection`/`cursor` are created in `app.__init__.py` (or in a dedicated module like `app/db.py`) and imported as `from app import connection, cursor` or `from app.db import connection, cursor` consistently.

## Common troubleshooting
- "Not all parameters were used in the SQL statement" — ensure SQL placeholders match the connector style (%s for mysql-connector-python).
- Already tracked __pycache__ files: add `__pycache__/` and `*.pyc` to `.gitignore`, then run:
  ```
  git rm -r --cached .
  git add .
  git commit -m "Ignore __pycache__ and bytecode"
  ```
- If using multiple threads, avoid sharing the same DB connection across threads without proper locking.

## File layout (important files)
- run.py — app entrypoint
- db.sql — schema + seed data
- app/__init__.py — package init + DB connection / start() entry
- app/billing.py — billing and printable bill logic
- app/logistics.py — product helpers (price, stock)
- app/employee.py — employees, auth helpers
- requirements.txt — Python dependencies