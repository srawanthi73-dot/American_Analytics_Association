import re

class Address:
    """
    Address class to represent and validate address details for Employees and Clients.
    Attributes:
        mail_id, phone_number, house_no, building_number, road_number,
        street_name, land_mark, city, state, zip_code
    """
    email_list = set()

    def __init__(self, mail_id, phone_number, house_no, building_number, road_number,
                 street_name, land_mark, city, state, zip_code, check_email_unique=True, current_email=None):
        self.mail_id = self.validate_mail_id(mail_id, current_email=current_email, check_unique=check_email_unique)
        self.phone_number = self.validate_phone_number(phone_number)
        self.house_no = self.validate_house_no(house_no)
        self.building_number = self.validate_building_number(building_number)
        self.road_number = self.validate_road_number(road_number)
        self.street_name = self.validate_street_name(street_name)
        self.land_mark = self.validate_land_mark(land_mark)
        self.city = self.validate_city(city)
        self.state = self.validate_state(state)
        self.zip_code = self.validate_zip_code(zip_code)

    @classmethod
    def register_email(cls, mail_id):
        if mail_id and isinstance(mail_id, str):
            cls.email_list.add(mail_id.strip().lower())

    @classmethod
    def remove_email(cls, mail_id):
        if mail_id and isinstance(mail_id, str):
            cls.email_list.discard(mail_id.strip().lower())

    @classmethod
    def validate_mail_id(cls, mail_id, current_email=None, check_unique=True):
        if not mail_id or not isinstance(mail_id, str):
            raise ValueError("Email ID cannot be empty.")
        mail_id = mail_id.strip()
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, mail_id):
            raise ValueError("Invalid email format. Allowed characters: alphabets, digits, _, -, ., @.")
        
        norm_email = mail_id.lower()
        norm_current = current_email.strip().lower() if current_email else None
        
        if check_unique:
            if norm_email in cls.email_list and norm_email != norm_current:
                raise ValueError(f"Email ID '{mail_id}' already exists in the system.")
            cls.email_list.add(norm_email)
        return mail_id

    @staticmethod
    def validate_phone_number(phone_number):
        if not phone_number:
            raise ValueError("Phone number cannot be empty.")
        phone_number = str(phone_number).strip()
        pattern = r'^(\+91)?[0-9]{10}$'
        if not re.match(pattern, phone_number):
            raise ValueError("Phone number must have 10 digits or 10 digits with +91 prefix.")
        return phone_number

    @staticmethod
    def validate_house_no(house_no):
        if not house_no or not str(house_no).strip():
            raise ValueError("House number cannot be empty.")
        return str(house_no).strip()

    @staticmethod
    def validate_building_number(building_number):
        if not building_number or not str(building_number).strip():
            raise ValueError("Building number cannot be empty.")
        return str(building_number).strip()

    @staticmethod
    def validate_road_number(road_number):
        if not road_number or not str(road_number).strip():
            raise ValueError("Road number cannot be empty.")
        return str(road_number).strip()

    @staticmethod
    def validate_street_name(street_name):
        if not street_name or not str(street_name).strip():
            raise ValueError("Street name cannot be empty.")
        street_name = str(street_name).strip()
        pattern = r'^[A-Za-z0-9\s_\-./,]+$'
        if not re.match(pattern, street_name):
            raise ValueError("Street name should contain alphanumeric characters, spaces or valid symbols.")
        return street_name

    @staticmethod
    def validate_land_mark(land_mark):
        if not land_mark or not str(land_mark).strip():
            raise ValueError("Landmark cannot be empty.")
        return str(land_mark).strip()

    @staticmethod
    def validate_city(city):
        if not city or not str(city).strip():
            raise ValueError("City cannot be empty.")
        city = str(city).strip()
        pattern = r'^[A-Za-z\s]+$'
        if not re.match(pattern, city):
            raise ValueError("City name should contain only alphabets and spaces.")
        return city

    @staticmethod
    def validate_state(state):
        if not state or not str(state).strip():
            raise ValueError("State cannot be empty.")
        state = str(state).strip()
        pattern = r'^[A-Za-z\s]+$'
        if not re.match(pattern, state):
            raise ValueError("State name should contain only alphabets and spaces.")
        return state

    @staticmethod
    def validate_zip_code(zip_code):
        if not zip_code or not str(zip_code).strip():
            raise ValueError("Zip code cannot be empty.")
        zip_str = str(zip_code).strip()
        if not zip_str.isdigit():
            raise ValueError("Zip code should contain only integer numbers.")
        return zip_str

    def display_address(self):
        print(f"Mail ID         : {self.mail_id}")
        print(f"Phone Number    : {self.phone_number}")
        print(f"House Number    : {self.house_no}")
        print(f"Building Number : {self.building_number}")
        print(f"Road Number     : {self.road_number}")
        print(f"Street Name     : {self.street_name}")
        print(f"Landmark        : {self.land_mark}")
        print(f"City            : {self.city}")
        print(f"State           : {self.state}")
        print(f"Zip Code        : {self.zip_code}")

    def __str__(self):
        return (f"{self.house_no}, Bldg {self.building_number}, Rd {self.road_number}, "
                f"{self.street_name}, Near {self.land_mark}, {self.city}, {self.state} - {self.zip_code} "
                f"(Email: {self.mail_id}, Phone: {self.phone_number})")
