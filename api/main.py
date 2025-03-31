from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json
import os

# Initialize FastAPI app
app = FastAPI()

# Path for storing chat history
HISTORY_FILE = "data/chat_history.json"

# Ensure the history file exists
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

# Request model
class ChatRequest(BaseModel):
    user_input: str

# Load chat history
def load_chat_history():
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

# Save chat history
def save_chat_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# Simple response function (Placeholder for AI model)
def generate_response(user_input):
    return f"Echo: {user_input}"  # Replace with Mamba model later

# Chat API endpoint
@app.post("/chat/")
def chat(request: ChatRequest):
    chat_history = load_chat_history()
    response = generate_response(request.user_input)

    message_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": request.user_input,
        "bot": response
    }

    chat_history.append(message_entry)
    save_chat_history(chat_history)

    return {"response": response, "timestamp": message_entry["timestamp"]}

# Endpoint to clear chat history
@app.delete("/clear_history/")
def clear_history():
    save_chat_history([])
    return {"message": "Chat history cleared"}
