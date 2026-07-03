from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# ==========================================================
# Load Environment Variables
# ==========================================================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# ==========================================================
# Gemini Client
# ==========================================================
client = genai.Client(api_key=API_KEY)

# ==========================================================
# Flask App
# ==========================================================
app = Flask(__name__)

# ==========================================================
# AI Personality / System Prompt
# ==========================================================
SYSTEM_PROMPT = """
You are an intelligent AI assistant created by RAZZ SINGH using Google's Gemini API.

Your personality:

- Friendly
- Professional
- Helpful
- Honest
- Clear and concise

Rules:

1. Always answer in Markdown.
2. Explain concepts step-by-step.
3. When writing code:
   - Provide complete working code.
   - Add comments.
   - Follow best practices.
4. Never invent facts.
5. If you don't know the answer, admit it.
6. If the user asks programming questions, act like a senior software engineer.
7. If the user asks DSA questions, explain intuitively first, then give code.
8. Format code inside Markdown code blocks.
9. Keep responses clean and readable.
10. If asked to compare technologies, provide a table.

Your goal is to teach, not just answer.
"""

# ==========================================================
# Store Chat History
# (Temporary - resets when server restarts)
# ==========================================================
chat_history = []

# ==========================================================
# Home Page
# ==========================================================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================================================
# Chat Endpoint
# ==========================================================
@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "reply": "Please enter a message."
            })

        # ---------------------------------------------
        # Save User Message
        # ---------------------------------------------
        chat_history.append({
            "role": "user",
            "text": user_message
        })

        # ---------------------------------------------
        # Convert History into Conversation
        # ---------------------------------------------
        conversation = []

        for msg in chat_history:
            conversation.append(
                types.Content(
                    role=msg["role"],
                    parts=[
                        types.Part(text=msg["text"])
                    ]
                )
            )

        # ---------------------------------------------
        # Generate Response
        # ---------------------------------------------
        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=conversation,

            config=types.GenerateContentConfig(

                system_instruction=SYSTEM_PROMPT,

                temperature=0.7,

                top_p=0.95,

                max_output_tokens=2048

            )

        )

        ai_reply = response.text

        # ---------------------------------------------
        # Save AI Response
        # ---------------------------------------------
        chat_history.append({
            "role": "model",
            "text": ai_reply
        })

        return jsonify({
            "reply": ai_reply
        })

    except Exception as e:

        return jsonify({
            "reply": str(e)
        })


# ==========================================================
# Clear Chat
# ==========================================================
@app.route("/clear", methods=["POST"])
def clear_chat():

    chat_history.clear()

    return jsonify({
        "message": "Chat Cleared"
    })


# ==========================================================
# Run App
# ==========================================================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )