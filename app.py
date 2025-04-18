import streamlit as st
import requests
import json
import time

# Set page configuration
st.set_page_config(
    page_title="Sports Performance Analyzer",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
API_KEY = "AIzaSyBQk6oB1HV0v7Uc99sAtw_4CbpubToUXcM"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Custom CSS for better UI
st.markdown("""
    <style>
        .stTextInput input {
            border-radius: 20px;
            padding: 10px 15px;
        }
        .stButton button {
            border-radius: 20px;
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            border: none;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .chat-message {
            padding: 12px 16px;
            border-radius: 18px;
            margin: 8px 0;
            max-width: 80%;
        }
        .user-message {
            background-color: #e3f2fd;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }
        .bot-message {
            background-color: #f1f1f1;
            margin-right: auto;
            border-bottom-left-radius: 5px;
        }
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar with app info and sport selection
with st.sidebar:
    st.title("🏆 Sports Analyzer")
    st.markdown("""
        **Get expert analysis on:**  
        - Player performance metrics  
        - Team strategies  
        - Training optimization  
        - Injury prevention  
        - Game statistics  
    """)
    
    selected_sport = st.selectbox(
        "Select your sport:",
        ("Football", "Basketball", "Tennis", "Cricket", "Swimming", "Athletics", "Other")
    )
    
    st.markdown("---")
    st.markdown("💡 **Tip:** Ask specific questions for better analysis")
    st.markdown("Example: *'How can I improve my shooting accuracy in basketball?'*")

# Main app area
st.title(f"🏅 {selected_sport} Performance Analyzer")
st.caption("Powered by Gemini AI - Ask me anything about sports performance!")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message["content"]}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>Coach:</strong> {message["content"]}
            </div>
        """, unsafe_allow_html=True)

# Function to call Gemini API
def generate_response(prompt):
    payload = {
        "contents": [{
            "parts": [{
                "text": f"You are a {selected_sport} performance analyst. Provide detailed, technical but understandable advice. {prompt}"
            }]
        }]
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Chat input
user_input = st.chat_input("Ask your sports performance question...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate and display bot response
    with st.spinner("Analyzing your performance..."):
        bot_response = generate_response(user_input)
        st.session_state.chat_history.append({"role": "bot", "content": bot_response})
        
        with st.chat_message("assistant"):
            st.markdown(bot_response)