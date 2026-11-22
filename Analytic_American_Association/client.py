import os
import csv
import random
import re
from address import Address

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENTS_FILE = os.path.join(BASE_DIR, "clients.txt")
CLIENTS_CSV = os.path.join(BASE_DIR, "Clients.csv")

class Client(Address):
    """
    Client Management class, inheriting from Address.
    Attributes:
        client_id: Auto-generated 'CLT_<6digits random Number>'
        client_name: Alphanumeric, spaces, '-', '_'
        client_description: Alphanumeric, spaces, '-', '_', punctuation
        std_bill_rate: float/int
        client_address: Address object (or self)
        + Address fields inherited from Address
    """
    def __init__(self, client_name, client_description, std_bill_rate, client_address=None,
                 mail_id=None, phone_number=None, house_no=None, building_number=None,
                 road_number=None, street_name=None, land_mark=None, city=None, state=None, zip_code=None,
                 client_id=None):
        if client_address is not None and isinstance(client_address, Address):
            super().__init__(
                mail_id=client_address.mail_id,
                phone_number=client_address.phone_number,
                house_no=client_address.house_no,
                building_number=client_address.building_number,
                road_number=client_address.road_number,
                street_name=client_address.street_name,
                land_mark=client_address.land_mark,
                city=client_address.city,
                state=client_address.state,
                zip_code=client_address.zip_code,
                check_email_unique=False
            )
            self.client_address = client_address
        else:
            super().__init__(
                mail_id=mail_id,
                phone_number=phone_number,
                house_no=house_no,
                building_number=building_number,
                road_number=road_number,
                street_name=street_name,
                land_mark=land_mark,
                city=city,
                state=state,
                zip_code=zip_code
            )
            self.client_address = self

        self.client_id = client_id if client_id else self.generate_client_id()
        self.client_name = self.validate_client_name(client_name)
        self.client_description = self.validate_client_description(client_description)
        self.std_bill_rate = self.validate_std_bill_rate(std_bill_rate)

    @staticmethod
    def generate_client_id():
        existing_ids = {c["client_id"] for c in load_all_clients()}
        while True:
            new_id = f"CLT_{random.randint(100000, 999999)}"
            if new_id not in existing_ids:
                return new_id

    @staticmethod
    def validate_client_name(name):
        if not name or not str(name).strip():
            raise ValueError("Client name cannot be empty.")
        name = str(name).strip()
        pattern = r'^[A-Za-z0-9_\- ]+$'
        if not re.match(pattern, name):
            raise ValueError("Client name should consist of only upper/lower alphabets, digits, '-', '_', and spaces.")
        return name

    @staticmethod
    def validate_client_description(desc):
        if not desc or not str(desc).strip():
            raise ValueError("Client description cannot be empty.")
        desc = str(desc).strip()
        pattern = r'^[A-Za-z0-9_\- .,\'\"/]+$'
        if not re.match(pattern, desc):
            raise ValueError("Client description contains invalid characters.")
        return desc

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

    def save_client(self, filename=CLIENTS_FILE):
        with open(filename, "a", encoding="utf-8") as f:
            f.write(
                f"Client ID: {self.client_id}\n"
                f"Client Name: {self.client_name}\n"
                f"Client Description: {self.client_description}\n"
                f"Standard Bill Rate: {self.std_bill_rate}\n"
                f"Mail ID: {self.mail_id}\n"
                f"Phone Number: {self.phone_number}\n"
                f"House Number: {self.house_no}\n"
                f"Building Number: {self.building_number}\n"
                f"Road Number: {self.road_number}\n"
                f"Street Name: {self.street_name}\n"
                f"Landmark: {self.land_mark}\n"
                f"City: {self.city}\n"
                f"State: {self.state}\n"
                f"Zip Code: {self.zip_code}\n"
                "------------------------------\n"
            )

    @classmethod
    def create_client_interactive(cls):
        print("\n--- Create New Client ---")
        try:
            name = input("Enter Client Name: ").strip()
            name = cls.validate_client_name(name)

            desc = input("Enter Client Description: ").strip()
            desc = cls.validate_client_description(desc)

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

            client = cls(name, desc, rate, client_address=address)
            client.save_client()
            print("\nClient created successfully!")
            print(f"Generated Client ID: {client.client_id}")
            return client
        except ValueError as e:
            print(f"Error creating client: {e}")
            return None

    @classmethod
    def update_client(cls, client_id=None):
        if not client_id:
            client_id = input("Enter Client ID to update: ").strip()
        clients = load_all_clients()
        client_found = False
        updated_clients = []

        for c in clients:
            if c["client_id"].upper() == client_id.upper():
                client_found = True
                print(f"Client found: {c['client_name']} (Current Rate: {c['std_bill_rate']})")
                try:
                    new_desc = input(f"Enter new Description [{c['client_description']}]: ").strip() or c['client_description']
                    new_desc = cls.validate_client_description(new_desc)

                    new_rate_str = input(f"Enter new Standard Bill Rate [{c['std_bill_rate']}]: ").strip() or str(c['std_bill_rate'])
                    new_rate = cls.validate_std_bill_rate(new_rate_str)

                    print("\nUpdate Address Details (leave blank to keep current):")
                    old_mail = c["mail_id"]
                    mail_in = input(f"Mail ID [{old_mail}]: ").strip() or old_mail
                    phone_in = input(f"Phone Number [{c['phone_number']}]: ").strip() or c['phone_number']
                    house_in = input(f"House Number [{c['house_no']}]: ").strip() or c['house_no']
                    bldg_in = input(f"Building Number [{c['building_number']}]: ").strip() or c['building_number']
                    road_in = input(f"Road Number [{c['road_number']}]: ").strip() or c['road_number']
                    street_in = input(f"Street Name [{c['street_name']}]: ").strip() or c['street_name']
                    landmark_in = input(f"Landmark [{c['land_mark']}]: ").strip() or c['land_mark']
                    city_in = input(f"City [{c['city']}]: ").strip() or c['city']
                    state_in = input(f"State [{c['state']}]: ").strip() or c['state']
                    zip_in = input(f"Zip Code [{c['zip_code']}]: ").strip() or c['zip_code']

                    new_address = Address(mail_in, phone_in, house_in, bldg_in, road_in,
                                          street_in, landmark_in, city_in, state_in, zip_in,
                                          current_email=old_mail)

                    c["client_description"] = new_desc
                    c["std_bill_rate"] = new_rate
                    c["mail_id"] = new_address.mail_id
                    c["phone_number"] = new_address.phone_number
                    c["house_no"] = new_address.house_no
                    c["building_number"] = new_address.building_number
                    c["road_number"] = new_address.road_number
                    c["street_name"] = new_address.street_name
                    c["land_mark"] = new_address.land_mark
                    c["city"] = new_address.city
                    c["state"] = new_address.state
                    c["zip_code"] = new_address.zip_code

                    print("Client updated successfully.")
                except ValueError as e:
                    print(f"Update failed: {e}")
                    return False
            updated_clients.append(c)

        if not client_found:
            print("Client ID is not found.")
            return False

        save_all_clients(updated_clients)
        return True

    @classmethod
    def delete_client(cls, client_id=None):
        if not client_id:
            client_id = input("Enter Client ID to delete: ").strip()
        clients = load_all_clients()
        client_found = False
        remaining = []

        for c in clients:
            if c["client_id"].upper() == client_id.upper():
                client_found = True
                Address.remove_email(c["mail_id"])
            else:
                remaining.append(c)

        if client_found:
            save_all_clients(remaining)
            print("Client deleted successfully.")
            return True
        else:
            print("Client ID is not found.")
            return False

    @classmethod
    def search_client(cls, client_id=None):
        if not client_id:
            client_id = input("Enter Client ID to search: ").strip()
        clients = load_all_clients()
        for c in clients:
            if c["client_id"].upper() == client_id.upper():
                print("\n------------------------------")
                print(f"Client ID          : {c['client_id']}")
                print(f"Client Name        : {c['client_name']}")
                print(f"Client Description : {c['client_description']}")
                print(f"Standard Bill Rate : {c['std_bill_rate']}")
                print(f"Mail ID            : {c['mail_id']}")
                print(f"Phone Number       : {c['phone_number']}")
                print(f"House Number       : {c['house_no']}")
                print(f"Building Number    : {c['building_number']}")
                print(f"Road Number        : {c['road_number']}")
                print(f"Street Name        : {c['street_name']}")
                print(f"Landmark           : {c['land_mark']}")
                print(f"City               : {c['city']}")
                print(f"State              : {c['state']}")
                print(f"Zip Code           : {c['zip_code']}")
                print("------------------------------")
                return c
        print("Client ID is not found.")
        return None

    @classmethod
    def display_all_clients(cls):
        clients = load_all_clients()
        if not clients:
            print("no clients are available in the system")
            return
        print("\nAvailable Clients:")
        print("--------------------------------------------------------------------------------")
        for c in clients:
            print(f"ID: {c['client_id']} | Name: {c['client_name']} | Rate: {c['std_bill_rate']} | "
                  f"City: {c['city']} | Phone: {c['phone_number']}")
        print("--------------------------------------------------------------------------------")


