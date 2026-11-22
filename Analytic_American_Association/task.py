import os
import csv
import random
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "tasks.txt")
TASKS_CSV = os.path.join(BASE_DIR, "tasks.csv")

class Task:
    """
    Task Management class.
    Attributes:
        task_id: Auto-generated 'TSK_<6digits random Number>'
        task_name: Alphanumeric, spaces, '-', '_'
        chargeable: True / False
        rate_card: float/int if chargeable, else 0.0 / None
    """
    def __init__(self, task_name, chargeable, rate_card=None, task_id=None):
        self.task_id = task_id if task_id else self.generate_task_id()
        self.task_name = self.validate_task_name(task_name)
        self.chargeable = self.validate_chargeable(chargeable)
        self.rate_card = self.validate_rate_card(rate_card, self.chargeable)

    @staticmethod
    def generate_task_id():
        # Ensure generated task_id is unique
        existing_ids = {t["task_id"] for t in load_all_tasks()}
        while True:
            new_id = f"TSK_{random.randint(100000, 999999)}"
            if new_id not in existing_ids:
                return new_id

    @staticmethod
    def validate_task_id(task_id):
        if not task_id or not str(task_id).strip():
            raise ValueError("Task ID cannot be empty.")
        task_id = str(task_id).strip()
        pattern = r'^TSK_\d{6}$'
        if not re.match(pattern, task_id):
            raise ValueError("Task ID must be in format TSK_<6 digits> (e.g. TSK_539493).")
        return task_id

    @staticmethod
    def validate_task_name(task_name):
        if not task_name or not str(task_name).strip():
            raise ValueError("Task name cannot be empty.")
        task_name = str(task_name).strip()
        pattern = r'^[A-Za-z0-9_\- ]+$'
        if not re.match(pattern, task_name):
            raise ValueError("Task name should consist of only upper/lower alphabets, digits, '-', '_', and spaces.")
        return task_name

    @staticmethod
    def validate_chargeable(chargeable):
        if isinstance(chargeable, bool):
            return chargeable
        val = str(chargeable).strip().lower()
        if val in ["yes", "y", "true", "t", "1"]:
            return True
        if val in ["no", "n", "false", "f", "0"]:
            return False
        raise ValueError("Chargeable should be True/False or Yes/No.")

    @staticmethod
    def validate_rate_card(rate_card, chargeable):
        if chargeable:
            if rate_card is None or str(rate_card).strip() == "":
                raise ValueError("Rate card is required for a chargeable task.")
            try:
                rate_str = str(rate_card).replace('$', '').strip()
                rate_val = float(rate_str)
                if rate_val < 0:
                    raise ValueError("Rate card cannot be negative.")
                return rate_val
            except ValueError:
                raise ValueError("Rate card must be an integer or float value.")
        else:
            return 0.0

    def save_task(self, filename=TASKS_FILE):
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"Task ID: {self.task_id}\n"
                    f"Task Name: {self.task_name}\n"
                    f"Chargeable: {self.chargeable}\n"
                    f"Rate Card: {self.rate_card}\n"
                    f"------------------------------\n")

    def savefile(self):
        self.save_task()

    @classmethod
    def create_task_interactive(cls):
        print("\n--- Create New Task ---")
        try:
            task_name = input("Enter Task Name: ").strip()
            task_name = cls.validate_task_name(task_name)
            
            chargeable_input = input("Is the task chargeable (Yes/No): ").strip()
            chargeable = cls.validate_chargeable(chargeable_input)
            
            rate_card = None
            if chargeable:
                rate_card_input = input("Enter Rate Card: ").strip()
                rate_card = cls.validate_rate_card(rate_card_input, chargeable)
            
            task = cls(task_name, chargeable, rate_card)
            task.save_task()
            print(f"\nTask created successfully!")
            print(f"Generated Task ID: {task.task_id}")
            return task
        except ValueError as e:
            print(f"Error: {e}")
            return None

    @classmethod
    def update_task(cls, task_id=None):
        if not task_id:
            task_id = input("Enter Task ID to update: ").strip()
        tasks = load_all_tasks()
        task_found = False
        updated_tasks = []

        for t in tasks:
            if t["task_id"].upper() == task_id.upper():
                task_found = True
                print(f"Task found: {t['task_name']} (Current Chargeable: {t['chargeable']}, Rate Card: {t['rate_card']})")
                try:
                    new_name = input("Enter new Task Name: ").strip()
                    new_name = cls.validate_task_name(new_name)
                    
                    new_chargeable_str = input("Is the task chargeable (Yes/No): ").strip()
                    new_chargeable = cls.validate_chargeable(new_chargeable_str)
                    
                    new_rate = 0.0
                    if new_chargeable:
                        new_rate_str = input("Enter new Rate Card: ").strip()
                        new_rate = cls.validate_rate_card(new_rate_str, new_chargeable)
                    
                    t["task_name"] = new_name
                    t["chargeable"] = new_chargeable
                    t["rate_card"] = new_rate
                    print("Task updated successfully.")
                except ValueError as e:
                    print(f"Update failed: {e}")
                    return False
            updated_tasks.append(t)

        if not task_found:
            print("Task ID is not found.")
            return False

        save_all_tasks(updated_tasks)
        return True

    @classmethod
    def delete_task(cls, task_id=None):
        if not task_id:
            task_id = input("Enter Task ID to delete: ").strip()
        tasks = load_all_tasks()
        task_found = False
        remaining_tasks = []

        for t in tasks:
            if t["task_id"].upper() == task_id.upper():
                task_found = True
            else:
                remaining_tasks.append(t)

        if task_found:
            save_all_tasks(remaining_tasks)
            print("Task deleted successfully.")
            return True
        else:
            print("Task ID is not found.")
            return False

    @classmethod
    def search_task(cls, task_id=None):
        if not task_id:
            task_id = input("Enter Task ID to search: ").strip()
        tasks = load_all_tasks()
        for t in tasks:
            if t["task_id"].upper() == task_id.upper():
                print("\n------------------------------")
                print(f"Task ID    : {t['task_id']}")
                print(f"Task Name  : {t['task_name']}")
                print(f"Chargeable : {t['chargeable']}")
                print(f"Rate Card  : {t['rate_card']}")
                print("------------------------------")
                return t
        print("Task ID is not found.")
        return None

    @classmethod
    def display_all_tasks(cls):
        tasks = load_all_tasks()
        if not tasks:
            print("no tasks are available in the system")
            return
        print("\nAvailable tasks:")
        print("--------------------------------------------------")
        for t in tasks:
            print(f"Task ID: {t['task_id']} | Name: {t['task_name']} | Chargeable: {t['chargeable']} | Rate: {t['rate_card']}")
        print("--------------------------------------------------")


