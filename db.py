import sqlite3

db_file = "Hotel_Management_System.db"

def init_db():
    print("Initializing database . . .")
    delete_db()  # Delete existing database and tables if they exist
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        create_all_tables(cursor)

    print("Database initialized successfully!")



def delete_db():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.executescript("""
            DROP TABLE IF EXISTS client;
            DROP TABLE IF EXISTS credit_card;
            DROP TABLE IF EXISTS address;
            DROP TABLE IF EXISTS manager;
            DROP TABLE IF EXISTS hotel;
            DROP TABLE IF EXISTS room;
            DROP TABLE IF EXISTS booking;
            DROP TABLE IF EXISTS review;
            DROP TABLE IF EXISTS client_address;
            DROP TABLE IF EXISTS manages;
        """)
        conn.commit()

def create_all_tables(cursor):
    create_client_table(cursor)
    create_credit_card_table(cursor)
    create_address_table(cursor)
    create_manager_table(cursor)
    create_hotel_table(cursor)
    create_room_table(cursor)
    create_booking_table(cursor)
    create_review_table(cursor)
    create_client_address_table(cursor)
    create_manages_table(cursor)


def create_client_table(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS client (
            client_name TEXT,
	        client_email TEXT NOT NULL,
	        PRIMARY KEY(client_email)
        );
    """)

def create_credit_card_table(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS credit_card (
            credit_card_num INT NOT NULL,
	        client_email TEXT NOT NULL,
	        city TEXT NOT NULL,
	        address_num INT NOT NULL,
	        street_name TEXT NOT NULL,
            PRIMARY KEY(credit_card_num),
            FOREIGN KEY(client_email) REFERENCES client,
	        FOREIGN KEY(city, address_num, street_name) REFERENCES address	 
        );
    """)

def create_address_table(cursor):
    cursor.executescript("""
        CREATE TABLE address (
	        city TEXT NOT NULL,
	        address_num INT NOT NULL,
	        street_name TEXT NOT NULL,
	        PRIMARY KEY(city, address_num, street_name)
        );
    """)

def create_manager_table(cursor):
    cursor.executescript("""
        CREATE TABLE manager (
	        manager_name TEXT,
	        manager_email TEXT,
	        ssn INT NOT NULL,
	        PRIMARY KEY(ssn)
        );
    """)

def create_hotel_table(cursor):
    cursor.executescript("""
        CREATE TABLE hotel (
	        hotel_name TEXT,
	        hotel_id INT NOT NULL,
	        city TEXT NOT NULL,
	        address_num INT NOT NULL,
	        street_name TEXT NOT NULL,
            PRIMARY KEY(hotel_id),
	        FOREIGN KEY(city, address_num, street_name) REFERENCES address,
	        UNIQUE(city, address_num, street_name)
        );
    """)

def create_booking_table(cursor):
    cursor.executescript("""
        CREATE TABLE booking (
	        booking_id INT NOT NULL,
	        price_per_day INT,
	        start_date DATE NOT NULL,
	        end_date DATE NOT NULL,
	        client_email TEXT NOT NULL,
	        room_num INT NOT NULL,
	        hotel_id INT NOT NULL,
	        PRIMARY KEY(booking_id),
	        FOREIGN KEY(client_email) REFERENCES client,
	        FOREIGN KEY(room_num, hotel_id) REFERENCES room
        );
    """)

def create_room_table(cursor):
    cursor.executescript("""
        CREATE TABLE room (
	        room_num INT NOT NULL,
	        num_windows INT,
	        last_renov_year INT,
	        accessible TEXT CHECK (accessible = 'elevator' OR accessible = 'stairs'),
	        hotel_id INT NOT NULL,
	        PRIMARY KEY(hotel_id, room_num),
	        FOREIGN KEY(hotel_id) REFERENCES hotel
        );
    """)

