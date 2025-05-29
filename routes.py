from flask import Blueprint, Flask, request, render_template, redirect, url_for
import psycopg2

routes = Blueprint('routes', __name__)

# PostgreSQL connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname="postgres",
    user="postgres",
    password="123",
    host="localhost",
    )
    return conn

@routes.route('/')
def index():
    return '<h2>Welcome! Go to /add_user, /add_event, /add_firm, etc. to insert data.</h2>'

# --- USER ---
@routes.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        city = request.form['city']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO "User" (user_name, user_email, user_contact, user_city)
            VALUES (%s, %s, %s, %s)
        ''', (name, email, contact, city))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('index2.html')

# --- EVENT ---
@routes.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']
        flyer = request.form['flyer']
        rating = request.form['rating']
        city = request.form['city']
        address = request.form['address']
        layout = request.form['layout']
        firm_id = request.form['firm_id']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Event (event_name, event_type, event_description, event_date, event_time, 
                               event_flyer, event_rating, event_city, event_address, event_layout, firm_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (name, type_, description, date, time, flyer, rating, city, address, layout, firm_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('event.html')

# --- FIRM ---
@routes.route('/add_firm', methods=['GET', 'POST'])
def add_firm():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        bio = request.form['bio']
        logo = request.form['logo']
        organizer_id = request.form['organizer_id']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO firm (firm_name, firm_type, firm_bio, firm_logo, organizer_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, type_, bio, logo, organizer_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('firm.html')

