import os
import csv
import random
import re
from address import Address

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMPLOYEES_FILE = os.path.join(BASE_DIR, "employees.txt")
EMPLOYEES_CSV = os.path.join(BASE_DIR, "Employee.csv")

class Employee:
    """
    Employee (Lawyer) Management class.
    Attributes:
        employee_id: Auto-generated 'EMP_<6digits random Number>'
        employee_name: Alphanumeric, spaces, '-', '_'
        std_bill_rate: float/int
        employee_address: Address object
    """
    def __init__(self, employee_name, std_bill_rate, employee_address, employee_id=None):
        self.employee_id = employee_id if employee_id else self.generate_employee_id()
        self.employee_name = self.validate_employee_name(employee_name)
        self.std_bill_rate = self.validate_std_bill_rate(std_bill_rate)
        if not isinstance(employee_address, Address):
            raise ValueError("employee_address must be an instance of Address class.")
        self.employee_address = employee_address

    @staticmethod
    def generate_employee_id():
        existing_ids = {e["employee_id"] for e in load_all_employees()}
        while True:
            new_id = f"EMP_{random.randint(100000, 999999)}"
            if new_id not in existing_ids:
                return new_id

    @staticmethod
    def validate_employee_name(name):
        if not name or not str(name).strip():
            raise ValueError("Employee name cannot be empty.")
        name = str(name).strip()
        pattern = r'^[A-Za-z0-9_\- ]+$'
        if not re.match(pattern, name):
            raise ValueError("Employee name should consist of only upper/lower alphabets, digits, '-', '_', and spaces.")
        return name

    @staticmethod
    def validate_std_bill_rate(rate):
        if rate is None or str(rate).strip() == "":
            raise ValueError("Standard bill rate cannot be empty.")
        try:
            val = float(str(rate).replace('$', '').strip())
            if val < 0:
                raise ValueError("Standard bill rate cannot be negative.")
            return val
        except ValueError:
            raise ValueError("Standard bill rate must be an integer or float number.")

    def save_employee(self, filename=EMPLOYEES_FILE):
        with open(filename, "a", encoding="utf-8") as f:
            f.write(
                f"Employee ID: {self.employee_id}\n"
                f"Employee Name: {self.employee_name}\n"
                f"Standard Bill Rate: {self.std_bill_rate}\n"
                f"Mail ID: {self.employee_address.mail_id}\n"
                f"Phone Number: {self.employee_address.phone_number}\n"
                f"House Number: {self.employee_address.house_no}\n"
                f"Building Number: {self.employee_address.building_number}\n"
                f"Road Number: {self.employee_address.road_number}\n"
                f"Street Name: {self.employee_address.street_name}\n"
                f"Landmark: {self.employee_address.land_mark}\n"
                f"City: {self.employee_address.city}\n"
                f"State: {self.employee_address.state}\n"
                f"Zip Code: {self.employee_address.zip_code}\n"
                "------------------------------\n"
            )

    @classmethod
    def create_employee_interactive(cls):
        print("\n--- Create New Employee ---")
        try:
            name = input("Enter Employee Name: ").strip()
            name = cls.validate_employee_name(name)
            
            rate = input("Enter Standard Bill Rate: ").strip()
            rate = cls.validate_std_bill_rate(rate)

            print("\nEnter Address Details:")
            mail_id = input("Mail ID: ").strip()
            phone_number = input("Phone Number: ").strip()
            house_no = input("House Number: ").strip()
            building_number = input("Building Number: ").strip()
            road_number = input("Road Number: ").strip()
            street_name = input("Street Name: ").strip()
            landmark = input("Landmark: ").strip()
            city = input("City: ").strip()
            state = input("State: ").strip()
            zip_code = input("Zip Code: ").strip()

            address = Address(mail_id, phone_number, house_no, building_number, road_number,
                              street_name, landmark, city, state, zip_code)
            
            emp = cls(name, rate, address)
            emp.save_employee()
            print("\nEmployee created successfully!")
            print(f"Generated Employee ID: {emp.employee_id}")
            return emp
        except ValueError as e:
            print(f"Error creating employee: {e}")
            return None

    @classmethod
    def update_employee(cls, employee_id=None):
        if not employee_id:
            employee_id = input("Enter Employee ID to update: ").strip()
        employees = load_all_employees()
        emp_found = False
        updated_employees = []

        for emp in employees:
            if emp["employee_id"].upper() == employee_id.upper():
                emp_found = True
                print(f"Employee found: {emp['employee_name']} (Current Rate: {emp['std_bill_rate']})")
                try:
                    new_rate_str = input("Enter new Standard Bill Rate: ").strip()
                    new_rate = cls.validate_std_bill_rate(new_rate_str)

                    print("\nUpdate Address Details (leave blank to keep current):")
                    old_mail = emp["mail_id"]
                    mail_in = input(f"Mail ID [{old_mail}]: ").strip() or old_mail
                    phone_in = input(f"Phone Number [{emp['phone_number']}]: ").strip() or emp['phone_number']
                    house_in = input(f"House Number [{emp['house_no']}]: ").strip() or emp['house_no']
                    bldg_in = input(f"Building Number [{emp['building_number']}]: ").strip() or emp['building_number']
                    road_in = input(f"Road Number [{emp['road_number']}]: ").strip() or emp['road_number']
                    street_in = input(f"Street Name [{emp['street_name']}]: ").strip() or emp['street_name']
                    landmark_in = input(f"Landmark [{emp['land_mark']}]: ").strip() or emp['land_mark']
                    city_in = input(f"City [{emp['city']}]: ").strip() or emp['city']
                    state_in = input(f"State [{emp['state']}]: ").strip() or emp['state']
                    zip_in = input(f"Zip Code [{emp['zip_code']}]: ").strip() or emp['zip_code']

                    # Validate new address with current_email so keeping same email passes
                    new_address = Address(mail_in, phone_in, house_in, bldg_in, road_in,
                                          street_in, landmark_in, city_in, state_in, zip_in,
                                          current_email=old_mail)
                    
                    emp["std_bill_rate"] = new_rate
                    emp["mail_id"] = new_address.mail_id
                    emp["phone_number"] = new_address.phone_number
                    emp["house_no"] = new_address.house_no
                    emp["building_number"] = new_address.building_number
                    emp["road_number"] = new_address.road_number
                    emp["street_name"] = new_address.street_name
                    emp["land_mark"] = new_address.land_mark
                    emp["city"] = new_address.city
                    emp["state"] = new_address.state
                    emp["zip_code"] = new_address.zip_code

                    print("Employee updated successfully.")
                except ValueError as e:
                    print(f"Update failed: {e}")
                    return False
            updated_employees.append(emp)

        if not emp_found:
            print("Employee ID is not found.")
            return False

        save_all_employees(updated_employees)
        return True

    @classmethod
    def delete_employee(cls, employee_id=None):
        if not employee_id:
            employee_id = input("Enter Employee ID to delete: ").strip()
        employees = load_all_employees()
        emp_found = False
        remaining = []

        for emp in employees:
            if emp["employee_id"].upper() == employee_id.upper():
                emp_found = True
                Address.remove_email(emp["mail_id"])
            else:
                remaining.append(emp)

        if emp_found:
            save_all_employees(remaining)
            print("Employee deleted successfully.")
            return True
        else:
            print("Employee ID is not found.")
            return False

    @classmethod
    def search_employee(cls, employee_id=None):
        if not employee_id:
            employee_id = input("Enter Employee ID to search: ").strip()
        employees = load_all_employees()
        for emp in employees:
            if emp["employee_id"].upper() == employee_id.upper():
                print("\n------------------------------")
                print(f"Employee ID        : {emp['employee_id']}")
                print(f"Employee Name      : {emp['employee_name']}")
                print(f"Standard Bill Rate : {emp['std_bill_rate']}")
                print(f"Mail ID            : {emp['mail_id']}")
                print(f"Phone Number       : {emp['phone_number']}")
                print(f"House Number       : {emp['house_no']}")
                print(f"Building Number    : {emp['building_number']}")
                print(f"Road Number        : {emp['road_number']}")
                print(f"Street Name        : {emp['street_name']}")
                print(f"Landmark           : {emp['land_mark']}")
                print(f"City               : {emp['city']}")
                print(f"State              : {emp['state']}")
                print(f"Zip Code           : {emp['zip_code']}")
                print("------------------------------")
                return emp
        print("Employee ID is not found.")
        return None

    @classmethod
    def display_all_employees(cls):
        employees = load_all_employees()
        if not employees:
            print("no employees are available in the system")
            return
        print("\nAvailable Employees:")
        print("--------------------------------------------------------------------------------")
        for emp in employees:
            print(f"ID: {emp['employee_id']} | Name: {emp['employee_name']} | Rate: {emp['std_bill_rate']} | "
                  f"City: {emp['city']} | Phone: {emp['phone_number']}")
        print("--------------------------------------------------------------------------------")


