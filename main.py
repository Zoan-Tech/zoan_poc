from action.init import init
init()

import streamlit as st
from action.agent import game_suggestion
from action.agent import game
from constant import Constant
import os

def get_history():
    history = ""
    try:
        with open(Constant.HISTORY_FILE.value, "r") as f:
            history = f.read()
    except FileNotFoundError:
        print("History file not found. Creating a new one.")
    return history

st.set_page_config(
    page_title="Game Generator",
    page_icon=":game_die:",
)

generated_img_dir = Constant.GENERATED_IMG.value
history_file = Constant.HISTORY_FILE.value

# Track generator change
if "prev_generator" not in st.session_state:
    st.session_state.prev_generator = "Assest Generator"

selected_generator = st.selectbox(
    "Select a generator",
    options=[
        "Assest Generator",
        "Game Generator",
    ],
    index=0,
)

# Reset chat if generator changed
if selected_generator != st.session_state.prev_generator:
    st.session_state.messages = []
    st.session_state.prev_generator = selected_generator
    with open(history_file, "w") as f:
        f.write("")



generator = game.GameGenerator(
    modules=game.modules,
    model_name=Constant.GEMINI_FLASH.value,
    mode="google"
) if selected_generator == "Game Generator" else game_suggestion.GameSuggestor(
    modules=game_suggestion.modules,
    model_name=Constant.GEMINI_FLASH.value,
    mode="google"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Reset Chat", key="reset_chat"):
    st.session_state.messages = []
    with open(history_file, "w") as f:
        f.write("")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    history = get_history()
    # Generate chatbot response
    response, steps = generator.invoke(prompt, history=history)
    with open(history_file, "a") as f:
        f.write(str(steps[1:]))

    # Add chatbot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
