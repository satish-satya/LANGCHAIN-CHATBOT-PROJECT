"""
This module defines the instructions that control the chatbot.
The prompt tells the model to act as a polite support agent and
packages the earlier messages plus the customer's new question.
"""

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

# {format_instructions} is filled later with the output parser's JSON schema.
# The intent names below must match the intent field in output_parser.py.
SYSTEM_PROMPT = """
You are a polite and helpful customer support representative.

Answer the customer's latest question clearly and concisely.
Use earlier messages to understand what the customer has already told you.
Only state business rules that the customer has already provided.
When a policy, price, refund rule, or account detail is unknown, say that you
do not know and recommend contacting human support.

Choose exactly one intent for the latest customer message:
Billing, Refund, Technical Support, General Inquiry, or Other.

Set requires_human_support to true when the customer should talk to a person.
Set confidence to a number from 0 to 1.

{format_instructions}
""".strip()


def create_chat_prompt() -> ChatPromptTemplate:
    """
    Builds the chat prompt template used for every customer message.
    Input: none. Callers later provide history, user_message, and format_instructions.
    Output: a ChatPromptTemplate that becomes a SystemMessage, past messages, and a HumanMessage.
    """
    # SystemMessagePromptTemplate becomes a SystemMessage when the prompt is filled in.
    # That SystemMessage holds the assistant's instructions.
    system_message_prompt = SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT)

    # HumanMessagePromptTemplate becomes a HumanMessage.
    # That HumanMessage holds the customer's latest question.
    human_message_prompt = HumanMessagePromptTemplate.from_template("{user_message}")

    # MessagesPlaceholder inserts the saved HumanMessage and AIMessage objects
    # between the instructions and the new question.
    return ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            MessagesPlaceholder(variable_name="history"),
            human_message_prompt,
        ]
    )