def create_review_table(cursor):
    cursor.executescript("""
        CREATE TABLE review (
	        rating INT CHECK (rating BETWEEN 0 AND 10),
	        review_message TEXT,
	        review_id INT NOT NULL,
	        hotel_id INT NOT NULL,
	        client_email TEXT NOT NULL,
	        PRIMARY KEY(review_id, hotel_id),
	        FOREIGN KEY(hotel_id) REFERENCES hotel,
	        FOREIGN KEY(client_email) REFERENCES client
        );
    """)

def create_client_address_table(cursor):
    cursor.executescript("""
        CREATE TABLE client_address (
	        client_email TEXT NOT NULL,
	        city TEXT NOT NULL,
	        address_num INT NOT NULL,
	        street_name TEXT NOT NULL,
	        PRIMARY KEY(client_email, city, address_num, street_name),
	        FOREIGN KEY(client_email) REFERENCES client,
	        FOREIGN KEY(city, address_num, street_name) REFERENCES address
        );
    """)

def create_manages_table(cursor):
    cursor.executescript("""
        CREATE TABLE manages (
	        ssn INT NOT NULL,
	        hotel_id INT NOT NULL,
	        PRIMARY KEY(ssn, hotel_id),
	        FOREIGN KEY(ssn) REFERENCES manager,
	        FOREIGN KEY(hotel_id) REFERENCES hotel
        );
    """)

def add_client(client_name, client_email):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO client (client_name, client_email)
            VALUES (?, ?);
        """, (client_name, client_email))
        conn.commit()

def remove_client(client_email):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM client WHERE client_email = ?;""", (client_email,))
        if cursor.fetchone() is None:
            print("Client not found.")
            return
        cursor.execute("""
            DELETE FROM client
            WHERE client_email = ?;
        """, (client_email,))
        print("Removing this client...")
        conn.commit()

def display_top_k_clients(k):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.client_name, c.client_email, COUNT(b.booking_id) as booking_count
            FROM client c
            LEFT JOIN booking b ON c.client_email = b.client_email
            GROUP BY c.client_email
            ORDER BY booking_count DESC
            LIMIT ?;
        """, (k,))
        clients = cursor.fetchall()
        if not clients:
            print("No clients found.")
            return
        for client in clients:
            print(f"Name: {client[0]}, Email: {client[1]}")


def display_hotel_bookings():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.hotel_name, r.room_num, COUNT(b.booking_id) AS booking_count
            FROM hotel h
            JOIN room r ON h.hotel_id = r.hotel_id
            LEFT JOIN booking b ON r.hotel_id = b.hotel_id AND r.room_num = b.room_num
            GROUP BY h.hotel_id, r.room_num
            ORDER BY h.hotel_id, r.room_num;
        """)
        rooms = cursor.fetchall()
        if not rooms:
            print("No hotel room bookings found.")
            return
        for hotel_name, room_num, booking_count in rooms:
            print(f"Hotel: {hotel_name}, Room: {room_num}, Bookings: {booking_count}")


def display_hotel_stats():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.hotel_name, h.hotel_id,
                   COALESCE(b.booking_count, 0) AS bookings,
                   r.average_rating
            FROM hotel h
            LEFT JOIN (
                SELECT hotel_id, COUNT(*) AS booking_count
                FROM booking
                GROUP BY hotel_id
            ) b ON h.hotel_id = b.hotel_id
            LEFT JOIN (
                SELECT hotel_id, ROUND(AVG(rating), 2) AS average_rating
                FROM review
                GROUP BY hotel_id
            ) r ON h.hotel_id = r.hotel_id
            ORDER BY h.hotel_name;
        """)
        hotels = cursor.fetchall()
        if not hotels:
            print("No hotel stats found.")
            return
        for hotel_name, hotel_id, bookings, average_rating in hotels:
            avg_display = average_rating if average_rating is not None else "N/A"
            print(f"Hotel: {hotel_name} (ID: {hotel_id}), Bookings: {bookings}, Average Rating: {avg_display}")


def display_clients_in_cities(c1, c2):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT c.client_name, c.client_email
            FROM client c
            JOIN client_address ca ON c.client_email = ca.client_email
            JOIN booking b ON c.client_email = b.client_email
            JOIN hotel h ON b.hotel_id = h.hotel_id
            WHERE ca.city = ?
              AND h.city = ?;
        """, (c1, c2))
        clients = cursor.fetchall()
        if not clients:
            print("No matching clients found.")
            return
        for client_name, client_email in clients:
            print(f"Name: {client_name}, Email: {client_email}")


