import logging
import os

import streamlit as st
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from utils import extract_context, prompt_chat

logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=".env")


st.title("Cocktail")

api_key = os.getenv("API_KEY")
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)


if "openai_model" not in st.session_state:
    st.session_state["mistral_model"] = "mistral-large-latest"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        context = extract_context(st.session_state.messages)
        engineered_chat = prompt_chat(prompt, context)
        print(engineered_chat)
        for response in client.chat_stream(
            model=st.session_state["mistral_model"],
            messages=[ChatMessage(role="user", content=engineered_chat)],
        ):
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "|")

        message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
