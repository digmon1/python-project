# Sanjay Kumar Shrestha (NP071558) - Leader
# Prabin Dahal (NP071529)
# Kapilmani Bhattrai (NP07151)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from file_handler import FileHandler
from auth import Authentication
from gui import EmployeeManagementApp
# MAIN FUNCTION
def main():
    # Initialize all required files
    FileHandler.initialize_files()
    # Display team information
    print("=" * 60)
    print("EMPLOYEE MANAGEMENT SYSTEM - TEAM MEMBERS")
    print("=" * 60)
    print("Leader: Sanjay Kumar Shrestha (NP071558)")
    print("Member: Prabin Dahal (NP071529)")
    print("Member: Kapilmani Bhattrai (NP07151)")
    print("=" * 60 + "\n")
    # Launch Tkinter GUI
    app = EmployeeManagementApp()
    app.mainloop()
    # Main menu loop
    while True:
        print("=" * 50)
        print("\tMAIN MENU")
        print("=" * 50)
        print("1. Boss Register")
        print("2. Boss Login")
        print("3. Manager Login")
        print("4. Employee Login")
        print("5. Exit")
        choice = input("Enter choice (1-5): ").strip()
        if choice == "1":
            Authentication.register_boss()
        elif choice == "2":
            user = Authentication.boss_login()
            if user:
                user.show_menu()
        elif choice == "3":
            user = Authentication.login(Authentication.MANAGER_FILE)
            if user:
                user.show_menu()
        elif choice == "4":
            user = Authentication.login(Authentication.EMPLOYEE_FILE)
            if user:
                user.show_menu()
        elif choice == "5":
            print("=" * 50)
            print("Thank you for using Employee Management System!")
            print("Exiting System...")
            print("=" * 50)
            break
        else:
            print("Invalid Choice! Please enter from 1-5\n")
# Run the main function
if __name__ == "__main__":
    main()