"""
Streamlit page for the AI Customer Support Assistant.
This file draws the chat window and sends each customer message
to the LangChain workflow in src/chat.py.
"""

import uuid

import streamlit as st

from src.chat import get_chat_response
from src.config import ConfigurationError, get_openai_api_key, get_openai_model
from src.memory import clear_history


def ensure_session() -> str:
    """
    Prepares the values Streamlit remembers for this browser tab.
    Input: none. Streamlit keeps st.session_state between reruns of this script.
    Output: the session id used to store this chat's message history.
    """
    # session_state survives each new message and each button click in this tab.
    # A new browser session does not have these values yet, so we create them.
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        # Each item is one chat bubble. Assistant items also store intent details.
        st.session_state.messages = []

    return st.session_state.session_id


def render_message(message: dict) -> None:
    """
    Draws one saved chat bubble on the page.
    Input: message, a dictionary with role and content. Assistant items also include intent details.
    Output: none. The bubble is written onto the Streamlit page.
    """
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant":
            if message["requires_human_support"]:
                human_support = "Yes"
            else:
                human_support = "No"

            st.caption(
                f"Intent: {message['intent']} | "
                f"Confidence: {message['confidence']:.2f} | "
                f"Human support recommended: {human_support}"
            )


# set_page_config must run before other Streamlit display commands.
st.set_page_config(page_title="AI Customer Support Assistant")

st.title("AI Customer Support Assistant")
st.write(
    "Ask a customer support question and the assistant will answer using this conversation. "
    "Each reply includes the detected category, a confidence score from 0 to 1, "
    "and whether human support is recommended."
)

try:
    # Check the .env settings before drawing the chat.
    # The key itself is not stored or shown on the page.
    get_openai_api_key()
    model_name = get_openai_model()
except ConfigurationError as error:
    st.error(str(error))
    st.stop()

session_id = ensure_session()

with st.sidebar:
    st.header("About this app")
    st.write(
        "This learning project connects a LangChain model, prompt, message history, "
        "and output parser. It answers questions in this session and labels each one."
    )
    st.write("It does not look up customer accounts or process refunds.")
    st.write(f"Model: {model_name}")

    st.header("Supported categories")
    st.write("Billing — invoices, charges, and payments.")
    st.write("Refund — requests to get money back.")
    st.write("Technical Support — something is not working.")
    st.write("General Inquiry — hours, contact options, and other general questions.")
    st.write("Other — questions that do not fit the categories above.")

    if st.button("Clear Chat"):
        # The page bubbles and the LangChain history are cleared together.
        clear_history(session_id)
        st.session_state.messages = []
        st.rerun()

user_text = st.chat_input("Type your question")

if user_text:
    # Save the question first, then ask the LangChain workflow for a reply.
    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.spinner("Writing a reply..."):
        result = get_chat_response(session_id, user_text)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result.response,
            "intent": result.intent,
            "confidence": result.confidence,
            "requires_human_support": result.requires_human_support,
        }
    )

# The hint is for an empty chat. It stays hidden once any message is saved.
if not st.session_state.messages:
    st.info("Type a question in the box at the bottom to start the conversation.")

for message in st.session_state.messages:
    render_message(message)
