import os
from file_handler import FileHandler
from validator import Validator
from models import Boss, Manager, Employee

class Authentication:
    BOSS_FILE = "boss.txt"
    MANAGER_FILE = "manager.txt"
    EMPLOYEE_FILE = "employee.txt"

    @staticmethod
    def register_boss():
        print("=" * 50)
        print("\tBOSS REGISTRATION")
        print("=" * 50)

        # Check if boss already exists (only one boss allowed)
        lines = FileHandler.read_records(Authentication.BOSS_FILE)
        if any(line.strip() for line in lines):
            print("Boss already registered!\n")
            return

        name = input("Name: ").strip()
        if Validator.has_invalid_chars(name):
            print("Name cannot contain '|' or newline characters!\n")
            return
        if not Validator.validate_name(name):
            print("Name cannot be empty or numbers only!\n")
            return

        emp_id = input("ID: ").strip()
        if Validator.has_invalid_chars(emp_id):
            print("ID cannot contain '|' or newline characters!\n")
            return
        if not Validator.validate_id(emp_id):
            print("ID cannot be empty!\n")
            return

        designation = "Boss"

        try:
            age = int(input("Age: "))
        except ValueError:
            print("Invalid age! Please enter a number.\n")
            return

        if not Validator.validate_age(age):
            print(f"Age must be at least {Validator.MIN_AGE}!\n")
            return

        address = input("Address: ").strip()
        if Validator.has_invalid_chars(address):
            print("Address cannot contain '|' or newline characters!\n")
            return
        if not Validator.validate_address(address):
            print("Invalid address! Enter a proper address.\n")
            return

        try:
            salary = int(input("Salary: "))
        except ValueError:
            print("Invalid salary! Please enter a number.\n")
            return

        if salary < 0:
            print("Salary cannot be negative!\n")
            return
        if not Validator.validate_salary(salary, Validator.BOSS_MIN_SALARY):
            print(f"Salary too low. At least {Validator.BOSS_MIN_SALARY:,} required.\n")
            return

        email = input("Email: ").strip()
        if not Validator.validate_email(email):
            print("Invalid email! Example: user@gmail.com\n")
            return
        email = email.lower()

        password = input("Password: ").strip()
        if Validator.has_invalid_chars(password):
            print("Password cannot contain '|' or newline characters!\n")
            return
        if not Validator.validate_password(password):
            print("Password must be at least 6 characters!\n")
            return

        record = f"{name}|{emp_id}|Boss|{age}|{address}|{salary}|{email}|{password}"
        FileHandler.append_record(Authentication.BOSS_FILE, record)
        print("Boss Registered Successfully!\n")

    @staticmethod
    def _attempt_login(file_name, header):
        """Shared logic for employee/manager login and boss login."""
        attempts = 0
        while attempts < 3:
            print("=" * 50)
            print(f"\t{header}")
            print("=" * 50)

            email = input("Enter Email: ").strip()
            password = input("Enter Password: ").strip()

            if not email or not password:
                attempts += 1
                print("Email and Password cannot be empty!")
                print(f"Attempts left: {3 - attempts}\n")
                continue

            if not Validator.validate_email(email):
                attempts += 1
                print("Invalid email format!")
                print(f"Attempts left: {3 - attempts}\n")
                continue

            email_lower = email.lower()
            lines = FileHandler.read_records(file_name)
            for line in lines:
                data = line.strip().split("|")
                if len(data) >= 8 and data[6].strip().lower() == email_lower and data[7] == password:
                    print("Login Successful!\n")
                    if file_name == Authentication.BOSS_FILE:
                        return Boss(*data[:8])
                    elif file_name == Authentication.MANAGER_FILE:
                        return Manager(*data[:8])
                    else:
                        return Employee(*data[:8])

            attempts += 1
            print(f"Invalid login! Attempts left: {3 - attempts}\n")

        print("Maximum attempts reached. System Terminated!")
        return None

    @staticmethod
    def login(file_name):
        lines = FileHandler.read_records(file_name)
        if not any(line.strip() for line in lines):
            print(f"No {file_name.replace('.txt', '')} registered yet!\n")
            return None
        return Authentication._attempt_login(file_name, "LOGIN")

    @staticmethod
    def boss_login():
        lines = FileHandler.read_records(Authentication.BOSS_FILE)
        if not any(line.strip() for line in lines):
            print("Boss does not exist! Please register first.\n")
            return None
        return Authentication._attempt_login(Authentication.BOSS_FILE, "BOSS LOGIN")