def display_problematic_hotels():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.hotel_name, h.hotel_id, ROUND(AVG(r.rating), 2) AS average_rating,
                   COUNT(DISTINCT b.client_email) AS distinct_non_chicago_clients
            FROM hotel h
            JOIN review r ON h.hotel_id = r.hotel_id
            JOIN booking b ON h.hotel_id = b.hotel_id
            WHERE h.city = 'Chicago'
              AND NOT EXISTS (
                  SELECT 1
                  FROM client_address ca
                  WHERE ca.client_email = b.client_email
                    AND ca.city = 'Chicago'
              )
            GROUP BY h.hotel_id
            HAVING average_rating < 2
               AND distinct_non_chicago_clients >= 2;
        """)
        hotels = cursor.fetchall()
        if not hotels:
            print("No problematic hotels found.")
            return
        for hotel_name, hotel_id, average_rating, distinct_clients in hotels:
            print(f"Hotel: {hotel_name} (ID: {hotel_id}), Average Rating: {average_rating}, Non-Chicago Clients: {distinct_clients}")


def display_client_spending():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.client_name,
                   COALESCE(SUM(b.price_per_day * (julianday(b.end_date) - julianday(b.start_date))), 0) AS total_spent
            FROM client c
            LEFT JOIN booking b ON c.client_email = b.client_email
            GROUP BY c.client_email
            ORDER BY total_spent DESC;
        """)
        clients = cursor.fetchall()
        if not clients:
            print("No client spending data found.")
            return
        for client_name, total_spent in clients:
            print(f"Name: {client_name}, Total Spent: ${total_spent:.2f}")


def update_client_name(old_email, new_name):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM client WHERE client_email = ?;""", (old_email,))
        if cursor.fetchone() is None:
            print("Client not found.")
            return
        cursor.execute("""
            UPDATE client
            SET client_name = ?
            WHERE client_email = ?;
        """, (new_name, old_email))
        print("Updating client name...")
        conn.commit()

def add_credit_card(credit_card_num, client_email, city, address_num, street_name):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO credit_card (credit_card_num, client_email, city, address_num, street_name)
            VALUES (?, ?, ?, ?, ?);
        """, (credit_card_num, client_email, city, address_num, street_name))
        conn.commit()

def update_credit_card(old_num, new_num):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM credit_card WHERE credit_card_num = ?;""", (old_num,))
        if cursor.fetchone() is None:
            print("Credit card not found.")
            return
        cursor.execute("""
            UPDATE credit_card
            SET credit_card_num = ?
            WHERE credit_card_num = ?;
        """, (new_num, old_num))
        conn.commit()
        print("Updating credit card number...")

def add_address(city, address_num, street_name):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO address (city, address_num, street_name)
            VALUES (?, ?, ?);
        """, (city, address_num, street_name))
        conn.commit()

def update_address(city, address_num, street_name, new_city, new_address_num, new_street_name):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM address WHERE city = ? AND address_num = ? AND street_name = ?;""", (city, address_num, street_name))
        if cursor.fetchone() is None:
            print("Address not found.")
            return
        cursor.execute("""
            UPDATE address
            SET city = ?, address_num = ?, street_name = ?
            WHERE city = ? AND address_num = ? AND street_name = ?;
        """, (new_city, new_address_num, new_street_name, city, address_num, street_name))
        conn.commit()
        print("Updating address...")

def add_manager(manager_name, manager_email, ssn):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO manager (manager_name, manager_email, ssn)
            VALUES (?, ?, ?);
        """, (manager_name, manager_email, ssn))
        conn.commit()