def load_all_employees(filename=EMPLOYEES_FILE):
    if not os.path.exists(filename):
        return []
    employees = []
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
        if "employee id" in data:
            emp_id = data["employee id"]
            emp_name = data.get("employee name", "")
            rate_str = data.get("standard bill rate", data.get("bill rate", "0.0"))
            try:
                rate_val = float(rate_str.replace('$', ''))
            except ValueError:
                rate_val = 0.0
            
            mail_id = data.get("mail id", "")
            Address.register_email(mail_id)

            employees.append({
                "employee_id": emp_id,
                "employee_name": emp_name,
                "std_bill_rate": rate_val,
                "mail_id": mail_id,
                "phone_number": data.get("phone number", ""),
                "house_no": data.get("house number", ""),
                "building_number": data.get("building number", ""),
                "road_number": data.get("road number", ""),
                "street_name": data.get("street name", ""),
                "land_mark": data.get("landmark", ""),
                "city": data.get("city", ""),
                "state": data.get("state", ""),
                "zip_code": data.get("zip code", "")
            })
    return employees


def save_all_employees(employees, filename=EMPLOYEES_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        for emp in employees:
            f.write(
                f"Employee ID: {emp['employee_id']}\n"
                f"Employee Name: {emp['employee_name']}\n"
                f"Standard Bill Rate: {emp['std_bill_rate']}\n"
                f"Mail ID: {emp['mail_id']}\n"
                f"Phone Number: {emp['phone_number']}\n"
                f"House Number: {emp['house_no']}\n"
                f"Building Number: {emp['building_number']}\n"
                f"Road Number: {emp['road_number']}\n"
                f"Street Name: {emp['street_name']}\n"
                f"Landmark: {emp['land_mark']}\n"
                f"City: {emp['city']}\n"
                f"State: {emp['state']}\n"
                f"Zip Code: {emp['zip_code']}\n"
                "------------------------------\n"
            )


def read_employee_csv(csv_path=EMPLOYEES_CSV, target_file=EMPLOYEES_FILE):
    """
    Reads Employee.csv and imports employees into employees.txt.
    """
    if not os.path.exists(csv_path):
        alt_path = os.path.join(BASE_DIR, "Employees.csv")
        if os.path.exists(alt_path):
            csv_path = alt_path
        else:
            print(f"CSV file '{csv_path}' not found.")
            return 0

    existing_employees = load_all_employees(target_file)
    existing_emails = {e["mail_id"].lower() for e in existing_employees}

    imported_count = 0
    # Use latin-1 or utf-8 with replace to handle accented characters like Café
    with open(csv_path, "r", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp_name = row.get("Employee Name", "").strip()
            mail_id = row.get("Mail Id", "").strip()
            phone = row.get("Phone Number", "").strip()
            bill_rate_raw = row.get("Standart Bill Rate", row.get("Standard Bill Rate", "0")).replace('$', '').strip()
            house_no = row.get("House Number", "").strip()
            bldg_no = row.get("Building Number", "").strip()
            road_no = row.get("Road Number", "").strip()
            street = row.get("Steet Name", row.get("Street Name", "")).strip()
            landmark = row.get("Landmark", "").strip()
            city = row.get("City", "").strip()
            state = row.get("State", "").strip()
            zip_code = row.get("Zip Code", "").strip()

            if mail_id and mail_id.lower() not in existing_emails:
                try:
                    address = Address(mail_id, phone, house_no, bldg_no, road_no,
                                      street, landmark, city, state, zip_code, check_email_unique=False)
                    emp = Employee(emp_name, bill_rate_raw, address)
                    emp.save_employee(target_file)
                    existing_emails.add(mail_id.lower())
                    Address.register_email(mail_id)
                    imported_count += 1
                except ValueError as e:
                    print(f"Skipping employee '{emp_name}': {e}")

    print(f"Successfully imported {imported_count} employees from CSV.")
    return imported_count


# Module-level aliases
update_employee = Employee.update_employee
delete_employee = Employee.delete_employee
search_employee = Employee.search_employee
display_all_employees = Employee.display_all_employees
