from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import google.generativeai as genai

# Configure API
genai.configure(api_key="AIzaSyAZkl5WmOOF0_u-NU76Z4DT5CfG8VeUM2Q")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create model object
model = genai.GenerativeModel("models/gemini-2.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    return chat.send_message(question, stream=True)

# Streamlit UI
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.header("🤖 Gemini Chatbot")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("INPUT:")
submit = st.button("SUBMIT")

if submit and user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    response = get_gemini_response(user_input)

    full_response = ""
    for chunk in response:
        if chunk.text:
            st.write(chunk.text)
            full_response += chunk.text

    st.session_state.chat_history.append(
        {"role": "assistant", "content": full_response}
    )

# Display chat history
st.subheader("Chat History")
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**User:** {chat['content']}")
    else:
        st.markdown(f"**Gemini:** {chat['content']}")
