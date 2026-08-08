import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from auth import Authentication
from models import Boss, Manager, Employee
from operations import SystemOperations
from validator import Validator
from file_handler import FileHandler
class EmployeeManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Management System")
        self.geometry("900x650")
        self.minsize(800, 600)
        
        # Configure styles
        self.configure_styles()
        
        # Current active frame
        self._current_frame = None
        self.logged_in_user = None
        
        # Start at login screen
        self.show_login_screen()
    def configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        
        # Color palette
        bg_color = "#f4f6f9"
        card_bg = "#ffffff"
        primary_color = "#3a6073"  # slate blue
        secondary_color = "#16a085"  # teal
        text_color = "#2c3e50"
        
        # Window background
        self.configure(bg=bg_color)
        
        style.configure(".", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        style.configure("TLabel", background=bg_color, foreground=text_color)
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=primary_color)
        style.configure("Subheader.TLabel", font=("Segoe UI", 12, "bold"), foreground=secondary_color)
        
        style.configure("Card.TFrame", background=card_bg, relief="flat", borderwidth=0)
        style.configure("CardLabel.TLabel", background=card_bg, font=("Segoe UI", 10))
        style.configure("CardHeader.TLabel", background=card_bg, font=("Segoe UI", 12, "bold"), foreground=primary_color)
        
        # Entry Styling
        style.configure("TEntry", fieldbackground="white", selectbackground=secondary_color)
        
        # Buttons
        style.configure("TButton", font=("Segoe UI", 10, "bold"), background=primary_color, foreground="white", borderwidth=0, padding=6)
        style.map("TButton", background=[("active", secondary_color)])
        
        style.configure("Secondary.TButton", font=("Segoe UI", 10), background="#95a5a6", foreground="white", borderwidth=0, padding=6)
        style.map("Secondary.TButton", background=[("active", "#7f8c8d")])
        
        style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), background="#e74c3c", foreground="white", borderwidth=0, padding=6)
        style.map("Danger.TButton", background=[("active", "#c0392b")])
        
        # Notebook / Tabs
        style.configure("TNotebook", background=bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background="#e2e8f0", foreground=text_color, font=("Segoe UI", 10, "bold"), padding=(12, 6))
        style.map("TNotebook.Tab", background=[("selected", card_bg)], foreground=[("selected", primary_color)])
        
        # Treeview
        style.configure("Treeview", background="white", foreground=text_color, rowheight=25, fieldbackground="white", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#e2e8f0", foreground=primary_color, font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#d1e8ff")], foreground=[("selected", text_color)])
    def switch_frame(self, frame_class, *args, **kwargs):
        new_frame = frame_class(self, *args, **kwargs)
        if self._current_frame is not None:
            self._current_frame.destroy()
        self._current_frame = new_frame
        self._current_frame.pack(fill="both", expand=True, padx=20, pady=20)
    def show_login_screen(self):
        self.logged_in_user = None
        self.switch_frame(LoginFrame)
class LoginFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame")
        self.parent = parent
        
        # Grid weight settings to center card
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        card = ttk.Frame(self, style="Card.TFrame", padding=35, relief="solid", borderwidth=1)
        card.grid(row=1, column=1, sticky="nsew")
        
        # Header
        lbl_title = ttk.Label(card, text="Employee Management", style="Header.TLabel", font=("Segoe UI", 18, "bold"))
        lbl_title.pack(pady=(0, 20))
        
        # Login Type Choice
        lbl_type = ttk.Label(card, text="Login As:", style="CardLabel.TLabel", font=("Segoe UI", 10, "bold"))
        lbl_type.pack(anchor="w", pady=(0, 5))
        
        self.var_login_type = tk.StringVar(value="Employee")
        combo_type = ttk.Combobox(card, textvariable=self.var_login_type, values=["Boss", "Manager", "Employee"], state="readonly", font=("Segoe UI", 10))
        combo_type.pack(fill="x", pady=(0, 15))
        
        # Email
        lbl_email = ttk.Label(card, text="Email Address", style="CardLabel.TLabel")
        lbl_email.pack(anchor="w", pady=(0, 5))
        self.entry_email = ttk.Entry(card, font=("Segoe UI", 11))
        self.entry_email.pack(fill="x", pady=(0, 15))
        
        # Password
        lbl_password = ttk.Label(card, text="Password", style="CardLabel.TLabel")
        lbl_password.pack(anchor="w", pady=(0, 5))
        self.entry_password = ttk.Entry(card, show="*", font=("Segoe UI", 11))
        self.entry_password.pack(fill="x", pady=(0, 25))
        
        # Controls Frame
        btn_frame = ttk.Frame(card, style="Card.TFrame")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        btn_login = ttk.Button(btn_frame, text="Sign In", command=self.handle_login)
        btn_login.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Register Boss button
        self.btn_register_boss = ttk.Button(btn_frame, text="Register Boss", command=self.handle_register_boss, style="Secondary.TButton")
        self.btn_register_boss.pack(side="right", fill="x", expand=True)
        
        self.check_boss_status()
    def check_boss_status(self):
        lines = FileHandler.read_records(Authentication.BOSS_FILE)
        if any(line.strip() for line in lines):
            self.btn_register_boss.config(state="disabled")
    def handle_login(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        login_type = self.var_login_type.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Email and Password cannot be empty!")
            return
            
        if not Validator.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return
            
        file_map = {
            "Boss": Authentication.BOSS_FILE,
            "Manager": Authentication.MANAGER_FILE,
            "Employee": Authentication.EMPLOYEE_FILE
        }
        
        file_name = file_map[login_type]
        lines = FileHandler.read_records(file_name)
        if not any(line.strip() for line in lines):
            msg = "Boss does not exist! Please register first." if login_type == "Boss" else f"No {login_type.lower()}s registered yet."
            messagebox.showerror("Error", msg)
            return
        email_lower = email.lower()
        success_user = None
        for line in lines:
            data = line.strip().split("|")
            if len(data) >= 8 and data[6].strip().lower() == email_lower and data[7] == password:
                if login_type == "Boss":
                    success_user = Boss(*data[:8])
                elif login_type == "Manager":
                    success_user = Manager(*data[:8])
                else:
                    success_user = Employee(*data[:8])
                break
                
        if success_user:
            messagebox.showinfo("Success", "Login Successful!")
            self.parent.logged_in_user = success_user
            if login_type == "Boss":
                self.parent.switch_frame(BossDashboardFrame)
            elif login_type == "Manager":
                self.parent.switch_frame(ManagerDashboardFrame)
            else:
                self.parent.switch_frame(EmployeeDashboardFrame)
        else:
            messagebox.showerror("Error", "Invalid Email or Password!")
    def handle_register_boss(self):
        RegisterBossDialog(self)
class RegisterBossDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Boss Registration")
        self.geometry("450x550")
        self.resizable(False, False)
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        
        lbl_header = ttk.Label(frame, text="Boss Registration", style="Subheader.TLabel")
        lbl_header.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        fields = [
            ("Name", "name", False),
            ("ID", "id", False),
            ("Age", "age", False),
            ("Address", "address", False),
            ("Salary", "salary", False),
            ("Email", "email", False),
            ("Password", "password", True)
        ]
        
        self.entries = {}
        for idx, (label, name, is_password) in enumerate(fields, start=1):
            lbl = ttk.Label(frame, text=label + ":")
            lbl.grid(row=idx, column=0, sticky="w", pady=5)
            
            show_char = "*" if is_password else ""
            entry = ttk.Entry(frame, show=show_char, font=("Segoe UI", 10))
            entry.grid(row=idx, column=1, sticky="ew", padx=(10, 0), pady=5)
            self.entries[name] = entry
            
        frame.grid_columnconfigure(1, weight=1)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(20, 0))
        
        btn_submit = ttk.Button(btn_frame, text="Submit", command=self.submit)
        btn_submit.pack(side="left", padx=5)
        
        btn_cancel = ttk.Button(btn_frame, text="Cancel", command=self.destroy, style="Secondary.TButton")
        btn_cancel.pack(side="right", padx=5)
    def submit(self):
        name = self.entries["name"].get().strip()
        emp_id = self.entries["id"].get().strip()
        age_str = self.entries["age"].get().strip()
        address = self.entries["address"].get().strip()
        salary_str = self.entries["salary"].get().strip()
        email = self.entries["email"].get().strip()
        password = self.entries["password"].get().strip()
        
        if Validator.has_invalid_chars(name) or not Validator.validate_name(name):
            messagebox.showerror("Error", "Invalid name! Cannot contain '|', newlines, or be digits-only.")
            return
        if Validator.has_invalid_chars(emp_id) or not Validator.validate_id(emp_id):
            messagebox.showerror("Error", "Invalid ID!")
            return
        
        try:
            age = int(age_str)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number!")
            return
            
        if not Validator.validate_age(age):
            messagebox.showerror("Error", f"Age must be at least {Validator.MIN_AGE}!")
            return
            
        if Validator.has_invalid_chars(address) or not Validator.validate_address(address):
            messagebox.showerror("Error", "Invalid address!")
            return
            
        try:
            salary = int(salary_str)
        except ValueError:
            messagebox.showerror("Error", "Salary must be a number!")
            return
            
        if salary < 0:
            messagebox.showerror("Error", "Salary cannot be negative!")
            return
        if not Validator.validate_salary(salary, Validator.BOSS_MIN_SALARY):
            messagebox.showerror("Error", f"Salary too low. At least {Validator.BOSS_MIN_SALARY:,} required.")
            return
            
        if not Validator.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return
        email = email.lower()
        
        if Validator.has_invalid_chars(password) or not Validator.validate_password(password):
            messagebox.showerror("Error", "Password must be at least 6 characters and contain no '|' or newlines.")
            return
            
        record = f"{name}|{emp_id}|Boss|{age}|{address}|{salary}|{email}|{password}"
        FileHandler.append_record(Authentication.BOSS_FILE, record)
        messagebox.showinfo("Success", "Boss Registered Successfully!")
        self.parent.check_boss_status()
        self.destroy()
class EmployeeDashboardFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.user = parent.logged_in_user
        
        # Header Frame
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 20))
        
        lbl_welcome = ttk.Label(header_frame, text=f"Welcome, {self.user.name} ({self.user.designation})", style="Header.TLabel")
        lbl_welcome.pack(side="left")
        
        btn_logout = ttk.Button(header_frame, text="Logout", command=self.logout, style="Danger.TButton")
        btn_logout.pack(side="right")
        
        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
        self.tab_profile = ttk.Frame(self.notebook, padding=20)
        self.tab_feedback = ttk.Frame(self.notebook, padding=20)
        
        self.notebook.add(self.tab_profile, text="My Profile")
        self.notebook.add(self.tab_feedback, text="Suggestions & Enquiries")
        
        self.setup_profile_tab()
        self.setup_feedback_tab()
    def logout(self):
        self.parent.show_login_screen()
    def setup_profile_tab(self):
        for child in self.tab_profile.winfo_children():
            child.destroy()
            
        profile_card = ttk.Frame(self.tab_profile, style="Card.TFrame", padding=20, relief="solid", borderwidth=1)
        profile_card.pack(pady=10, fill="x")
        
        profile_data = self.user.view_profile()
        
        fields = [
            ("Name", profile_data["name"]),
            ("Employee ID", profile_data["emp_id"]),
            ("Designation", profile_data["designation"]),
            ("Age", str(profile_data["age"])),
            ("Address", profile_data["address"]),
            ("Salary", f"Rs. {profile_data['salary']:,}"),
            ("Email", profile_data["email"])
        ]
        
        for idx, (label, val) in enumerate(fields):
            lbl_key = ttk.Label(profile_card, text=label + ":", font=("Segoe UI", 10, "bold"), background="white")
            lbl_key.grid(row=idx, column=0, sticky="w", pady=6)
            
            lbl_val = ttk.Label(profile_card, text=val, background="white")
            lbl_val.grid(row=idx, column=1, sticky="w", padx=(20, 0), pady=6)
            
        btn_frame = ttk.Frame(self.tab_profile)
        btn_frame.pack(fill="x", pady=15)
        
        btn_edit_address = ttk.Button(btn_frame, text="Edit Address", command=self.edit_address)
        btn_edit_address.pack(side="left", padx=5)
        
        btn_change_pw = ttk.Button(btn_frame, text="Change Password", command=self.change_password)
        btn_change_pw.pack(side="left", padx=5)
    def edit_address(self):
        new_address = simpledialog.askstring("Edit Address", "Enter New Address:", parent=self)
        if new_address is not None:
            new_address = new_address.strip()
            try:
                self.user.update_address(Employee.FILE_NAME, new_address)
                messagebox.showinfo("Success", "Address Updated Successfully!")
                self.setup_profile_tab()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    def change_password(self):
        new_pass = simpledialog.askstring("Change Password", "Enter New Password:", show="*", parent=self)
        if new_pass is not None:
            new_pass = new_pass.strip()
            try:
                self.user.reset_password(Employee.FILE_NAME, new_pass)
                messagebox.showinfo("Success", "Password Changed Successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    def setup_feedback_tab(self):
        # Suggestion panel
        sug_frame = ttk.LabelFrame(self.tab_feedback, text="Give Suggestion", padding=15)
        sug_frame.pack(fill="x", pady=(0, 15))
        
        lbl_sug = ttk.Label(sug_frame, text="What would you like to suggest?")
        lbl_sug.pack(anchor="w", pady=(0, 5))
        
        self.text_sug = tk.Text(sug_frame, height=4, font=("Segoe UI", 10))
        self.text_sug.pack(fill="x", pady=(0, 10))
        
        btn_submit_sug = ttk.Button(sug_frame, text="Submit Suggestion", command=self.submit_suggestion)
        btn_submit_sug.pack(anchor="e")
        
        # Enquiry panel
        enq_frame = ttk.LabelFrame(self.tab_feedback, text="Give Enquiry", padding=15)
        enq_frame.pack(fill="x")
        
        lbl_enq = ttk.Label(enq_frame, text="Enter your enquiry or question:")
        lbl_enq.pack(anchor="w", pady=(0, 5))
        
        self.text_enq = tk.Text(enq_frame, height=4, font=("Segoe UI", 10))
        self.text_enq.pack(fill="x", pady=(0, 10))
        
        btn_submit_enq = ttk.Button(enq_frame, text="Submit Enquiry", command=self.submit_enquiry)
        btn_submit_enq.pack(anchor="e")
    def submit_suggestion(self):
        msg = self.text_sug.get("1.0", "end-1c").strip()
        try:
            self.user.give_suggestion(msg)
            messagebox.showinfo("Success", "Suggestion submitted successfully!")
            self.text_sug.delete("1.0", tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    def submit_enquiry(self):
        msg = self.text_enq.get("1.0", "end-1c").strip()
        try:
            self.user.give_enquiry(msg)
            messagebox.showinfo("Success", "Enquiry submitted successfully!")
            self.text_enq.delete("1.0", tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
class ManagerDashboardFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.user = parent.logged_in_user
        
        # Header Frame
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 20))
        
        lbl_welcome = ttk.Label(header_frame, text=f"Welcome, {self.user.name} ({self.user.designation})", style="Header.TLabel")
        lbl_welcome.pack(side="left")
        
        btn_logout = ttk.Button(header_frame, text="Logout", command=self.logout, style="Danger.TButton")
        btn_logout.pack(side="right")
        
        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
        self.tab_profile = ttk.Frame(self.notebook, padding=20)
        self.tab_employees = ttk.Frame(self.notebook, padding=20)
        self.tab_feedback = ttk.Frame(self.notebook, padding=20)
        
        self.notebook.add(self.tab_profile, text="My Profile")
        self.notebook.add(self.tab_employees, text="Manage Employees")
        self.notebook.add(self.tab_feedback, text="View Feedback")
        
        self.setup_profile_tab()
        self.setup_employees_tab()
        self.setup_feedback_tab()
    def logout(self):
        self.parent.show_login_screen()
    def setup_profile_tab(self):
        for child in self.tab_profile.winfo_children():
            child.destroy()
            
        profile_card = ttk.Frame(self.tab_profile, style="Card.TFrame", padding=20, relief="solid", borderwidth=1)
        profile_card.pack(pady=10, fill="x")
        
        profile_data = self.user.view_profile()
        
        fields = [
            ("Name", profile_data["name"]),
            ("Manager ID", profile_data["emp_id"]),
            ("Designation", profile_data["designation"]),
            ("Age", str(profile_data["age"])),
            ("Address", profile_data["address"]),
            ("Salary", f"Rs. {profile_data['salary']:,}"),
            ("Email", profile_data["email"])
        ]
        
        for idx, (label, val) in enumerate(fields):
            lbl_key = ttk.Label(profile_card, text=label + ":", font=("Segoe UI", 10, "bold"), background="white")
            lbl_key.grid(row=idx, column=0, sticky="w", pady=6)
            
            lbl_val = ttk.Label(profile_card, text=val, background="white")
            lbl_val.grid(row=idx, column=1, sticky="w", padx=(20, 0), pady=6)
            
        btn_frame = ttk.Frame(self.tab_profile)
        btn_frame.pack(fill="x", pady=15)
        
        btn_edit_address = ttk.Button(btn_frame, text="Edit Address", command=self.edit_address)
        btn_edit_address.pack(side="left", padx=5)
        
        btn_change_pw = ttk.Button(btn_frame, text="Change Password", command=self.change_password)
        btn_change_pw.pack(side="left", padx=5)
    def edit_address(self):
        new_address = simpledialog.askstring("Edit Address", "Enter New Address:", parent=self)
        if new_address is not None:
            new_address = new_address.strip()
            try:
                self.user.update_address(Manager.FILE_NAME, new_address)
                messagebox.showinfo("Success", "Address Updated Successfully!")
                self.setup_profile_tab()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    def change_password(self):
        new_pass = simpledialog.askstring("Change Password", "Enter New Password:", show="*", parent=self)
        if new_pass is not None:
            new_pass = new_pass.strip()
            try:
                self.user.reset_password(Manager.FILE_NAME, new_pass)
                messagebox.showinfo("Success", "Password Changed Successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    def setup_employees_tab(self):
        search_frame = ttk.Frame(self.tab_employees)
        search_frame.pack(fill="x", pady=(0, 10))
        
        lbl_search = ttk.Label(search_frame, text="Search Employees:")
        lbl_search.pack(side="left", padx=(0, 10))
        
        self.entry_search_emp = ttk.Entry(search_frame, font=("Segoe UI", 10), width=30)
        self.entry_search_emp.pack(side="left", padx=(0, 10))
        
        btn_search = ttk.Button(search_frame, text="Search", command=self.search_employees)
        btn_search.pack(side="left", padx=(0, 5))
        
        btn_clear = ttk.Button(search_frame, text="Clear", command=self.clear_search_employees, style="Secondary.TButton")
        btn_clear.pack(side="left")
        
        btn_add = ttk.Button(search_frame, text="Add Employee", command=self.add_employee)
        btn_add.pack(side="right")
        
        # Treeview frame
        tree_frame = ttk.Frame(self.tab_employees)
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("name", "id", "designation", "age", "address", "salary", "email")
        self.tree_employees = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        self.tree_employees.heading("name", text="Name")
        self.tree_employees.heading("id", text="ID")
        self.tree_employees.heading("designation", text="Designation")
        self.tree_employees.heading("age", text="Age")
        self.tree_employees.heading("address", text="Address")
        self.tree_employees.heading("salary", text="Salary")
        self.tree_employees.heading("email", text="Email Address")
        
        self.tree_employees.column("name", width=120)
        self.tree_employees.column("id", width=80)
        self.tree_employees.column("designation", width=100)
        self.tree_employees.column("age", width=50)
        self.tree_employees.column("address", width=120)
        self.tree_employees.column("salary", width=80)
        self.tree_employees.column("email", width=180)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_employees.yview)
        self.tree_employees.configure(yscrollcommand=scrollbar.set)
        
        self.tree_employees.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Controls panel
        ctrl_frame = ttk.Frame(self.tab_employees)
        ctrl_frame.pack(fill="x", pady=(10, 0))
        
        btn_delete = ttk.Button(ctrl_frame, text="Delete Selected Employee", command=self.delete_employee, style="Danger.TButton")
        btn_delete.pack(side="left")
        
        self.populate_employees_table()
    def populate_employees_table(self, records=None):
        for item in self.tree_employees.get_children():
            self.tree_employees.delete(item)
            
        if records is None:
            records = SystemOperations.get_all_users(Employee.FILE_NAME)
            
        for data in records:
            display_data = list(data)
            try:
                display_data[5] = f"{int(data[5]):,}"
            except ValueError:
                pass
            self.tree_employees.insert("", "end", values=display_data[:7])
    def search_employees(self):
        kw = self.entry_search_emp.get().strip()
        results = SystemOperations.search_users(Employee.FILE_NAME, kw)
        self.populate_employees_table(results)
    def clear_search_employees(self):
        self.entry_search_emp.delete(0, tk.END)
        self.populate_employees_table()
    def add_employee(self):
        AddUserDialog(self, Employee.FILE_NAME, Validator.EMPLOYEE_MIN_SALARY, "employee", self.populate_employees_table)
    def delete_employee(self):
        selected = self.tree_employees.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an employee from the table to delete!")
            return
            
        item_values = self.tree_employees.item(selected[0])["values"]
        emp_id = str(item_values[1])
        name = item_values[0]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Employee '{name}' (ID: {emp_id})?")
        if confirm:
            success = SystemOperations.delete_user_by_id(Employee.FILE_NAME, emp_id)
            if success:
                messagebox.showinfo("Success", "Employee deleted successfully!")
                self.populate_employees_table()
            else:
                messagebox.showerror("Error", "Failed to delete employee!")
    def setup_feedback_tab(self):
        fb_notebook = ttk.Notebook(self.tab_feedback)
        fb_notebook.pack(fill="both", expand=True)
        
        tab_sug = ttk.Frame(fb_notebook, padding=10)
        tab_enq = ttk.Frame(fb_notebook, padding=10)
        
        fb_notebook.add(tab_sug, text="Suggestions Log")
        fb_notebook.add(tab_enq, text="Enquiries Log")
        
        # Suggestions Tree
        columns = ("name", "id", "message", "timestamp")
        self.tree_sug = ttk.Treeview(tab_sug, columns=columns, show="headings")
        self.tree_sug.heading("name", text="Name")
        self.tree_sug.heading("id", text="Employee ID")
        self.tree_sug.heading("message", text="Suggestion Message")
        self.tree_sug.heading("timestamp", text="Submitted Timestamp")
        self.tree_sug.column("name", width=120)
        self.tree_sug.column("id", width=80)
        self.tree_sug.column("message", width=350)
        self.tree_sug.column("timestamp", width=150)
        
        # Scrollbar for suggestions
        scroll_sug = ttk.Scrollbar(tab_sug, orient="vertical", command=self.tree_sug.yview)
        self.tree_sug.configure(yscrollcommand=scroll_sug.set)
        self.tree_sug.pack(side="left", fill="both", expand=True)
        scroll_sug.pack(side="right", fill="y")
        
        # Enquiries Tree
        self.tree_enq = ttk.Treeview(tab_enq, columns=columns, show="headings")
        self.tree_enq.heading("name", text="Name")
        self.tree_enq.heading("id", text="Employee ID")
        self.tree_enq.heading("message", text="Enquiry Message")
        self.tree_enq.heading("timestamp", text="Submitted Timestamp")
        self.tree_enq.column("name", width=120)
        self.tree_enq.column("id", width=80)
        self.tree_enq.column("message", width=350)
        self.tree_enq.column("timestamp", width=150)
        
        # Scrollbar for enquiries
        scroll_enq = ttk.Scrollbar(tab_enq, orient="vertical", command=self.tree_enq.yview)
        self.tree_enq.configure(yscrollcommand=scroll_enq.set)
        self.tree_enq.pack(side="left", fill="both", expand=True)
        scroll_enq.pack(side="right", fill="y")
        
        self.populate_feedback_tables()
        
    def populate_feedback_tables(self):
        # Suggestions
        for item in self.tree_sug.get_children():
            self.tree_sug.delete(item)
        sug_data = SystemOperations.get_all_feedback("suggestion.txt")
        for row in sug_data:
            self.tree_sug.insert("", "end", values=row)
            
        # Enquiries
        for item in self.tree_enq.get_children():
            self.tree_enq.delete(item)
        enq_data = SystemOperations.get_all_feedback("enquiry.txt")
        for row in enq_data:
            self.tree_enq.insert("", "end", values=row)
class BossDashboardFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.user = parent.logged_in_user
        
        # Header Frame
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 20))
        
        lbl_welcome = ttk.Label(header_frame, text=f"Welcome, {self.user.name} ({self.user.designation})", style="Header.TLabel")
        lbl_welcome.pack(side="left")
        
        btn_logout = ttk.Button(header_frame, text="Logout", command=self.logout, style="Danger.TButton")
        btn_logout.pack(side="right")
        
        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
        self.tab_profile = ttk.Frame(self.notebook, padding=20)
        self.tab_managers = ttk.Frame(self.notebook, padding=20)
        self.tab_employees = ttk.Frame(self.notebook, padding=20)
        
        self.notebook.add(self.tab_profile, text="My Profile")
        self.notebook.add(self.tab_managers, text="Manage Managers")
        self.notebook.add(self.tab_employees, text="Manage Employees")
        
        self.setup_profile_tab()
        self.setup_managers_tab()
        self.setup_employees_tab()
    def logout(self):
        self.parent.show_login_screen()
    def setup_profile_tab(self):
        for child in self.tab_profile.winfo_children():
            child.destroy()
            
        profile_card = ttk.Frame(self.tab_profile, style="Card.TFrame", padding=20, relief="solid", borderwidth=1)
        profile_card.pack(pady=10, fill="x")
        
        profile_data = self.user.view_profile()
        
        fields = [
            ("Name", profile_data["name"]),
            ("Boss ID", profile_data["emp_id"]),
            ("Designation", profile_data["designation"]),
            ("Age", str(profile_data["age"])),
            ("Address", profile_data["address"]),
            ("Salary", f"Rs. {profile_data['salary']:,}"),
            ("Email", profile_data["email"])
        ]
        
        for idx, (label, val) in enumerate(fields):
            lbl_key = ttk.Label(profile_card, text=label + ":", font=("Segoe UI", 10, "bold"), background="white")
            lbl_key.grid(row=idx, column=0, sticky="w", pady=6)
            
            lbl_val = ttk.Label(profile_card, text=val, background="white")
            lbl_val.grid(row=idx, column=1, sticky="w", padx=(20, 0), pady=6)
            
        btn_frame = ttk.Frame(self.tab_profile)
        btn_frame.pack(fill="x", pady=15)
        
        btn_edit_address = ttk.Button(btn_frame, text="Edit Address", command=self.edit_address)
        btn_edit_address.pack(side="left", padx=5)
        
        btn_change_pw = ttk.Button(btn_frame, text="Change Password", command=self.change_password)
        btn_change_pw.pack(side="left", padx=5)
    def edit_address(self):
        new_address = simpledialog.askstring("Edit Address", "Enter New Address:", parent=self)
        if new_address is not None:
            new_address = new_address.strip()
            try:
                self.user.update_address(Boss.FILE_NAME, new_address)
                messagebox.showinfo("Success", "Address Updated Successfully!")
                self.setup_profile_tab()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    def change_password(self):
        new_pass = simpledialog.askstring("Change Password", "Enter New Password:", show="*", parent=self)
        if new_pass is not None:
            new_pass = new_pass.strip()
            try:
                self.user.reset_password(Boss.FILE_NAME, new_pass)
                messagebox.showinfo("Success", "Password Changed Successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    def setup_managers_tab(self):
        search_frame = ttk.Frame(self.tab_managers)
        search_frame.pack(fill="x", pady=(0, 10))
        
        lbl_search = ttk.Label(search_frame, text="Search Managers:")
        lbl_search.pack(side="left", padx=(0, 10))
        
        self.entry_search_mgr = ttk.Entry(search_frame, font=("Segoe UI", 10), width=30)
        self.entry_search_mgr.pack(side="left", padx=(0, 10))
        
        btn_search = ttk.Button(search_frame, text="Search", command=self.search_managers)
        btn_search.pack(side="left", padx=(0, 5))
        
        btn_clear = ttk.Button(search_frame, text="Clear", command=self.clear_search_managers, style="Secondary.TButton")
        btn_clear.pack(side="left")
        
        btn_add = ttk.Button(search_frame, text="Add Manager", command=self.add_manager)
        btn_add.pack(side="right")
        
        # Treeview frame
        tree_frame = ttk.Frame(self.tab_managers)
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("name", "id", "designation", "age", "address", "salary", "email")
        self.tree_managers = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        self.tree_managers.heading("name", text="Name")
        self.tree_managers.heading("id", text="ID")
        self.tree_managers.heading("designation", text="Designation")
        self.tree_managers.heading("age", text="Age")
        self.tree_managers.heading("address", text="Address")
        self.tree_managers.heading("salary", text="Salary")
        self.tree_managers.heading("email", text="Email Address")
        
        self.tree_managers.column("name", width=120)
        self.tree_managers.column("id", width=80)
        self.tree_managers.column("designation", width=100)
        self.tree_managers.column("age", width=50)
        self.tree_managers.column("address", width=120)
        self.tree_managers.column("salary", width=80)
        self.tree_managers.column("email", width=180)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_managers.yview)
        self.tree_managers.configure(yscrollcommand=scrollbar.set)
        
        self.tree_managers.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ctrl_frame = ttk.Frame(self.tab_managers)
        ctrl_frame.pack(fill="x", pady=(10, 0))
        
        btn_delete = ttk.Button(ctrl_frame, text="Delete Selected Manager", command=self.delete_manager, style="Danger.TButton")
        btn_delete.pack(side="left")
        
        self.populate_managers_table()
    def populate_managers_table(self, records=None):
        for item in self.tree_managers.get_children():
            self.tree_managers.delete(item)
            
        if records is None:
            records = SystemOperations.get_all_users(Manager.FILE_NAME)
            
        for data in records:
            display_data = list(data)
            try:
                display_data[5] = f"{int(data[5]):,}"
            except ValueError:
                pass
            self.tree_managers.insert("", "end", values=display_data[:7])
    def search_managers(self):
        kw = self.entry_search_mgr.get().strip()
        results = SystemOperations.search_users(Manager.FILE_NAME, kw)
        self.populate_managers_table(results)
    def clear_search_managers(self):
        self.entry_search_mgr.delete(0, tk.END)
        self.populate_managers_table()
    def add_manager(self):
        AddUserDialog(self, Manager.FILE_NAME, Validator.MANAGER_MIN_SALARY, "manager", self.populate_managers_table)
    def delete_manager(self):
        selected = self.tree_managers.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a manager from the table to delete!")
            return
            
        item_values = self.tree_managers.item(selected[0])["values"]
        emp_id = str(item_values[1])
        name = item_values[0]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Manager '{name}' (ID: {emp_id})?")
        if confirm:
            success = SystemOperations.delete_user_by_id(Manager.FILE_NAME, emp_id)
            if success:
                messagebox.showinfo("Success", "Manager deleted successfully!")
                self.populate_managers_table()
            else:
                messagebox.showerror("Error", "Failed to delete manager!")
    def setup_employees_tab(self):
        search_frame = ttk.Frame(self.tab_employees)
        search_frame.pack(fill="x", pady=(0, 10))
        
        lbl_search = ttk.Label(search_frame, text="Search Employees:")
        lbl_search.pack(side="left", padx=(0, 10))
        
        self.entry_search_emp = ttk.Entry(search_frame, font=("Segoe UI", 10), width=30)
        self.entry_search_emp.pack(side="left", padx=(0, 10))
        
        btn_search = ttk.Button(search_frame, text="Search", command=self.search_employees)
        btn_search.pack(side="left", padx=(0, 5))
        
        btn_clear = ttk.Button(search_frame, text="Clear", command=self.clear_search_employees, style="Secondary.TButton")
        btn_clear.pack(side="left")
        
        btn_add = ttk.Button(search_frame, text="Add Employee", command=self.add_employee)
        btn_add.pack(side="right")
        
        # Treeview frame
        tree_frame = ttk.Frame(self.tab_employees)
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("name", "id", "designation", "age", "address", "salary", "email")
        self.tree_employees = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        self.tree_employees.heading("name", text="Name")
        self.tree_employees.heading("id", text="ID")
        self.tree_employees.heading("designation", text="Designation")
        self.tree_employees.heading("age", text="Age")
        self.tree_employees.heading("address", text="Address")
        self.tree_employees.heading("salary", text="Salary")
        self.tree_employees.heading("email", text="Email Address")
        
        self.tree_employees.column("name", width=120)
        self.tree_employees.column("id", width=80)
        self.tree_employees.column("designation", width=100)
        self.tree_employees.column("age", width=50)
        self.tree_employees.column("address", width=120)
        self.tree_employees.column("salary", width=80)
        self.tree_employees.column("email", width=180)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_employees.yview)
        self.tree_employees.configure(yscrollcommand=scrollbar.set)
        
        self.tree_employees.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Controls panel
        ctrl_frame = ttk.Frame(self.tab_employees)
        ctrl_frame.pack(fill="x", pady=(10, 0))
        
        btn_delete = ttk.Button(ctrl_frame, text="Delete Selected Employee", command=self.delete_employee, style="Danger.TButton")
        btn_delete.pack(side="left")
        
        self.populate_employees_table()
    def populate_employees_table(self, records=None):
        for item in self.tree_employees.get_children():
            self.tree_employees.delete(item)
            
        if records is None:
            records = SystemOperations.get_all_users(Employee.FILE_NAME)
            
        for data in records:
            display_data = list(data)
            try:
                display_data[5] = f"{int(data[5]):,}"
            except ValueError:
                pass
            self.tree_employees.insert("", "end", values=display_data[:7])
    def search_employees(self):
        kw = self.entry_search_emp.get().strip()
        results = SystemOperations.search_users(Employee.FILE_NAME, kw)
        self.populate_employees_table(results)
    def clear_search_employees(self):
        self.entry_search_emp.delete(0, tk.END)
        self.populate_employees_table()
    def add_employee(self):
        AddUserDialog(self, Employee.FILE_NAME, Validator.EMPLOYEE_MIN_SALARY, "employee", self.populate_employees_table)
    def delete_employee(self):
        selected = self.tree_employees.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an employee from the table to delete!")
            return
            
        item_values = self.tree_employees.item(selected[0])["values"]
        emp_id = str(item_values[1])
        name = item_values[0]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Employee '{name}' (ID: {emp_id})?")
        if confirm:
            success = SystemOperations.delete_user_by_id(Employee.FILE_NAME, emp_id)
            if success:
                messagebox.showinfo("Success", "Employee deleted successfully!")
                self.populate_employees_table()
            else:
                messagebox.showerror("Error", "Failed to delete employee!")
