import os
from file_handler import FileHandler
from validator import Validator

class SystemOperations:
    @staticmethod
    def add_user(file_name, min_salary, user_type, name=None, emp_id=None, designation=None, age_str=None, address=None, salary_str=None, email=None, password=None):
        if name is None:
            # CLI mode
            print("-" * 50)
            print(f"ADD {user_type.upper()}")
            print("-" * 50)
            
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
            if Validator.check_duplicate_id(file_name, emp_id):
                print(f"A {user_type} with this ID already exists!\n")
                return

            designation = input("Designation: ").strip()
            if Validator.has_invalid_chars(designation):
                print("Designation cannot contain '|' or newline characters!\n")
                return
            if not Validator.validate_designation(designation):
                print("Designation cannot be empty!\n")
                return

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
            if not Validator.validate_salary(salary, min_salary):
                label = " for manager" if user_type.lower() == "manager" else ""
                print(f"Salary too low. At least {min_salary:,} required{label}.\n")
                return

            email = input("Email: ").strip()
            if not Validator.validate_email(email):
                print("Invalid email! Example: user@gmail.com\n")
                return
            email = email.lower()
            if Validator.check_duplicate_email(file_name, email):
                print("Email already exists!\n")
                return

            password = input("Password: ").strip()
            if Validator.has_invalid_chars(password):
                print("Password cannot contain '|' or newline characters!\n")
                return
            if not Validator.validate_password(password):
                print("Password must be at least 6 characters!\n")
                return

            record = f"{name}|{emp_id}|{designation}|{age}|{address}|{salary}|{email}|{password}"
            FileHandler.append_record(file_name, record)
            print(f"{user_type.capitalize()} Added Successfully!\n")
            return True
        else:
            # GUI mode (parameters passed)
            name = name.strip()
            if Validator.has_invalid_chars(name):
                raise ValueError("Name cannot contain '|' or newline characters!")
            if not Validator.validate_name(name):
                raise ValueError("Name cannot be empty or numbers only!")

            emp_id = emp_id.strip()
            if Validator.has_invalid_chars(emp_id):
                raise ValueError("ID cannot contain '|' or newline characters!")
            if not Validator.validate_id(emp_id):
                raise ValueError("ID cannot be empty!")
            if Validator.check_duplicate_id(file_name, emp_id):
                raise ValueError(f"A {user_type} with this ID already exists!")

            designation = designation.strip()
            if Validator.has_invalid_chars(designation):
                raise ValueError("Designation cannot contain '|' or newline characters!")
            if not Validator.validate_designation(designation):
                raise ValueError("Designation cannot be empty!")

            try:
                age = int(age_str)
            except ValueError:
                raise ValueError("Invalid age! Please enter a number.")
            if not Validator.validate_age(age):
                raise ValueError(f"Age must be at least {Validator.MIN_AGE}!")

            address = address.strip()
            if Validator.has_invalid_chars(address):
                raise ValueError("Address cannot contain '|' or newline characters!")
            if not Validator.validate_address(address):
                raise ValueError("Invalid address! Enter a proper address.")

            try:
                salary = int(salary_str)
            except ValueError:
                raise ValueError("Invalid salary! Please enter a number.")
            if salary < 0:
                raise ValueError("Salary cannot be negative!")
            if not Validator.validate_salary(salary, min_salary):
                label = " for manager" if user_type.lower() == "manager" else ""
                raise ValueError(f"Salary too low. At least {min_salary:,} required{label}.")

            email = email.strip()
            if not Validator.validate_email(email):
                raise ValueError("Invalid email format! Example: user@gmail.com")
            email = email.lower()
            if Validator.check_duplicate_email(file_name, email):
                raise ValueError("Email already exists!")

            password = password.strip()
            if Validator.has_invalid_chars(password):
                raise ValueError("Password cannot contain '|' or newline characters!")
            if not Validator.validate_password(password):
                raise ValueError("Password must be at least 6 characters!")

            record = f"{name}|{emp_id}|{designation}|{age}|{address}|{salary}|{email}|{password}"
            FileHandler.append_record(file_name, record)
            return True

    @staticmethod
    def view_all(file_name):
        print("-" * 50)
        print(f"CONTENTS OF {file_name}")
        print("-" * 50)
        if not os.path.exists(file_name):
            print("File does not exist!\n")
            return
        lines = FileHandler.read_records(file_name)
        content = "".join(lines).strip()
        if content:
            print(content)
        else:
            print("No records found.")
        print()

    @staticmethod
    def get_all_users(file_name):
        """Reads file and returns structured list of user lists."""
        lines = FileHandler.read_records(file_name)
        users = []
        for line in lines:
            data = line.strip().split("|")
            if len(data) >= 8:
                users.append(data[:8])
        return users

    @staticmethod
    def search_user(file_name):
        keyword = input("Enter Name/ID/Email to search: ").strip()
        if not keyword:
            print("Search keyword cannot be empty!\n")
            return
        
        print("-" * 50)
        print(f"SEARCH RESULTS IN {file_name}")
        print("-" * 50)
        if not os.path.exists(file_name):
            print("File does not exist!\n")
            return
        
        results = SystemOperations.search_users(file_name, keyword)
        if results:
            for user in results:
                print("|".join(user))
        else:
            print(f"No matching records found in {file_name}.")
        print()

    @staticmethod
    def search_users(file_name, keyword):
        """Filters users in the file by keyword (name, ID, or email)."""
        keyword_lower = keyword.strip().lower()
        if not keyword_lower:
            return SystemOperations.get_all_users(file_name)
        
        all_users = SystemOperations.get_all_users(file_name)
        results = []
        for user in all_users:
            name, id_val, email = user[0], user[1], user[6]
            if (keyword_lower in name.lower()
                    or keyword_lower in id_val.lower()
                    or keyword_lower in email.lower()):
                results.append(user)
        return results

    @staticmethod
    def delete_user(file_name):
        keyword = input("Enter exact Name/ID/Email to delete: ").strip()
        if not keyword:
            print("Delete keyword cannot be empty!\n")
            return
        if not os.path.exists(file_name):
            print("File does not exist!\n")
            return
        
        lines = FileHandler.read_records(file_name)
        keyword_lower = keyword.lower()
        matches = []
        for i, line in enumerate(lines):
            data = line.strip().split("|")
            if len(data) < 8:
                continue
            if (data[1] == keyword
                    or data[6].lower() == keyword_lower
                    or data[0].lower() == keyword_lower):
                matches.append((i, data))
        
        if not matches:
            print(f"No exact matching record found in {file_name} to delete.\n")
            return
        
        lines_to_remove = set()
        for i, data in matches:
            print("-" * 50)
            print(f"Name: {data[0]} | ID: {data[1]} | Designation: {data[2]} | Email: {data[6]}")
            confirm = input("Delete this record? (Y/N): ").strip().lower()
            if confirm == "y":
                lines_to_remove.add(i)
            elif confirm == "n":
                continue
            else:
                print("Invalid input. Skipping this record (not deleted).")
        
        if not lines_to_remove:
            print("No records were deleted.\n")
            return
        
        new_lines = [line for idx, line in enumerate(lines) if idx not in lines_to_remove]
        FileHandler.write_records(file_name, new_lines)
        print(f"{len(lines_to_remove)} record(s) deleted successfully!\n")

    @staticmethod
    def delete_user_by_id(file_name, emp_id):
        """Deletes user with the specific employee ID. Returns True if deleted."""
        lines = FileHandler.read_records(file_name)
        new_lines = []
        deleted = False
        for line in lines:
            data = line.strip().split("|")
            if len(data) >= 8 and data[1].strip() == emp_id.strip():
                deleted = True
            else:
                new_lines.append(line)
        if deleted:
            FileHandler.write_records(file_name, new_lines)
        return deleted

    @staticmethod
    def get_all_feedback(file_name):
        """Reads suggestion/enquiry file and returns structured list of feedback items."""
        lines = FileHandler.read_records(file_name)
        feedback = []
        for line in lines:
            data = line.strip().split("|")
            if len(data) >= 4:
                feedback.append(data[:4])
        return feedback