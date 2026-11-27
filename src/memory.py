"""
This module manages conversation history for the chatbot.
It stores previous human and AI messages so the model
can generate context-aware responses.
"""

import warnings

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

# LangChain 1.6.4 marked this class as deprecated in favor of agent memory.
# This lesson still uses it: it is the simple in-memory ChatMessageHistory
# and it keeps each session's messages in a Python list.
warnings.filterwarnings(
    "ignore",
    message=r".*InMemoryChatMessageHistory.*was deprecated.*",
)

# One history object per Streamlit session.
# The key is the session id created in app.py.
_session_histories: dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """
    Returns the message history for one Streamlit session.
    Input: session_id, the unique id for the current browser session.
    Output: the InMemoryChatMessageHistory that stores that session's messages.
    """
    if session_id not in _session_histories:
        _session_histories[session_id] = InMemoryChatMessageHistory()

    return _session_histories[session_id]


def get_messages(session_id: str) -> list[BaseMessage]:
    """
    Returns the saved messages for one session, oldest first.
    Input: session_id for the Streamlit session.
    Output: a list of HumanMessage and AIMessage objects. It is empty for a new chat.
    """
    # list(...) copies the messages so reading them does not change the saved history.
    return list(get_session_history(session_id).messages)


def add_user_message(session_id: str, message: str) -> None:
    """
    Saves the customer's message in that session's history.
    Input: session_id, and message, the text the customer typed.
    Output: none. The history gains one HumanMessage.
    Example: add_user_message("session-1", "I need a refund") stores that sentence.
    """
    human_message = HumanMessage(content=message)
    get_session_history(session_id).add_message(human_message)


def add_ai_message(session_id: str, message: str) -> None:
    """
    Saves the chatbot reply in that session's history.
    Input: session_id, and message, the reply text shown to the customer.
    Output: none. The history gains one AIMessage.
    """
    ai_message = AIMessage(content=message)
    get_session_history(session_id).add_message(ai_message)


def clear_history(session_id: str) -> None:
    """
    Deletes every saved message for one Streamlit session.
    Input: session_id for the chat that should start over.
    Output: none. The next get_messages call returns an empty list.
    """
    if session_id in _session_histories:
        _session_histories[session_id].clear()
