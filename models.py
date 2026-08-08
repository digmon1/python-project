from datetime import datetime
from file_handler import FileHandler
from validator import Validator
from operations import SystemOperations
class User:
    def __init__(self, name, emp_id, designation, age, address, salary, email, password):
        self.name = name
        self.emp_id = emp_id
        self.designation = designation
        self.age = int(age)
        self.address = address
        self.salary = int(salary)
        self.email = email
        self.password = password
    def view_profile(self):
        print("-" * 50)
        print("PROFILE")
        print("-" * 50)
        print(f"Name: {self.name}")
        print(f"ID: {self.emp_id}")
        print(f"Designation: {self.designation}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")
        print(f"Salary: {self.salary}")
        print(f"Email: {self.email}")
        print()
        return {
            "name": self.name,
            "emp_id": self.emp_id,
            "designation": self.designation,
            "age": self.age,
            "address": self.address,
            "salary": self.salary,
            "email": self.email
        }
    def update_address(self, file_name, new_address):
        new_address = new_address.strip()
        if not new_address:
            print("Address cannot be empty!\n")
            raise ValueError("Address cannot be empty!")
        if Validator.has_invalid_chars(new_address):
            print("Value cannot contain '|' or newline characters!\n")
            raise ValueError("Address cannot contain '|' or newline characters!")
        if not Validator.validate_address(new_address):
            print("Invalid Address!\n")
            raise ValueError("Invalid Address format!")
        success = FileHandler.update_record_field(file_name, self.email, 4, new_address)
        if success:
            self.address = new_address
            print("Profile Updated Successfully!\n")
            return True
        else:
            print("User not found!\n")
            raise ValueError("User not found in file!")

    def reset_password(self, file_name, new_pass=None):
        if new_pass is None:
            new_pass = input("Enter New Password: ").strip()
        new_pass = new_pass.strip()
        if not new_pass:
            print("Password cannot be empty!\n")
            raise ValueError("Password cannot be empty!")
        if Validator.has_invalid_chars(new_pass):
            print("Password cannot contain '|' or newline characters!\n")
            raise ValueError("Password cannot contain '|' or newline characters!")
        if not Validator.validate_password(new_pass):
            print("Password must be at least 6 characters!\n")
            raise ValueError("Password must be at least 6 characters!")
        success = FileHandler.update_record_field(file_name, self.email, 7, new_pass)
        if success:
            self.password = new_pass
            print("Password Updated Successfully!\n")
            return True
        else:
            print("User not found!\n")
            raise ValueError("User not found in file!")
    def show_menu(self):
        raise NotImplementedError("Subclasses must implement show_menu")
class Employee(User):
    FILE_NAME = "employee.txt"
    def give_suggestion(self, msg=None):
        if msg is None:
            msg = input("Enter your suggestion: ").strip()
        msg = msg.strip()
        if not msg:
            print("Suggestion cannot be empty!\n")
            raise ValueError("Suggestion cannot be empty!")
        elif Validator.has_invalid_chars(msg):
            print("Suggestion cannot contain '|' or newline characters!\n")
            raise ValueError("Suggestion cannot contain '|' or newline characters!")
        else:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            record = f"{self.name}|{self.emp_id}|{msg}|{timestamp}"
            FileHandler.append_record("suggestion.txt", record)
            print("Suggestion submitted successfully!\n")
            return True

    def give_enquiry(self, msg=None):
        if msg is None:
            msg = input("Enter your enquiry: ").strip()
        msg = msg.strip()
        if not msg:
            print("Enquiry cannot be empty!\n")
            raise ValueError("Enquiry cannot be empty!")
        elif Validator.has_invalid_chars(msg):
            print("Enquiry cannot contain '|' or newline characters!\n")
            raise ValueError("Enquiry cannot contain '|' or newline characters!")
        else:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            record = f"{self.name}|{self.emp_id}|{msg}|{timestamp}"
            FileHandler.append_record("enquiry.txt", record)
            print("Enquiry submitted successfully!\n")
            return True

    def show_menu(self):
        while True:
            print("=" * 50)
            print("\tEMPLOYEE MENU")
            print("=" * 50)
            print("1. View Profile")
            print("2. Edit Address")
            print("3. Reset Password")
            print("4. Give Suggestion")
            print("5. Give Enquiry")
            print("6. Logout")
            choice = input("Enter choice (1-6): ").strip()
            if choice == "1":
                self.view_profile()
            elif choice == "2":
                new_address = input("New Address: ").strip()
                try:
                    self.update_address(self.FILE_NAME, new_address)
                except ValueError:
                    pass
            elif choice == "3":
                try:
                    self.reset_password(self.FILE_NAME)
                except ValueError:
                    pass
            elif choice == "4":
                try:
                    self.give_suggestion()
                except ValueError:
                    pass
            elif choice == "5":
                try:
                    self.give_enquiry()
                except ValueError:
                    pass
            elif choice == "6":
                print("Logging out...\n")
                break
            else:
                print("Invalid Choice! Please enter from 1-6\n")
