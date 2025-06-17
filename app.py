import google.generativeai as genai
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, session

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("api_key")
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Configure Gemini - NEW SYNTAX
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')  

safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"}
]

@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize chat history
    if "messages" not in session:
        session["messages"] = []
    
    if request.method == "POST":
        user_input = request.form["message"]
        
        # Create prompt with chat history
        prompt = """You are Captain Blackbeard, a sarcastic pirate. 
        Never break character. Respond to all messages as a pirate would.
        Previous conversation:\n"""
        
        for msg in session["messages"]:
            prompt += f"{msg['role']}: {msg['content']}\n"
            
        prompt += f"User: {user_input}\nPirate: "
# Get response
        try:
            response = model.generate_content(
                prompt,
                safety_settings=safety_settings
            )
            pirate_response = response.text
        except Exception as e:
            pirate_response = f"Arrr! The parrot ate me response! ({str(e)})"
        
        # Update session
        session["messages"].extend([
            {"role": "user", "content": user_input},
            {"role": "pirate", "content": pirate_response}
        ])
        session.modified = True
    
    return render_template("index.html", messages=session["messages"])

if __name__ == "__main__":
    app.run(debug=True)
