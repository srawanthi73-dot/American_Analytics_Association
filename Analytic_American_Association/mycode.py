"""
Analytic American Association Project
Refactored and corrected implementation.
Imports all required classes, functions, and executes the main application.
"""
from task import (
    Task,
    create_tasks_from_csv,
    update_task,
    delete_task,
    search_task,
    display_all_tasks
)
from address import Address
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
    generate_client_bill,
    generate_bill
)
from start import main

if __name__ == "__main__":
    main()
