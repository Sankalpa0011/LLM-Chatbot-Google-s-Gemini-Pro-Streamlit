import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# load environment variebles
load_dotenv()

# configure streamlit page settings
st.set_page_config(
    page_title = "Chat With Gemini-Pro!",
    page_icon=":brain:",   # Favicon emoji
    layout="centered",     # page layout option
)

GOOGLE_API_KEY =  os.getenv("GOOGLE_API_KEY")

#  set up Google Gemini Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-pro")


# function to translate roles between Gemini Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    
# initialize chat session in streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# display the chatbot's title on the page
st.title("🤖 Gemini Pro - ChatBot")

# display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# input field for user's message
user_prompt = st.chat_input("Ask Gemini Pro...")
if user_prompt:
    # add user's message to chat and display
    st.chat_message("user").markdown(user_prompt)

    # send user's message to Gemin Pro and the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # display Gemini Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)