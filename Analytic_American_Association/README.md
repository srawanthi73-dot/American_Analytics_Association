# Analytic American Association - Law Firm Management System

## Project Name
**Analytic American Association**

## Description
This project is an enterprise-grade command-line Law Firm Management System developed in Python. It handles clients, employees (lawyers), tasks, timesheets, and billing management with strict data validation, Object-Oriented Programming (OOPS) design patterns (composition, inheritance, encapsulation), and file-based data persistence.

### Key Capabilities
- **Task Management**: Create, update, search, delete, and list tasks. Tasks can be billable (chargeable) or non-billable, with hourly rate card validation. Tasks can also be bulk-imported from `tasks.csv`.
- **Address Validation**: Comprehensive address validator supporting unique emails, 10-digit phone numbers (with optional `+91`), house/building/road details, landmark, city, state, and zip code.
- **Employee (Lawyer) Management**: Manage lawyers and their standard billing rates. Compose `Address` objects into `Employee` profiles. Bulk import lawyers from `Employee.csv`.
- **Client Management**: Manage clients with unique problem descriptions and rate cards. The `Client` class inherits directly from `Address` (demonstrating OOP inheritance). Bulk import clients from `Clients.csv`.
- **Time Sheet Management**: Track work performed by lawyers for specific clients on specific tasks, capped at a maximum of 8 hours per entry with validation against existing entity records. Time sheets are protected from deletion once submitted.
- **Admin (Billing Management)**: Dynamically generate detailed employee and client bills based on recorded timesheet hours and rates, saving formatted output to `Employee_Bill.txt` and `Client_Bill.txt`.

---

## Requirements
- Python 3.8 or higher.
- Built strictly using Python Standard Library (`os`, `csv`, `re`, `random`, `datetime`, `sys`). No external pip dependencies required.

---

## File Structure
```text
MiniProject-1/
├── start.py         # Primary entry point (matching exact terminal specification)
├── main.py          # Standard project entry point
├── mycode.py        # Forwarding runner and export module
├── address.py       # Address class with validations and unique email tracking
├── task.py          # Task class, CSV loader, and text persistence
├── employee.py      # Employee class, CSV loader, and text persistence
├── client.py        # Client class (subclass of Address), CSV loader, and text persistence
├── timesheet.py     # TimeSheet class and validations
├── bill.py          # Dynamic bill generation for employees and clients
├── tasks.csv        # Pre-configured CSV data for tasks
├── Employee.csv     # Pre-configured CSV data for employees
├── Clients.csv      # Pre-configured CSV data for clients
└── README.md        # Project documentation
```

---

## How to Run

1. Open a terminal or command prompt in the project directory:
   ```bash
   cd "C:\Users\ADMIN\Desktop\MiniProject-1 (1)\MiniProject-1"
   ```

2. Run the application:
   ```bash
   python start.py
   ```
   *(Alternatively, `python main.py` or `python mycode.py` also work)*

---

## Main Menu Navigation
```text
        1. Task
        2. Employee
        3. Client
        4. Time Sheet
        5. Admin
        6. Exit

Enter your choice:
```
- **Option 1 (Task)**: Create, import from `tasks.csv`, update, search, delete, and list tasks.
- **Option 2 (Employee)**: Create, import from `Employee.csv`, update, search, delete, and list employees.
- **Option 3 (Client)**: Create, import from `Clients.csv`, update, search, delete, and list clients.
- **Option 4 (Time Sheet)**: Log daily work hours (<= 8 hours), update, search, and list timesheets.
- **Option 5 (Admin)**: Dynamically generate and export Employee and Client bills.
- **Option 6 (Exit)**: Exit the application cleanly.
