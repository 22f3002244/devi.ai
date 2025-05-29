from flask import Flask, render_template, request
from google import genai
import re
import datetime
import markdown
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey123'

# Gemini client setup
client = genai.Client(api_key="AIzaSyABHPfU3dSKY79OscpoyTOdKF4nQWuQoTg")

# Jinja2 environment for custom template-based prompts
jinja_env = Environment(loader=FileSystemLoader("templates"))

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    formatted = ""
    user_text = ""

    if request.method == "POST":
        user_text = request.form.get("user_input")

        # Use Jinja2 to render prompt from template
        template = jinja_env.get_template("prompt_template.txt")
        prompt = template.render(text=user_text)

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