class Manager(User):
    FILE_NAME = "manager.txt"
    def show_menu(self):
        while True:
            print("=" * 50)
            print("\tMANAGER MENU")
            print("=" * 50)
            print("1. View Profile")
            print("2. Edit Address")
            print("3. Reset Password")
            print("4. Add Employee")
            print("5. View Employees")
            print("6. Search Employee")
            print("7. Delete Employee")
            print("8. View Suggestions")
            print("9. View Enquiries")
            print("10. Logout")
            choice = input("Enter choice (1-10): ").strip()
            if choice == "1":
                self.view_profile()
            elif choice == "2":
                new_address = input("New Address: ").strip()
                try:
                    self.update_address(self.FILE_NAME, new_address)
                except ValueError:
                    pass
            elif choice == "3":
                try:
                    self.reset_password(self.FILE_NAME)
                except ValueError:
                    pass
            elif choice == "4":
                SystemOperations.add_user(Employee.FILE_NAME, Validator.EMPLOYEE_MIN_SALARY, "employee")
            elif choice == "5":
                SystemOperations.view_all(Employee.FILE_NAME)
            elif choice == "6":
                SystemOperations.search_user(Employee.FILE_NAME)
            elif choice == "7":
                SystemOperations.delete_user(Employee.FILE_NAME)
            elif choice == "8":
                SystemOperations.view_all("suggestion.txt")
            elif choice == "9":
                SystemOperations.view_all("enquiry.txt")
            elif choice == "10":
                print("Logging out...\n")
                break
            else:
                print("Invalid Choice! Please enter from 1-10\n")
class Boss(User):
    FILE_NAME = "boss.txt"
    def show_menu(self):
        while True:
            print("=" * 50)
            print("\tBOSS MENU")
            print("=" * 50)
            print("1. View Profile")
            print("2. Edit Address")
            print("3. Reset Password")
            print("4. Add Manager")
            print("5. Add Employee")
            print("6. View Managers")
            print("7. View Employees")
            print("8. Search Managers")
            print("9. Search Employees")
            print("10. Delete Manager")
            print("11. Delete Employee")
            print("12. Logout")
            choice = input("Enter choice (1-12): ").strip()
            if choice == "1":
                self.view_profile()
            elif choice == "2":
                new_address = input("New Address: ").strip()
                try:
                    self.update_address(self.FILE_NAME, new_address)
                except ValueError:
                    pass
            elif choice == "3":
                try:
                    self.reset_password(self.FILE_NAME)
                except ValueError:
                    pass
            elif choice == "4":
                SystemOperations.add_user(Manager.FILE_NAME, Validator.MANAGER_MIN_SALARY, "manager")
            elif choice == "5":
                SystemOperations.add_user(Employee.FILE_NAME, Validator.EMPLOYEE_MIN_SALARY, "employee")
            elif choice == "6":
                SystemOperations.view_all(Manager.FILE_NAME)
            elif choice == "7":
                SystemOperations.view_all(Employee.FILE_NAME)
            elif choice == "8":
                SystemOperations.search_user(Manager.FILE_NAME)
            elif choice == "9":
                SystemOperations.search_user(Employee.FILE_NAME)
            elif choice == "10":
                SystemOperations.delete_user(Manager.FILE_NAME)
            elif choice == "11":
                SystemOperations.delete_user(Employee.FILE_NAME)
            elif choice == "12":
                print("Logging out...\n")
                break
            else:
                print("Invalid Choice! Please enter from 1-12\n")