class AddUserDialog(tk.Toplevel):
    def __init__(self, parent, file_name, min_salary, user_type, callback):
        super().__init__(parent)
        self.file_name = file_name
        self.min_salary = min_salary
        self.user_type = user_type
        self.callback = callback
        
        self.title(f"Add New {user_type.capitalize()}")
        self.geometry("450x550")
        self.resizable(False, False)
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        
        lbl_header = ttk.Label(frame, text=f"Add New {user_type.capitalize()}", style="Subheader.TLabel")
        lbl_header.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        fields = [
            ("Name", "name", False),
            ("ID", "id", False),
            ("Designation", "designation", False),
            ("Age", "age", False),
            ("Address", "address", False),
            ("Salary", "salary", False),
            ("Email", "email", False),
            ("Password", "password", True)
        ]
        
        self.entries = {}
        for idx, (label, name, is_password) in enumerate(fields, start=1):
            lbl = ttk.Label(frame, text=label + ":")
            lbl.grid(row=idx, column=0, sticky="w", pady=5)
            
            show_char = "*" if is_password else ""
            entry = ttk.Entry(frame, show=show_char, font=("Segoe UI", 10))
            entry.grid(row=idx, column=1, sticky="ew", padx=(10, 0), pady=5)
            self.entries[name] = entry
            
        frame.grid_columnconfigure(1, weight=1)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(20, 0))
        
        btn_submit = ttk.Button(btn_frame, text="Submit", command=self.submit)
        btn_submit.pack(side="left", padx=5)
        
        btn_cancel = ttk.Button(btn_frame, text="Cancel", command=self.destroy, style="Secondary.TButton")
        btn_cancel.pack(side="right", padx=5)
    def submit(self):
        name = self.entries["name"].get().strip()
        emp_id = self.entries["id"].get().strip()
        designation = self.entries["designation"].get().strip()
        age_str = self.entries["age"].get().strip()
        address = self.entries["address"].get().strip()
        salary_str = self.entries["salary"].get().strip()
        email = self.entries["email"].get().strip()
        password = self.entries["password"].get().strip()
        
        try:
            SystemOperations.add_user(
                self.file_name, self.min_salary, self.user_type,
                name, emp_id, designation, age_str, address, salary_str, email, password
            )
            messagebox.showinfo("Success", f"{self.user_type.capitalize()} Added Successfully!")
            self.callback()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))