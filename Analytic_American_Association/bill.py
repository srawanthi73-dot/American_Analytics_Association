import os
from datetime import datetime
from employee import load_all_employees
from client import load_all_clients
from timesheet import load_all_timesheets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_employee_bill(employee_id=None):
    """
    Generates dynamic bill for an employee by reading employee and timesheet records.
    Outputs to Employee_Bill.txt (and console).
    """
    if not employee_id:
        employee_id = input("Enter Employee ID: ").strip()

    employees = load_all_employees()
    emp = None
    for e in employees:
        if e["employee_id"].upper() == employee_id.upper():
            emp = e
            break

    if not emp:
        print("Employee ID is not found.")
        return None

    # Read timesheet.txt and calculate total hours for this employee
    timesheets = load_all_timesheets()
    emp_timesheets = [ts for ts in timesheets if ts["employee_id"].upper() == employee_id.upper()]

    bill_hours = sum(ts["hours"] for ts in emp_timesheets)
    bill_rate = float(emp["std_bill_rate"])
    bill_amount = bill_hours * bill_rate
    bill_date = datetime.now().strftime("%Y/%m/%d")

    bill_status = input("Enter bill status (Paid/Unpaid or Yes/No): ").strip()
    if not bill_status:
        bill_status = "Unpaid"

    bill_content = (
        "**************************************************\n"
        "                  EMPLOYEE BILL                   \n"
        "**************************************************\n"
        f"Bill Date       : {bill_date}\n"
        f"Employee ID     : {emp['employee_id']}\n"
        f"Employee Name   : {emp['employee_name']}\n"
        f"Bill Hours      : {bill_hours}\n"
        f"Bill Rate       : {bill_rate}\n"
        f"Bill Amount     : {bill_amount}\n"
        f"Bill Status     : {bill_status}\n"
        "**************************************************\n"
    )

    out_file = os.path.join(BASE_DIR, "Employee_Bill.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(bill_content)

    print("\n" + bill_content)
    print(f"Employee bill generated and saved to '{out_file}'.")
    return bill_content


def generate_client_bill(client_id=None):
    """
    Generates dynamic bill for a client by reading client and timesheet records.
    Outputs to Client_Bill.txt (and console).
    """
    if not client_id:
        client_id = input("Enter Client ID: ").strip()

    clients = load_all_clients()
    client = None
    for c in clients:
        if c["client_id"].upper() == client_id.upper():
            client = c
            break

    if not client:
        print("Client ID is not found.")
        return None

    # Read timesheet.txt and calculate total hours for this client
    timesheets = load_all_timesheets()
    clt_timesheets = [ts for ts in timesheets if ts["client_id"].upper() == client_id.upper()]

    bill_hours = sum(ts["hours"] for ts in clt_timesheets)
    bill_rate = float(client["std_bill_rate"])
    bill_amount = bill_hours * bill_rate
    bill_date = datetime.now().strftime("%Y/%m/%d")

    bill_status = input("Enter bill status (Paid/Unpaid or Yes/No): ").strip()
    if not bill_status:
        bill_status = "Unpaid"

    bill_content = (
        "**************************************************\n"
        "                   CLIENT BILL                    \n"
        "**************************************************\n"
        f"Bill Date       : {bill_date}\n"
        f"Client ID       : {client['client_id']}\n"
        f"Client Name     : {client['client_name']}\n"
        f"Bill Hours      : {bill_hours}\n"
        f"Bill Rate       : {bill_rate}\n"
        f"Bill Amount     : {bill_amount}\n"
        f"Bill Status     : {bill_status}\n"
        "**************************************************\n"
    )

    out_file = os.path.join(BASE_DIR, "Client_Bill.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(bill_content)

    print("\n" + bill_content)
    print(f"Client bill generated and saved to '{out_file}'.")
    return bill_content


def generate_bill(employee_id=None, client_id=None):
    """
    Optional combined bill generator for employee and client combination.
    """
    if not employee_id:
        employee_id = input("Enter Employee ID: ").strip()
    if not client_id:
        client_id = input("Enter Client ID: ").strip()

    employees = {e["employee_id"].upper(): e for e in load_all_employees()}
    clients = {c["client_id"].upper(): c for c in load_all_clients()}

    emp = employees.get(employee_id.upper())
    clt = clients.get(client_id.upper())

    if not emp:
        print("Employee ID is not found.")
        return
    if not clt:
        print("Client ID is not found.")
        return

    timesheets = load_all_timesheets()
    matched = [ts for ts in timesheets if ts["employee_id"].upper() == employee_id.upper() and ts["client_id"].upper() == client_id.upper()]

    total_hours = sum(ts["hours"] for ts in matched)
    rate = float(emp["std_bill_rate"])
    total_amount = total_hours * rate

    bill_content = (
        "==================== BILL ====================\n"
        f"Employee ID   : {emp['employee_id']}\n"
        f"Employee Name : {emp['employee_name']}\n"
        f"Client ID     : {clt['client_id']}\n"
        f"Client Name   : {clt['client_name']}\n\n"
        f"Hours Worked  : {total_hours}\n"
        f"Bill Rate     : {rate}\n"
        f"Total Amount  : {total_amount}\n"
        "==============================================\n"
    )

    out_file = os.path.join(BASE_DIR, "Bill.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(bill_content)

    print("\n" + bill_content)
    print("Bill generated successfully.")
