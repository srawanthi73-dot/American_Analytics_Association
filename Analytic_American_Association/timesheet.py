import os
import random
import re
from datetime import datetime
from task import load_all_tasks
from employee import load_all_employees
from client import load_all_clients

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIMESHEET_FILE = os.path.join(BASE_DIR, "timesheet.txt")

class TimeSheet:
    """
    Time Sheet Management class.
    Attributes:
        timesheet_id: Auto-generated 'TMS_<6digits random Number>'
        timesheet_date: format 'yyyy/MM/dd'
        employee_id: valid existing employee ID
        client_id: valid existing client ID
        task_id: valid existing task ID
        hours: float/int > 0 and <= 8 hrs
    """
    def __init__(self, timesheet_date, employee_id, client_id, task_id, hours, timesheet_id=None):
        self.timesheet_id = timesheet_id if timesheet_id else self.generate_timesheet_id()
        self.timesheet_date = self.validate_date(timesheet_date)
        self.employee_id = self.validate_employee(employee_id)
        self.client_id = self.validate_client(client_id)
        self.task_id = self.validate_task(task_id)
        self.hours = self.validate_hours(hours)

    @staticmethod
    def generate_timesheet_id():
        existing_ids = {ts["timesheet_id"] for ts in load_all_timesheets()}
        while True:
            new_id = f"TMS_{random.randint(100000, 999999)}"
            if new_id not in existing_ids:
                return new_id

    @staticmethod
    def validate_date(date_str):
        if not date_str or not str(date_str).strip():
            raise ValueError("Timesheet date cannot be empty.")
        date_str = str(date_str).strip()
        try:
            datetime.strptime(date_str, "%Y/%m/%d")
            return date_str
        except ValueError:
            raise ValueError("Date should be of the format yyyy/MM/dd (e.g. 2026/01/15).")

    @staticmethod
    def validate_employee(emp_id):
        if not emp_id or not str(emp_id).strip():
            raise ValueError("Employee ID cannot be empty.")
        emp_id = str(emp_id).strip()
        employees = load_all_employees()
        existing_ids = [e["employee_id"].upper() for e in employees]
        if emp_id.upper() not in existing_ids:
            raise ValueError(f"Employee ID '{emp_id}' not found in the system.")
        for e in employees:
            if e["employee_id"].upper() == emp_id.upper():
                return e["employee_id"]
        return emp_id

    @staticmethod
    def validate_client(client_id):
        if not client_id or not str(client_id).strip():
            raise ValueError("Client ID cannot be empty.")
        client_id = str(client_id).strip()
        clients = load_all_clients()
        existing_ids = [c["client_id"].upper() for c in clients]
        if client_id.upper() not in existing_ids:
            raise ValueError(f"Client ID '{client_id}' not found in the system.")
        for c in clients:
            if c["client_id"].upper() == client_id.upper():
                return c["client_id"]
        return client_id

    @staticmethod
    def validate_task(task_id):
        if not task_id or not str(task_id).strip():
            raise ValueError("Task ID cannot be empty.")
        task_id = str(task_id).strip()
        tasks = load_all_tasks()
        existing_ids = [t["task_id"].upper() for t in tasks]
        if task_id.upper() not in existing_ids:
            raise ValueError(f"Task ID '{task_id}' not found in the system.")
        for t in tasks:
            if t["task_id"].upper() == task_id.upper():
                return t["task_id"]
        return task_id

    @staticmethod
    def validate_hours(hours):
        if hours is None or str(hours).strip() == "":
            raise ValueError("Hours cannot be empty.")
        try:
            val = float(str(hours).strip())
            if val <= 0:
                raise ValueError("Hours worked must be greater than 0.")
            if val > 8.0:
                raise ValueError("Number of hours shouldn't be more than 8hrs.")
            return val
        except ValueError as e:
            if "greater than 0" in str(e) or "more than 8" in str(e):
                raise
            raise ValueError("Hours should be in integer or float only.")

    def save_timesheet(self, filename=TIMESHEET_FILE):
        with open(filename, "a", encoding="utf-8") as f:
            f.write(
                f"Timesheet ID: {self.timesheet_id}\n"
                f"Timesheet Date: {self.timesheet_date}\n"
                f"Employee ID: {self.employee_id}\n"
                f"Client ID: {self.client_id}\n"
                f"Task ID: {self.task_id}\n"
                f"Hours: {self.hours}\n"
                "------------------------------\n"
            )

    @classmethod
    def create_timesheet_interactive(cls):
        print("\n--- Create New Time Sheet ---")
        try:
            date_in = input("Enter Timesheet Date (yyyy/MM/dd): ").strip()
            date_val = cls.validate_date(date_in)

            emp_in = input("Enter Employee ID: ").strip()
            emp_val = cls.validate_employee(emp_in)

            clt_in = input("Enter Client ID: ").strip()
            clt_val = cls.validate_client(clt_in)

            tsk_in = input("Enter Task ID: ").strip()
            tsk_val = cls.validate_task(tsk_in)

            hours_in = input("Enter Hours worked (<= 8 hrs): ").strip()
            hours_val = cls.validate_hours(hours_in)

            ts = cls(date_val, emp_val, clt_val, tsk_val, hours_val)
            ts.save_timesheet()
            print("\nTimesheet created successfully!")
            print(f"Generated Timesheet ID: {ts.timesheet_id}")
            return ts
        except ValueError as e:
            print(f"Error creating timesheet: {e}")
            return None

    @classmethod
    def update_time_sheet(cls, timesheet_id=None):
        if not timesheet_id:
            timesheet_id = input("Enter Timesheet ID to update: ").strip()
        timesheets = load_all_timesheets()
        ts_found = False
        updated_ts_list = []

        for ts in timesheets:
            if ts["timesheet_id"].upper() == timesheet_id.upper():
                ts_found = True
                print(f"Timesheet found: Date {ts['timesheet_date']}, Emp {ts['employee_id']}")
                try:
                    new_client = input(f"Enter new Client ID [{ts['client_id']}]: ").strip() or ts['client_id']
                    new_client = cls.validate_client(new_client)

                    new_task = input(f"Enter new Task ID [{ts['task_id']}]: ").strip() or ts['task_id']
                    new_task = cls.validate_task(new_task)

                    new_hours_str = input(f"Enter new Hours [{ts['hours']}]: ").strip() or str(ts['hours'])
                    new_hours = cls.validate_hours(new_hours_str)

                    ts["client_id"] = new_client
                    ts["task_id"] = new_task
                    ts["hours"] = new_hours
                    print("Timesheet updated successfully.")
                except ValueError as e:
                    print(f"Update failed: {e}")
                    return False
            updated_ts_list.append(ts)

        if not ts_found:
            print("Timesheet ID not found.")
            return False

        save_all_timesheets(updated_ts_list)
        return True

    @classmethod
    def delete_time_sheet(cls, timesheet_id=None):
        print("Time Sheet cannot be deleted once submitted, so don't delete any time sheet.")
        return False

    @classmethod
    def search_time_sheet(cls, timesheet_id=None):
        if not timesheet_id:
            timesheet_id = input("Enter Timesheet ID to search: ").strip()
        timesheets = load_all_timesheets()
        for ts in timesheets:
            if ts["timesheet_id"].upper() == timesheet_id.upper():
                print("\n------------------------------")
                print(f"Timesheet ID   : {ts['timesheet_id']}")
                print(f"Timesheet Date : {ts['timesheet_date']}")
                print(f"Employee ID    : {ts['employee_id']}")
                print(f"Client ID      : {ts['client_id']}")
                print(f"Task ID        : {ts['task_id']}")
                print(f"Hours Worked   : {ts['hours']}")
                print("------------------------------")
                return ts
        print("Timesheet ID not found.")
        return None

    @classmethod
    def display_all_time_sheets(cls):
        timesheets = load_all_timesheets()
        if not timesheets:
            print("no timesheets are available in the system")
            return
        print("\nAvailable Timesheets:")
        print("--------------------------------------------------------------------------------")
        for ts in timesheets:
            print(f"ID: {ts['timesheet_id']} | Date: {ts['timesheet_date']} | Emp: {ts['employee_id']} | "
                  f"Client: {ts['client_id']} | Task: {ts['task_id']} | Hours: {ts['hours']}")
        print("--------------------------------------------------------------------------------")


