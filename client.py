#Need to import execute method from db once we have the database set up
import db

def register_client():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    print("Registering a new client...")
    
    # Add client to database
    db.add_client(name, email)
    
    # Client Address(es)
    while True:
        print("Add an address (leave city blank to stop):")
        city = input("City: ")
        if not city:
            break
        address_num = int(input("Address number: "))
        street_name = input("Street name: ")
        db.add_address(city, address_num, street_name)
        db.add_client_address(email, city, address_num, street_name)
    
    # Credit card(s)
    while True:
        print("Add a credit card (leave number blank to stop):")
        card_num_str = input("Credit card number: ")
        if not card_num_str:
            break
        card_num = int(card_num_str)
        print("Billing address for credit card:")
        city = input("City: ")
        address_num = int(input("Address number: "))
        street_name = input("Street name: ")
        db.add_address(city, address_num, street_name)  #Ensure address exists
        db.add_credit_card(card_num, email, city, address_num, street_name)
    
    print("Registration complete!")

def login_client():
    email = input("Enter your email: ")
    name = db.login_client(email)
    if name:
        print(f"Welcome, {name}!")
        return True
    else:
        print("Invalid email. Please register first.")
        return False

def update_name():
    email = input("Enter your email: ")
    new_name = input("Enter new name: ")
    db.update_client_name(email, new_name)

def update_address():
    email = input("Enter your email: ")
    old_city = input("Enter city of old address: ")
    old_address_num = input("Enter old address number: ")
    old_street = input("Enter old street name: ")
    new_city = input("Enter new city: ")
    new_address_num = input("Enter new address number: ")
    new_street = input("Enter new street name: ")
    db.update_client_address(email, old_city, old_address_num, old_street, new_city, new_address_num, new_street)

def update_credit_card():
    old_credit_num = input("Enter old credit card number: ")
    new_credit_num = input("Enter new credit card number: ")
    db.update_credit_card(old_credit_num, new_credit_num)
    
def view_available_hotels_and_rooms():
    
    # Get date range from user
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    # Validate dates
    if not start_date or not end_date:
        print("Invalid date range. Please enter both start and end dates.")
        return
    
    #Get all hotels with available rooms
    available_hotels = db.get_hotels_with_available_rooms(start_date, end_date)
    
    if not available_hotels:
        print(f"No available rooms found for {start_date} to {end_date}.")
        return
    
    print(f"\nAvailable rooms for {start_date} to {end_date}:")
    print("-" * 35)
    print(f"{'Hotel Name':<20} {'Room Number':<12}")
    print("-" * 35)
    
    for hotel in available_hotels:
        hotel_id, hotel_name, city = hotel
        
        # Get available rooms for this specific hotel
        available_rooms = db.get_available_rooms_in_hotel(hotel_id, start_date, end_date)
        
        for room in available_rooms:
            room_num, num_windows, last_renov_year, accessible = room
            print(f"{hotel_name:<20} {room_num:<12}")
    
    print("-" * 35)

def manual_booking():
    print("\n===== Manual Booking =====")
    
    # Get client email and verify client exists
    client_email = input("Enter your email: ")
    client_name = db.login_client(client_email)
    if not client_name:
        print("Invalid email. Client not found.")
        return
    
    #Get hotel ID and verify hotel exists
    try:
        hotel_id = int(input("Enter hotel ID: "))
    except ValueError:
        print("Invalid hotel ID.")
        return
    
    hotel_info = db.get_hotel_info(hotel_id)
    if not hotel_info:
        print("Hotel not found.")
        return
    
    hotel_name = hotel_info[1]
    print(f"Selected hotel: {hotel_name}")
    
    # Get room number and verify room exists
    try:
        room_num = int(input("Enter room number: "))
    except ValueError:
        print("Invalid room number.")
        return
    
    room_details = db.get_room_details(hotel_id, room_num)
    if not room_details:
        print("Room not found in this hotel.")
        return
    
    # Get date range
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    if not start_date or not end_date:
        print("Invalid date range. Please enter both start and end dates.")
        return
    
    #Check if room is available for the date range
    available_rooms = db.get_available_rooms_in_hotel(hotel_id, start_date, end_date)
    room_available = any(room[0] == room_num for room in available_rooms)
    
    if not room_available:
        print(f"Room {room_num} is not available for {start_date} to {end_date}.")
        return
    
    price_per_day = db.get_booking_price(hotel_id, room_num)
    
    # Create the booking
    booking_id = db.get_next_booking_id()
    db.add_booking(booking_id, price_per_day, start_date, end_date, client_email, room_num, hotel_id)
    
    #Display confirmation
    print("\n===== Booking Confirmed =====")
    print(f"Booking ID: {booking_id}")
    print(f"Client: {client_name} ({client_email})")
    print(f"Hotel: {hotel_name}")
    print(f"Room: {room_num}")
    print(f"Check-in: {start_date}")
    print(f"Check-out: {end_date}")
    print(f"Price per day: ${price_per_day}")
    print("=============================\n")
