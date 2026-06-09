from manager import manager_menu, login_manager, register_manager
from client import client_menu, login_client, register_client
import db

def main():
    db.init_db()  # Initialize the database and creates tables if they don't exist
    while True:
        print("-----Welcome to the Hotel Management System!-----")
        print("1. I am a manager.")
        print("2. I am a client.")
        print("3. Exit")
        
        choice = input("Please select your role (1-3): ")
        
        if choice == '1':
            manager_flow()
        elif choice == '2':
            client_flow()
        elif choice == '3':
            print("Thank you for using the Hotel Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def manager_flow():
    while True:
        print("\n-----Manager Menu-----")
        print("1. Register")
        print("2. Login")
        print("3. Back to main menu")
        
        choice = input("Please select an option (1-3): ")
        
        if choice == '1':
            register_manager()
        elif choice == '2':
            if login_manager():
                manager_menu()
                break  # After menu, back to main menu
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def client_flow():
    while True:
        print("\n-----Client Menu-----")
        print("1. Register")
        print("2. Login")
        print("3. Back to main menu")
        
        choice = input("Please select an option (1-3): ")
        
        if choice == '1':
            register_client()
        elif choice == '2':
            if login_client():
                client_menu()
                break  # After menu, back to main
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()