import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# SQL commands
commands = [

    # User table
    '''
    CREATE TABLE "User" (
        user_id SERIAL PRIMARY KEY,
        user_name VARCHAR(100),
        user_email VARCHAR(100),
        user_contact VARCHAR(20),
        user_city VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''',

    # Organizer table
    '''
    CREATE TABLE Organizer (
        organizer_id SERIAL PRIMARY KEY,
        organizer_name VARCHAR(100),
        organizer_email VARCHAR(100),
        organizer_contact VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''',

    # Firm table
    '''
    CREATE TABLE firm (
        firm_id SERIAL PRIMARY KEY,
        firm_name VARCHAR(100),
        firm_type VARCHAR(50),
        firm_bio TEXT,
        firm_logo TEXT,
        organizer_id INT,
        FOREIGN KEY (organizer_id) REFERENCES Organizer(organizer_id)
    );
    ''',

    # Social Media table
    '''
    CREATE TABLE social_media (
        social_id SERIAL PRIMARY KEY,
        firm_id INT,
        social_platform VARCHAR(50),
        link TEXT,
        icon TEXT,
        FOREIGN KEY (firm_id) REFERENCES firm(firm_id)
    );
    ''',

    # Event table
    '''
    CREATE TABLE Event (
        event_id SERIAL PRIMARY KEY,
        event_name VARCHAR(100),
        event_type VARCHAR(50),
        event_description TEXT,
        event_date DATE,
        event_time TIME,
        event_flyer TEXT,
        event_rating FLOAT,
        event_city VARCHAR(50),
        event_address TEXT,
        event_layout TEXT,
        firm_id INT,
        FOREIGN KEY (firm_id) REFERENCES firm(firm_id)
    );
    ''',

    # Tickets_category table
    '''
    CREATE TABLE Tickets_category (
        category_id SERIAL PRIMARY KEY,
        event_id INT,
        category_name VARCHAR(100),
        category_price DECIMAL(10, 2),
        category_available INT,
        category_description TEXT,
        FOREIGN KEY (event_id) REFERENCES Event(event_id)
    );
    ''',

    # Cart table
    '''
    CREATE TABLE cart (
        cart_id SERIAL PRIMARY KEY,
        user_id INT,
        event_id INT,
        category_id INT,
        quantity INT,
        total_amount DECIMAL(10, 2),
        payment_pending BOOLEAN,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id),
        FOREIGN KEY (event_id) REFERENCES Event(event_id),
        FOREIGN KEY (category_id) REFERENCES Tickets_category(category_id)
    );
    ''',

    # Booking History
    '''
    CREATE TABLE booking_history (
        booking_id SERIAL PRIMARY KEY,
        cart_id INT,
        datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cart_id) REFERENCES cart(cart_id)
    );
    ''',

    # Attendees
    '''
    CREATE TABLE attendees (
        attendee_id SERIAL PRIMARY KEY,
        booking_id INT,
        attendee_name VARCHAR(100),
        FOREIGN KEY (booking_id) REFERENCES booking_history(booking_id)
    );
    ''',

    # Comments
    '''
    CREATE TABLE Comments (
        comment_id SERIAL PRIMARY KEY,
        event_id INT,
        user_id INT,
        user_feedback TEXT,
        FOREIGN KEY (event_id) REFERENCES Event(event_id),
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    );
    ''',

    # Image Gallery
    '''
    CREATE TABLE Image_Gallery (
        gallery_id SERIAL PRIMARY KEY,
        event_id INT,
        gallery_image TEXT,
        FOREIGN KEY (event_id) REFERENCES Event(event_id)
    );
    '''
]

# Execute SQL commands
for command in commands:
    cur.execute(command)

# Commit and close
conn.commit()
cur.close()
conn.close()

print("Database schema created successfully.")