def add_hotel(hotel_name, hotel_id, city, address_num, street_name):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO hotel (hotel_name, hotel_id, city, address_num, street_name)
            VALUES (?, ?, ?, ?, ?);
        """, (hotel_name, hotel_id, city, address_num, street_name))
        conn.commit()

def remove_hotel(hotel_id):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM hotel WHERE hotel_id = ?;""", (hotel_id,))
        if cursor.fetchone() is None:
            print("Hotel not found.")
            return
        cursor.execute("""
            DELETE FROM hotel
            WHERE hotel_id = ?;
        """, (hotel_id,))
        print("Removing this hotel...")
        conn.commit()

def update_hotel(hotel_id, new_name):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM hotel WHERE hotel_id = ?;""", (hotel_id,))
        if cursor.fetchone() is None:
            print("Hotel not found.")
            return
        cursor.execute("""
            UPDATE hotel
            SET hotel_name = ?
            WHERE hotel_id = ?;
        """, (new_name, hotel_id))
        print("Updating hotel information...")
        conn.commit()

def add_room(room_num, num_windows, last_renov_year, accessible, hotel_id):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO room (room_num, num_windows, last_renov_year, accessible, hotel_id)
            VALUES (?, ?, ?, ?, ?);
        """, (room_num, num_windows, last_renov_year, accessible, hotel_id))
        conn.commit()

def remove_room(hotel_id, room_num):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM room WHERE hotel_id = ? AND room_num = ?;""", (hotel_id, room_num))
        if cursor.fetchone() is None:
            print("Room not found.")
            return
        cursor.execute("""
            DELETE FROM room
            WHERE hotel_id = ? AND room_num = ?;
        """, (hotel_id, room_num))
        print("Removing this room...")
        conn.commit()

def update_room(hotel_id, room_num, new_num_windows, new_last_renov_year, new_accessible):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM room WHERE hotel_id = ? AND room_num = ?;""", (hotel_id, room_num))
        if cursor.fetchone() is None:
            print("Room not found.")
            return
        cursor.execute("""
            UPDATE room
            SET num_windows = ?, last_renov_year = ?, accessible = ?
            WHERE hotel_id = ? AND room_num = ?;
        """, (new_num_windows, new_last_renov_year, new_accessible, hotel_id, room_num))
        print("Updating room information...")
        conn.commit()
        

def add_booking(booking_id, price_per_day, start_date, end_date, client_email, room_num, hotel_id):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO booking (booking_id, price_per_day, start_date, end_date, client_email, room_num, hotel_id)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (booking_id, price_per_day, start_date, end_date, client_email, room_num, hotel_id))
        conn.commit()

def add_review(rating, review_message, review_id, hotel_id, client_email):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        # Check if client exists
        cursor.execute("SELECT * FROM client WHERE client_email = ?;", (client_email,))
        if cursor.fetchone() is None:
            print("Client not found.")
            return       
        # Check if client has previously stayed at this hotel (has a booking)
        cursor.execute("""
            SELECT * FROM booking 
            WHERE client_email = ? AND hotel_id = ?;
        """, (client_email, hotel_id))
        if cursor.fetchone() is None:
            print("You may only review hotels that you've stayed at!")
            return     
        cursor.execute("""
            INSERT INTO review (rating, review_message, review_id, hotel_id, client_email)
            VALUES (?, ?, ?, ?, ?);
        """, (rating, review_message, review_id, hotel_id, client_email))
        print("Submitting a review...")
        conn.commit()

def add_client_address(client_email, city, address_num, street_name):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO client_address (client_email, city, address_num, street_name)
            VALUES (?, ?, ?, ?);
        """, (client_email, city, address_num, street_name))
        conn.commit()

def update_client_address(client_email, city, address_num, street_name, new_city, new_address_num, new_street_name):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM client_address WHERE client_email = ? AND city = ? AND address_num = ? AND street_name = ?;""", (client_email, city, address_num, street_name))
        if cursor.fetchone() is None:
            print("Client address not found.")
            return
        cursor.execute("""
            UPDATE client_address
            SET city = ?, address_num = ?, street_name = ?
            WHERE client_email = ? AND city = ? AND address_num = ? AND street_name = ?;
        """, (new_city, new_address_num, new_street_name, client_email, city, address_num, street_name))
        print("Updating client address...")
        conn.commit()

