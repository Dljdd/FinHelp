from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.title("💸Fintessa")

# Initialize chat history in session state if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display existing messages in chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Your question:")

if prompt:
    if not openai_api_key:
        st.error("Please add your OpenAI API key to continue.")
        st.stop()

    # Append user's prompt to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)  # Display user's prompt in the chat

    client = OpenAI(api_key=openai_api_key)

    # Make the API call to OpenAI to get the chatbot's response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": msg["role"], "content": msg["content"]} for msg in st.session_state["messages"]]
    )

    if response.choices:
        msg = response.choices[0].message.content  # Access the chatbot's response content

        # Simulate typing for the chatbot's response
        full_response = ""
        message_placeholder = st.empty()
        for chunk in msg.split():
            full_response += chunk + " "
            time.sleep(0.05)  # Simulate typing delay
            message_placeholder.markdown(full_response + "▌")  # Show typing effect with blinking cursor

        # Display the full message without the blinking cursor
        message_placeholder.markdown(full_response)

        # Append assistant's response to session state
        st.session_state.messages.append({"role": "assistant", "content": msg})
