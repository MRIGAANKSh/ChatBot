import streamlit as st
import google.generativeai as genai

# Configure Streamlit page settings
st.set_page_config(
    page_title="MAX CHATBOT",
    page_icon="🤖",
    layout="centered",
)

# Set your Google API Key
GOOGLE_API_KEY = "AIzaSyDPunydE5plFzENEPjY63KO2rLmzBk14KM"  # Replace with your actual API key

# Configure API Key
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"Error configuring API key: {e}")
    st.stop()

# Load Gemini-Pro model
try:
    model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# Function to map roles for Streamlit chat format
def translate_role(role):
    return "assistant" if role == "model" else role

# Initialize chat session
if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Error initializing chat session: {e}")
        st.stop()

# Display chatbot title
st.title("🤖💬 MAX - A ChatBot")

# Show chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role(message.role)):
        st.markdown(message.parts[0].text)

# Get user input
user_prompt = st.chat_input("Ask Max...")
if user_prompt:
    # Display user input in chat
    st.chat_message("user").markdown(user_prompt)

    # Get AI response
    try:
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    except Exception as e:
        st.error(f"Error getting response: {e}")