def load_all_timesheets(filename=TIMESHEET_FILE):
    if not os.path.exists(filename):
        return []
    timesheets = []
    with open(filename, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    records = content.split("------------------------------\n")
    for rec in records:
        rec = rec.strip()
        if not rec:
            continue
        lines = rec.split("\n")
        data = {}
        for line in lines:
            if ": " in line:
                k, v = line.split(": ", 1)
                data[k.strip().lower()] = v.strip()
        if "timesheet id" in data:
            ts_id = data["timesheet id"]
            ts_date = data.get("timesheet date", "")
            emp_id = data.get("employee id", "")
            clt_id = data.get("client id", "")
            tsk_id = data.get("task id", "")
            try:
                hours_val = float(data.get("hours", "0"))
            except ValueError:
                hours_val = 0.0
            timesheets.append({
                "timesheet_id": ts_id,
                "timesheet_date": ts_date,
                "employee_id": emp_id,
                "client_id": clt_id,
                "task_id": tsk_id,
                "hours": hours_val
            })
    return timesheets


def save_all_timesheets(timesheets, filename=TIMESHEET_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        for ts in timesheets:
            f.write(
                f"Timesheet ID: {ts['timesheet_id']}\n"
                f"Timesheet Date: {ts['timesheet_date']}\n"
                f"Employee ID: {ts['employee_id']}\n"
                f"Client ID: {ts['client_id']}\n"
                f"Task ID: {ts['task_id']}\n"
                f"Hours: {ts['hours']}\n"
                "------------------------------\n"
            )


# Module-level aliases
update_time_sheet = TimeSheet.update_time_sheet
delete_time_sheet = TimeSheet.delete_time_sheet
search_time_sheet = TimeSheet.search_time_sheet
display_all_time_sheets = TimeSheet.display_all_time_sheets
dispaly_all_time_sheets = TimeSheet.display_all_time_sheets