def automatic_booking():
    print("\n===== Automatic Booking =====")
    
    client_email = input("Enter your email: ")
    
    #Verify client exists
    if not db.login_client(client_email):
        print("Invalid email. Client not found.")
        return
    
    try:
        hotel_id = int(input("Enter hotel ID: "))
    except ValueError:
        print("Invalid hotel ID.")
        return
    
    #Verify hotel exists
    hotel_info = db.get_hotel_info(hotel_id)
    if not hotel_info:
        print("Hotel not found.")
        return
    
    hotel_name = hotel_info[1]
    print(f"Selected hotel: {hotel_name}")
    
    #Get date range
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    #Get available rooms in the specified hotel
    available_rooms = db.get_available_rooms_in_hotel(hotel_id, start_date, end_date)
    
    if available_rooms:
        room = available_rooms[0]  #Book the first available room
        room_num = room[0]
        
        price_per_day = db.get_booking_price_per_day(hotel_id, room_num)
        
        #Create booking
        booking_id = db.get_next_booking_id()
        db.add_booking(booking_id, price_per_day, start_date, end_date, client_email, room_num, hotel_id)
        
        #Display confirmation
        print("\n===== Booking Confirmed - See Details Below =====")
        print(f"Booking ID: {booking_id}")
        print(f"Hotel: {hotel_name}")
        print(f"Room: {room_num}")
        print(f"Check-in: {start_date}")
        print(f"Check-out: {end_date}")
        print(f"Price per day: ${price_per_day}")
        print("=============================\n")
    else:
        #No room available - suggest alternative hotels available with specified date range
        print(f"\nNo rooms available at {hotel_name} for {start_date} to {end_date}.")
        
        #Get hotels with available rooms
        alternative_hotels = db.get_hotels_with_available_rooms(start_date, end_date)
        
        if alternative_hotels:
            print("\nAlternative hotels with available rooms:")
            for alt_hotel in alternative_hotels: #List all alternative hotels
                alt_id = alt_hotel[0]
                alt_name = alt_hotel[1]
                alt_city = alt_hotel[2]
                print(f"  - {alt_name} (ID: {alt_id}) in {alt_city}")
        else:
            print("No alternative hotels with available rooms for this date range.")

def view_all_bookings():
    print("\n===== View All Bookings =====")
    
    
    client_email = input("Enter your email: ")
    
    #Verify client exists
    client_name = db.login_client(client_email)
    if not client_name:
        print("Invalid email. Client not found.")
        return
    
    #Get all bookings for this client that is logged in
    bookings = db.get_client_bookings(client_email)
    
    if not bookings:
        print(f"No bookings found for {client_name} ({client_email}).")
        return
    
    print(f"\nBookings for {client_name} ({client_email}):")
    print("-" * 85)
    print(f"{'Booking ID':<10} {'Hotel':<20} {'Room':<5} {'Check-in':<12} {'Check-out':<12} {'Price/Day':<10} {'Total Cost':<10}")
    print("-" * 85)
    
    for booking in bookings:
        booking_id, hotel_name, room_num, start_date, end_date, price_per_day, total_cost = booking
        print(f"{booking_id:<10} {hotel_name:<20} {room_num:<5} {start_date:<12} {end_date:<12} ${price_per_day:<9} ${total_cost:<9.2f}")
    
    print("-" * 85)
    print(f"Total bookings: {len(bookings)}")

def submit_review():
    rating = input("Enter rating (1-10): ")
    comment = input("Enter comment: ")
    review_id = input("Enter review ID: ")
    hotel_id = input("Enter hotel ID: ")
    client_email = input("Enter your email: ")
    db.add_review(rating, comment, review_id, hotel_id, client_email)
    


def client_menu():
    while True:
        print("\n-----Client Menu-----")
        print("1. Update name")
        print("2. Update address")
        print("3. Update credit card")
        print("4. View available hotels and rooms")
        print("5. Manual booking")
        print("6. Automatic booking")
        print("7. View all bookings")
        print("8. Submit review")
        print("9. Logout")
        
        choice = input("Please select an option (1-9): ")
        
        if choice == '1':
            update_name()
        elif choice == '2':
            update_address()
        elif choice == '3':
            update_credit_card()
        elif choice == '4':
            view_available_hotels_and_rooms()
        elif choice == '5':
            manual_booking()
        elif choice == '6':
            automatic_booking()
        elif choice == '7':
            view_all_bookings()
        elif choice == '8':
            submit_review()
        elif choice == '9':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")