def load_all_tasks(filename=TASKS_FILE):
    if not os.path.exists(filename):
        return []
    tasks = []
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
        if "task id" in data:
            task_id = data["task id"]
            task_name = data.get("task name", "")
            ch_val = data.get("chargeable", "False").lower() in ["true", "yes"]
            rc_str = data.get("rate card", "0.0")
            try:
                rc_val = float(rc_str)
            except ValueError:
                rc_val = 0.0
            tasks.append({
                "task_id": task_id,
                "task_name": task_name,
                "chargeable": ch_val,
                "rate_card": rc_val
            })
    return tasks


def save_all_tasks(tasks, filename=TASKS_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(f"Task ID: {t['task_id']}\n"
                    f"Task Name: {t['task_name']}\n"
                    f"Chargeable: {t['chargeable']}\n"
                    f"Rate Card: {t['rate_card']}\n"
                    f"------------------------------\n")


def create_tasks_from_csv(csv_path=TASKS_CSV, target_file=TASKS_FILE):
    """
    Reads tasks.csv and populates tasks.txt with Task instances.
    Avoids duplicate entries by checking existing task names.
    """
    if not os.path.exists(csv_path):
        print(f"File {csv_path} not found.")
        return 0

    existing_tasks = load_all_tasks(target_file)
    existing_names = {t["task_name"].lower() for t in existing_tasks}

    imported_count = 0
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            task_name = row.get("Task Name", "").strip()
            chargeable_raw = row.get("Chargeable", "No").strip()
            rate_raw = row.get("Rate Card", "0").replace('$', '').strip()

            if task_name and task_name.lower() not in existing_names:
                try:
                    task = Task(task_name=task_name, chargeable=chargeable_raw, rate_card=rate_raw)
                    task.save_task(target_file)
                    existing_names.add(task_name.lower())
                    imported_count += 1
                except ValueError as e:
                    print(f"Skipping task '{task_name}': {e}")

    print(f"Successfully imported {imported_count} tasks from tasks.csv.")
    return imported_count


# Module-level aliases to support both functional and OOP imports
read_tasks_csv = create_tasks_from_csv
update_task = Task.update_task
delete_task = Task.delete_task
search_task = Task.search_task
display_all_tasks = Task.display_all_tasks
