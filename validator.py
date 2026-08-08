import re
from file_handler import FileHandler

class Validator:
    MIN_AGE = 18
    EMPLOYEE_MIN_SALARY = 10000
    MANAGER_MIN_SALARY = 20000
    BOSS_MIN_SALARY = 40000
    
    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$")

    @staticmethod
    def validate_name(name):
        """Not empty, not only spaces, not only digits. Allows 'Sanjay Kumar'."""
        name = name.strip()
        if not name:
            return False
        if not any(ch.isalpha() for ch in name):
            return False
        return True

    @staticmethod
    def validate_id(id_value):
        """Not empty, not only spaces."""
        return id_value.strip() != ""

    @staticmethod
    def validate_designation(designation):
        """Not empty, not only spaces."""
        return designation.strip() != ""

    @staticmethod
    def validate_age(age):
        """age must already be an int."""
        return age >= Validator.MIN_AGE

    @staticmethod
    def validate_address(address):
        """Not empty, not only spaces, not only digits. Allows 'Pokhara-8'."""
        address = address.strip()
        if len(address) < 2:
            return False
        if address.isdigit():
            return False
        return True

    @staticmethod
    def validate_salary(salary, minimum):
        """salary must already be an int/float."""
        return salary >= minimum

    @staticmethod
    def validate_email(email):
        email = email.strip()
        if not email:
            return False
        return Validator.EMAIL_PATTERN.match(email) is not None

    @staticmethod
    def validate_password(password):
        return len(password) >= 6

    @staticmethod
    def has_invalid_chars(text):
        return "|" in text or "\n" in text or "\r" in text

    @staticmethod
    def check_duplicate_email(file_name, email, exclude_email=None):
        email = email.strip().lower()
        lines = FileHandler.read_records(file_name)
        for line in lines:
            data = line.strip().split("|")
            if len(data) >= 8:
                existing_email = data[6].strip().lower()
                if exclude_email and existing_email == exclude_email.strip().lower():
                    continue
                if existing_email == email:
                    return True
        return False

    @staticmethod
    def check_duplicate_id(file_name, id_value):
        id_value = id_value.strip()
        lines = FileHandler.read_records(file_name)
        for line in lines:
            data = line.strip().split("|")
            if len(data) >= 8 and data[1].strip() == id_value:
                return True
        return False