def load_all_clients(filename=CLIENTS_FILE):
    if not os.path.exists(filename):
        return []
    clients = []
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
        if "client id" in data:
            c_id = data["client id"]
            c_name = data.get("client name", "")
            desc = data.get("client description", "")
            rate_str = data.get("standard bill rate", data.get("standard rate bill", data.get("bill rate", "0.0")))
            try:
                rate_val = float(rate_str.replace('$', ''))
            except ValueError:
                rate_val = 0.0

            mail_id = data.get("mail id", "")
            Address.register_email(mail_id)

            clients.append({
                "client_id": c_id,
                "client_name": c_name,
                "client_description": desc,
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
    return clients


def save_all_clients(clients, filename=CLIENTS_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        for c in clients:
            f.write(
                f"Client ID: {c['client_id']}\n"
                f"Client Name: {c['client_name']}\n"
                f"Client Description: {c['client_description']}\n"
                f"Standard Bill Rate: {c['std_bill_rate']}\n"
                f"Mail ID: {c['mail_id']}\n"
                f"Phone Number: {c['phone_number']}\n"
                f"House Number: {c['house_no']}\n"
                f"Building Number: {c['building_number']}\n"
                f"Road Number: {c['road_number']}\n"
                f"Street Name: {c['street_name']}\n"
                f"Landmark: {c['land_mark']}\n"
                f"City: {c['city']}\n"
                f"State: {c['state']}\n"
                f"Zip Code: {c['zip_code']}\n"
                "------------------------------\n"
            )


def read_clients_csv(csv_path=CLIENTS_CSV, target_file=CLIENTS_FILE):
    """
    Reads Clients.csv and imports clients into clients.txt.
    """
    if not os.path.exists(csv_path):
        print(f"CSV file '{csv_path}' not found.")
        return 0

    existing_clients = load_all_clients(target_file)
    existing_emails = {c["mail_id"].lower() for c in existing_clients}

    imported_count = 0
    with open(csv_path, "r", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            c_name = row.get("Client Name", "").strip()
            mail_id = row.get("Mail Id", "").strip()
            phone = row.get("Phone Number", "").strip()
            bill_rate_raw = row.get("Standart Bill Rate", row.get("Standard Bill Rate", "0")).replace('$', '').strip()
            desc = row.get("Descrioption", row.get("Description", "")).strip()
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
                    client = Client(c_name, desc, bill_rate_raw, client_address=address)
                    client.save_client(target_file)
                    existing_emails.add(mail_id.lower())
                    Address.register_email(mail_id)
                    imported_count += 1
                except ValueError as e:
                    print(f"Skipping client '{c_name}': {e}")

    print(f"Successfully imported {imported_count} clients from CSV.")
    return imported_count


# Module-level aliases
update_client = Client.update_client
delete_client = Client.delete_client
search_client = Client.search_client
display_all_clients = Client.display_all_clients
