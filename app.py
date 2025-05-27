from flask import Flask, render_template, request
from google import genai
import re
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey123'

# Gemini client setup
client = genai.Client(api_key="")

# Jinja2 environment for custom template-based prompts
jinja_env = Environment(loader=FileSystemLoader("templates"))

def format_gemini_response(response_text, bold_mode='upper'):
    """
    Format Gemini response for plain text output (not HTML).
    
    Parameters:
    - response_text: str - raw text from Gemini
    - bold_mode: str - 'upper', 'keep', or 'none' (default 'upper')
    
    Returns:
    - str - nicely formatted plain text
    """

    # Handle bold formatting
    if bold_mode == 'upper':
        response_text = re.sub(r'\*\*(.+?)\*\*', lambda m: m.group(1).upper(), response_text)
    elif bold_mode == 'keep':
        # Keep as markdown-style bold
        response_text = re.sub(r'\*\*(.+?)\*\*', r'**\1**', response_text)
    else:
        # Strip bold
        response_text = re.sub(r'\*\*(.+?)\*\*', r'\1', response_text)

    # Process line by line
    lines = response_text.strip().splitlines()
    formatted_lines = []
    in_list = False

    for line in lines:
        stripped = line.strip()

        # Bullet points
        if re.match(r"^[-*]\s", stripped):
            if not in_list:
                in_list = True
            item = re.sub(r"^[-*]\s", "", stripped)
            formatted_lines.append(f"• {item}")
        else:
            if in_list:
                in_list = False
                formatted_lines.append(" ")  # add space after list
            else:
                formatted_lines.append(stripped)

    # Clean up: remove extra leading/trailing empty lines
    while formatted_lines and formatted_lines[0] == "":
        formatted_lines.pop(0)
    while formatted_lines and formatted_lines[-1] == "":
        formatted_lines.pop()

    return "\n".join(formatted_lines)


@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    formatted = ""

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
        formatted = format_gemini_response(response_text)

    return render_template("index.html", response = formatted)

if __name__ == "__main__":
    app.run(debug=True)
