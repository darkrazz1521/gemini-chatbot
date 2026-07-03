from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

# --------------------------------------------------
# Load environment variables from .env
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# Read Gemini API Key
# --------------------------------------------------
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# --------------------------------------------------
# Initialize Gemini Client
# --------------------------------------------------
client = genai.Client(api_key=API_KEY)

# --------------------------------------------------
# Create Flask App
# --------------------------------------------------
app = Flask(__name__)

# --------------------------------------------------
# Home Route
# Opens index.html
# --------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Chat Route
# Receives message from frontend
# Sends it to Gemini
# Returns response as JSON
# --------------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        user_message = data.get("message", "")

        if user_message.strip() == "":
            return jsonify({
                "reply": "Please enter a message."
            })

        # Generate response using Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )

        ai_reply = response.text

        return jsonify({
            "reply": ai_reply
        })

    except Exception as e:

        return jsonify({
            "reply": f"Error : {str(e)}"
        })


# --------------------------------------------------
# Run Flask App
# --------------------------------------------------
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )