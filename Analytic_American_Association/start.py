import sys
from task import (
    Task,
    create_tasks_from_csv,
    update_task,
    delete_task,
    search_task,
    display_all_tasks
)
from employee import (
    Employee,
    read_employee_csv,
    update_employee,
    delete_employee,
    search_employee,
    display_all_employees
)
from client import (
    Client,
    read_clients_csv,
    update_client,
    delete_client,
    search_client,
    display_all_clients
)
from timesheet import (
    TimeSheet,
    update_time_sheet,
    delete_time_sheet,
    search_time_sheet,
    display_all_time_sheets
)
from bill import (
    generate_employee_bill,
    generate_client_bill
)

def task_menu():
    while True:
        print("\n        --- TASK MANAGEMENT ---")
        print("        1. Create Task")
        print("        2. Import Tasks from CSV")
        print("        3. Update Task")
        print("        4. Delete Task")
        print("        5. Search Task")
        print("        6. Display All Tasks")
        print("        7. Back\n")
        ch = input("Enter your choice: ").strip()

        if ch == "1":
            Task.create_task_interactive()
        elif ch == "2":
            create_tasks_from_csv()
        elif ch == "3":
            update_task()
        elif ch == "4":
            delete_task()
        elif ch == "5":
            search_task()
        elif ch == "6":
            display_all_tasks()
        elif ch == "7":
            break
        else:
            print("Invalid choice. Please enter a valid option (1-7).")

def employee_menu():
    while True:
        print("\n        --- EMPLOYEE MANAGEMENT ---")
        print("        1. Create Employee")
        print("        2. Import Employees from CSV")
        print("        3. Update Employee")
        print("        4. Delete Employee")
        print("        5. Search Employee")
        print("        6. Display All Employees")
        print("        7. Back\n")
        ch = input("Enter your choice: ").strip()

        if ch == "1":
            Employee.create_employee_interactive()
        elif ch == "2":
            read_employee_csv()
        elif ch == "3":
            update_employee()
        elif ch == "4":
            delete_employee()
        elif ch == "5":
            search_employee()
        elif ch == "6":
            display_all_employees()
        elif ch == "7":
            break
        else:
            print("Invalid choice. Please enter a valid option (1-7).")

def client_menu():
    while True:
        print("\n        --- CLIENT MANAGEMENT ---")
        print("        1. Create Client")
        print("        2. Import Clients from CSV")
        print("        3. Update Client")
        print("        4. Delete Client")
        print("        5. Search Client")
        print("        6. Display All Clients")
        print("        7. Back\n")
        ch = input("Enter your choice: ").strip()

        if ch == "1":
            Client.create_client_interactive()
        elif ch == "2":
            read_clients_csv()
        elif ch == "3":
            update_client()
        elif ch == "4":
            delete_client()
        elif ch == "5":
            search_client()
        elif ch == "6":
            display_all_clients()
        elif ch == "7":
            break
        else:
            print("Invalid choice. Please enter a valid option (1-7).")

def timesheet_menu():
    while True:
        print("\n        --- TIME SHEET MANAGEMENT ---")
        print("        1. Create Time Sheet")
        print("        2. Update Time Sheet")
        print("        3. Search Time Sheet")
        print("        4. Display All Time Sheets")
        print("        5. Delete Time Sheet")
        print("        6. Back\n")
        ch = input("Enter your choice: ").strip()

        if ch == "1":
            TimeSheet.create_timesheet_interactive()
        elif ch == "2":
            update_time_sheet()
        elif ch == "3":
            search_time_sheet()
        elif ch == "4":
            display_all_time_sheets()
        elif ch == "5":
            delete_time_sheet()
        elif ch == "6":
            break
        else:
            print("Invalid choice. Please enter a valid option (1-6).")

def admin_menu():
    while True:
        print("\n        --- ADMIN (BILLING MANAGEMENT) ---")
        print("        1. Generate Employee Bill")
        print("        2. Generate Client Bill")
        print("        3. Back\n")
        ch = input("Enter your choice: ").strip()

        if ch == "1":
            generate_employee_bill()
        elif ch == "2":
            generate_client_bill()
        elif ch == "3":
            break
        else:
            print("Invalid choice. Please enter a valid option (1-3).")

def main():
    while True:
        print("\n")
        print("        1. Task")
        print("        2. Employee")
        print("        3. Client")
        print("        4. Time Sheet")
        print("        5. Admin")
        print("        6. Exit\n")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            task_menu()
        elif choice == "2":
            employee_menu()
        elif choice == "3":
            client_menu()
        elif choice == "4":
            timesheet_menu()
        elif choice == "5":
            admin_menu()
        elif choice == "6":
            print("\nThank you for using Analytic American Association System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
