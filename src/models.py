"""
This module creates the OpenAI chat model used by the chatbot.
Model setup stays in this one place so the rest of the app
can request replies without repeating the configuration.
"""

from langchain_openai import ChatOpenAI

from src.config import get_openai_api_key, get_openai_model


def create_chat_model() -> ChatOpenAI:
    """
    Creates the OpenAI chat model from the values in the .env file.
    Input: none. The API key and model name come from the configuration module.
    Output: a ChatOpenAI object that can generate customer-support replies.
    """
    # The key and model name are read from the environment.
    # They are not written in this file.
    # temperature=0.3 keeps support replies steady.
    return ChatOpenAI(
        model=get_openai_model(),
        api_key=get_openai_api_key(),
        temperature=0.3,
    )
