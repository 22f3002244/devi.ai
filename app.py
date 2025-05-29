from flask import Flask, render_template, request, redirect, url_for
from google import genai
import re
from datetime import datetime
import markdown
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import os
from routes import get_db_connection, routes

def fetch_full_database():
    conn = get_db_connection()
    cur = conn.cursor()

    # Step 1: Get all table names from public schema
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()

    full_data = {}

    # Step 2: For each table, fetch all rows and column names
    for table in tables:
        table_name = table[0]
        cur.execute(f'SELECT * FROM "{table_name}"')  # quotes preserve case sensitivity
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        full_data[table_name] = [dict(zip(colnames, row)) for row in rows]

    cur.close()
    conn.close()

    return full_data

def serialize_data(obj):
    if isinstance(obj, dict):
        return {k: serialize_data(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_data(v) for v in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey123'

app.register_blueprint(routes)

load_dotenv()  # Load variables from .env file
key = os.getenv("KEY")

# Gemini client setup
client = genai.Client(api_key=key)

# Jinja2 environment for custom template-based prompts
jinja_env = Environment(loader=FileSystemLoader("templates"))

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    formatted = ""
    user_text = ""

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = fetch_full_database()
    data_serialized = serialize_data(data)

    if request.method == "POST":
        user_text = request.form.get("user_input")

        # Use Jinja2 to render prompt from template
        template = jinja_env.get_template("prompt_template.txt")
        prompt = template.render(text=user_text, datetime=now, data=data_serialized)

        # Send to Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        response_text = response.text
        formatted = markdown.markdown(response_text)

    return render_template("index.html", response = formatted, user_input=user_text)

if __name__ == "__main__":
    app.run(debug=True)
