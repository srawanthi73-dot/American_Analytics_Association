Overview
An end-to-end management console built for law firms and professional service agencies. The system automates client intake, attorney profile management, task allocation, timesheet tracking, and dynamic billing generation while enforcing strict data consistency and business rules.

Key Software Engineering Highlights
Designed to demonstrate core Object-Oriented Programming (OOP) and clean-code practices:
OOP Inheritance: Client inherits directly from Address, demonstrating subclassing and code reuse.
OOP Composition: Employee encapsulates an Address instance, illustrating modular object composition.
Strict Data Validation: Regex-driven validation rules for emails, phone numbers (+91 supported), dates (yyyy/MM/dd), hours (<= 8 hrs/day), and financial values.
File I/O & CSV Ingestion: Automated batch import and parsing of legacy CSV datasets with automatic character encoding fallbacks and duplicate-prevention hashing.
Dynamic Invoicing: On-the-fly bill calculation cross-referencing timesheet logs against entity billing rates with formatted .txt exports.
Graceful Error Handling: Custom exception management preventing application crashes on malformed inputs.

Project Structure
├── start.py         # Application entry point & interactive terminal UI
├── main.py          # Alternative standard runner
├── address.py       # Address class with regex validation & email uniqueness
├── task.py          # Task lifecycle (billable/non-billable, rate cards)
├── employee.py      # Attorney profiles & rate-card assignment
├── client.py        # Client model extending Address
├── timesheet.py     # Timesheet logging & business logic constraints
├── bill.py          # Dynamic billing engine for attorneys and clients
├── *.csv            # Mock legacy datasets (Tasks, Employees, Clients)
└── README.md

Quick Start
Prerequisites
Python 3.8 or higher (No third-party packages required — uses standard library).
Installation & Execution
Clone the repository:
git clone https://github.com/<your-username>/law-firm-management-system.git
cd law-firm-management-system
Run the application:
python start.py

Menu Options
        1. Task         - Create, batch import (tasks.csv), update, search, delete
        2. Employee     - Attorney management & batch import (Employee.csv)
        3. Client       - Client management & batch import (Clients.csv)
        4. Time Sheet   - Log daily work hours (<= 8 hrs), query & update logs
        5. Admin        - Generate itemized bills for Employees & Clients
        6. Exit         - Clean session termination

Built With
Language: Python 3
Libraries: Built purely with standard Python modules (re, csv, datetime, os, random, sys) to ensure zero-dependency deployment.

