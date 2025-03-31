import streamlit as st
import requests
import json
import datetime
import os

# Backend API URL
API_URL = "https://f13e-34-16-186-60.ngrok-free.app"

# Ensure the directory exists
history_file = "data/chat_history.json"
os.makedirs(os.path.dirname(history_file), exist_ok=True)

# Load chat history from JSON file
def load_chat_history():
    try:
        with open(history_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save chat history to JSON file
def save_chat_history(history):
    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)

# Streamlit UI
st.title("💬 Mamba Chatbot")

# Load chat history into session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

# Display chat history using chat messages
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(f"**You ({chat['timestamp']}):** {chat['user']}")
    with st.chat_message("assistant"):
        st.markdown(f"**Bot ({chat['timestamp']}):** {chat['bot']}")

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    with st.chat_message("user"):
        st.markdown(f"**You:** {user_input}")
    
    try:
        response = requests.post(f"{API_URL}/chat/", json={"user_input": user_input})
        if response.status_code == 200:
            bot_reply = response.json()
            
            # Use API timestamp if available, otherwise generate one
            timestamp = bot_reply.get("timestamp", datetime.datetime.now().isoformat())

            message_entry = {
                "timestamp": timestamp,
                "user": user_input,
                "bot": bot_reply["response"]
            }
            st.session_state.chat_history.append(message_entry)
            save_chat_history(st.session_state.chat_history)
            
            with st.chat_message("assistant"):
                st.markdown(f"**Bot:** {bot_reply['response']}")
        else:
            st.error("Failed to connect to chatbot API.")
    except requests.exceptions.RequestException:
        st.error("Error connecting to the chatbot backend.")

# Clear chat history
if st.button("Clear Chat"):
    requests.delete(f"{API_URL}/clear_history/")
    st.session_state.chat_history = []
    save_chat_history([])
    st.rerun()
