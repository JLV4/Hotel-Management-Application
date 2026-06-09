#Need to import execute method from db once we have the database set up
import db

def register_manager():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    ssn  = input("Enter your SSN: ")
    db.add_manager(name, email, ssn)
    print("Registering a new manager...")

def login_manager():
    ssn = input("Enter your SSN: ")
    name = db.login_manager(ssn)
    if name:
        print(f"Welcome, {name}!")
        return True
    else:
        print("Invalid SSN. Please register first.")
        return False

def insert_hotel():
    hotel_name = input("Enter hotel name: ")
    hotel_id = input("Enter hotel ID: ")
    city = input("Enter hotel city: ")
    adddress_num = input("Enter hotel address number: ")
    street = input("Enter hotel street: ")
    db.add_hotel(hotel_name, hotel_id, city, adddress_num, street)
    print("Inserting a new hotel...")

def remove_hotel():
    hotel_id = input("Enter hotel ID to remove: ")
    db.remove_hotel(hotel_id)

def update_hotel():
    hotel_id = input("Enter hotel ID: ")
    new_name = input("Enter new hotel name: ")
    db.update_hotel(hotel_id, new_name)

def insert_room():
    room_num = input("Enter room number: ")
    num_windows = input("Enter number of windows: ")
    last_renov_year = input("Enter last renovation year: ")
    accessible = input("Enter accessibility information: ")
    hotel_id = input("Enter hotel ID: ")
    db.add_room(room_num, num_windows, last_renov_year, accessible, hotel_id)
    print("Inserting a new room...")

def remove_room():
    hotel_id = input("Enter hotel ID: ")
    room_num = input("Enter room number: ")
    print("Removing a room...")
    db.remove_room(hotel_id, room_num)

def update_room():
    hotel_id = input("Enter hotel ID: ")
    room_num = input("Enter room number: ")
    new_num_windows = input("Enter new number of windows: ")
    new_last_renov_year = input("Enter new last renovation year: ")
    new_accessible = input("Enter new accessibility information: ")
    db.update_room(hotel_id, room_num, new_num_windows, new_last_renov_year, new_accessible)

def remove_client():
    email = input("Enter client email to remove: ")
    db.remove_client(email)

def show_top_k_clients():
    k = input("Enter the value of k: ")
    print("Showing name & email of top-k clients...\n")
    db.display_top_k_clients(k)

def show_hotel_bookings():
    print("Showing all hotel rooms and their number of bookings...\n")
    db.display_hotel_bookings()

def show_hotel_stats():
    print("Showing hotel stats...")
    db.display_hotel_stats()

def show_clients_in_cities():
    c1 = input("Enter city C1 (client address city): ")
    c2 = input("Enter city C2 (hotel city): ")
    print(f"Showing clients with address in {c1} who booked hotels in {c2}...\n")
    db.display_clients_in_cities(c1, c2)

def show_problematic_hotels():
    print("Showing problematic hotels...")
    db.display_problematic_hotels()

def show_client_spending():
    print("Showing client spending...")
    db.display_client_spending()


#MENU
def manager_menu():
    while True:
        print("\n-----Manager Menu-----")
        print("1. Insert hotel")
        print("2. Remove hotel")
        print("3. Update hotel")
        print("4. Insert room")
        print("5. Remove room")
        print("6. Update room")
        print("7. Remove client")
        print("8. Show top-k clients")
        print("9. Show hotel bookings")
        print("10. Show hotel stats")
        print("11. Show clients in cities")
        print("12. Show problematic hotels")
        print("13. Show client spending")
        print("14. Logout")

        choice = input("Please select an option (1-14): ")
        
        if choice == '1':
            insert_hotel()
        elif choice == '2':
            remove_hotel()
        elif choice == '3':
            update_hotel()
        elif choice == '4':
            insert_room()
        elif choice == '5':
            remove_room()
        elif choice == '6':
            update_room()
        elif choice == '7':
            remove_client()
        elif choice == '8':
            show_top_k_clients()
        elif choice == '9':
            show_hotel_bookings()
        elif choice == '10':
            show_hotel_stats()
        elif choice == '11':
            show_clients_in_cities()
        elif choice == '12':
            show_problematic_hotels()
        elif choice == '13':
            show_client_spending()
        elif choice == '14':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")