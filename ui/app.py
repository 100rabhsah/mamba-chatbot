import streamlit as st
import requests
import json

# Backend API URL
API_URL = "http://backend:8000"

# Load chat history from JSON file
def load_chat_history():
    try:
        with open("data/chat_history.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save chat history to JSON file
def save_chat_history(history):
    with open("data/chat_history.json", "w") as f:
        json.dump(history, f, indent=4)

# Streamlit UI
st.title("💬 Mamba Chatbot")

# Load chat history into session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

# Display chat history
for chat in st.session_state.chat_history:
    st.text_area(f"You ({chat['timestamp']})", value=chat["user"], height=70, disabled=True)
    st.text_area(f"Bot ({chat['timestamp']})", value=chat["bot"], height=70, disabled=True)

# User input
user_input = st.text_input("Type your message:")

if st.button("Send"):
    if user_input.strip():
        # Send message to FastAPI backend
        response = requests.post(f"{API_URL}/chat/", json={"user_input": user_input})
        if response.status_code == 200:
            bot_reply = response.json()
            message_entry = {
                "timestamp": bot_reply["timestamp"],
                "user": user_input,
                "bot": bot_reply["response"]
            }
            st.session_state.chat_history.append(message_entry)
            save_chat_history(st.session_state.chat_history)
            st.rerun()

# Clear chat history
if st.button("Clear Chat"):
    requests.delete(f"{API_URL}/clear_history/")
    st.session_state.chat_history = []
    save_chat_history([])
    st.rerun()