def add_manages(ssn, hotel_id):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO manages (ssn, hotel_id)
            VALUES (?, ?);
        """, (ssn, hotel_id))
        conn.commit()

def update_manages(ssn, hotel_id, new_hotel_id):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE manages
            SET hotel_id = ?
            WHERE ssn = ? AND hotel_id = ?;
        """, (new_hotel_id, ssn, hotel_id))
        conn.commit()

def login_manager(ssn):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT manager_name FROM manager WHERE ssn = ?;
        """, (ssn,))
        result = cursor.fetchone()
        return result[0] if result else None

def login_client(email):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT client_name FROM client WHERE client_email = ?;
        """, (email,))
        result = cursor.fetchone()
        return result[0] if result else None

# Automatic Booking Functions

def get_next_booking_id():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(booking_id) FROM booking;")
        result = cursor.fetchone()
        return (result[0] + 1) if result[0] is not None else 1

def get_available_rooms_in_hotel(hotel_id, start_date, end_date):
    """
    Get all available rooms in a specific hotel for a date range.
    Returns list of (room_num, num_windows, last_renov_year, accessible) tuples.
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.room_num, r.num_windows, r.last_renov_year, r.accessible
            FROM room r
            WHERE r.hotel_id = ?
              AND NOT EXISTS (
                  SELECT 1 FROM booking b
                  WHERE b.hotel_id = r.hotel_id
                    AND b.room_num = r.room_num
                    AND NOT (b.end_date <= ? OR b.start_date >= ?)
              )
            ORDER BY r.room_num;
        """, (hotel_id, start_date, end_date))
        return cursor.fetchall()

def get_hotels_with_available_rooms(start_date, end_date):
    """
    Get all hotels that have at least one available room for a date range.
    Returns list of (hotel_id, hotel_name, city) tuples.
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT h.hotel_id, h.hotel_name, h.city
            FROM hotel h
            WHERE EXISTS (
                SELECT 1 FROM room r
                WHERE r.hotel_id = h.hotel_id
                  AND NOT EXISTS (
                      SELECT 1 FROM booking b
                      WHERE b.hotel_id = r.hotel_id
                        AND b.room_num = r.room_num
                        AND NOT (b.end_date <= ? OR b.start_date >= ?)
                  )
            )
            ORDER BY h.hotel_name;
        """, (start_date, end_date))
        return cursor.fetchall()

def get_hotel_info(hotel_id):
    """Get hotel information by ID"""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT hotel_id, hotel_name, city, address_num, street_name
            FROM hotel
            WHERE hotel_id = ?;
        """, (hotel_id,))
        return cursor.fetchone()

def get_room_details(hotel_id, room_num):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT room_num, num_windows, last_renov_year, accessible
            FROM room
            WHERE hotel_id = ? AND room_num = ?;
        """, (hotel_id, room_num))
        return cursor.fetchone()
    
def get_booking_price(hotel_id, room_num):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT price_per_day
            FROM booking
            WHERE hotel_id = ? AND room_num = ?;
        """, (hotel_id, room_num))
        
        result = cursor.fetchone()
        return result[0] if result else None

def get_client_bookings(client_email):
    """
    Get all bookings for a specific client including room, hotel name, and cost.
    Returns list of (booking_id, hotel_name, room_num, start_date, end_date, price_per_day, total_cost) tuples.
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.booking_id, h.hotel_name, b.room_num, b.start_date, b.end_date, b.price_per_day,
                   (b.price_per_day * (julianday(b.end_date) - julianday(b.start_date))) AS total_cost
            FROM booking b
            JOIN hotel h ON b.hotel_id = h.hotel_id
            WHERE b.client_email = ?
            ORDER BY b.start_date DESC;
        """, (client_email,))
        return cursor.fetchall()


            

