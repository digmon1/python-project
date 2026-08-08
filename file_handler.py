import os

class FileHandler:
    @staticmethod
    def initialize_files():
        files = ["boss.txt", "manager.txt", "employee.txt", "suggestion.txt", "enquiry.txt"]
        for file in files:
            if not os.path.exists(file):
                try:
                    with open(file, "w") as f:
                        pass  # Create empty file
                    print(f"Created {file}")
                except OSError as e:
                    print(f"Warning: could not create {file} ({e})")

    @staticmethod
    def read_records(file_name):
        """Reads and returns all lines from a file. Handles file not found."""
        if not os.path.exists(file_name):
            return []
        try:
            with open(file_name, "r") as f:
                return f.readlines()
        except OSError:
            return []

    @staticmethod
    def append_record(file_name, record_str):
        """Appends a single line to the file. Ensures a newline at the end."""
        try:
            with open(file_name, "a") as f:
                f.write(record_str.strip() + "\n")
            return True
        except OSError:
            return False

    @staticmethod
    def write_records(file_name, lines):
        """Writes all lines to a file, replacing its contents."""
        try:
            with open(file_name, "w") as f:
                f.writelines(lines)
            return True
        except OSError:
            return False

    @staticmethod
    def update_record_field(file_name, email, field_index, new_value):
        """
        Updates a specific field in a record identified by email.
        The records are '|' delimited.
        """
        lines = FileHandler.read_records(file_name)
        email_lower = email.strip().lower()
        updated = False
        new_lines = []
        for line in lines:
            data = line.strip().split("|")
            if len(data) >= 8 and data[6].strip().lower() == email_lower and not updated:
                data[field_index] = str(new_value)
                new_lines.append("|".join(data) + "\n")
                updated = True
            else:
                new_lines.append(line)
        if updated:
            FileHandler.write_records(file_name, new_lines)
        return updated