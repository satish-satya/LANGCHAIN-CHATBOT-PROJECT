"""
This module connects the model, prompt, memory, and output parser.
It runs one customer message through that workflow and returns
a structured reply the Streamlit page can display.
"""

from langchain_core.messages import AIMessage

from src.memory import add_ai_message, add_user_message, get_messages
from src.models import create_chat_model
from src.output_parser import SupportResponse, create_output_parser, parse_support_response
from src.prompts import create_chat_prompt


def message_to_text(ai_message) -> str:
    """
    Reads the reply text from the chat model result.
    Input: ai_message, usually an AIMessage returned by ChatOpenAI.
    Output: the text the output parser should read.
    """
    if isinstance(ai_message, AIMessage):
        content = ai_message.content
    else:
        content = ai_message

    if isinstance(content, str):
        return content

    # Some replies arrive as a list of blocks, such as [{"type": "text", "text": "..."}].
    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, str):
                text_parts.append(block)
            elif isinstance(block, dict):
                text_parts.append(str(block.get("text", "")))
        return "".join(text_parts)

    return str(content)


def get_chat_response(session_id: str, user_message: str, model=None) -> SupportResponse:
    """
    Answers one customer message with the LangChain workflow.
    Input: session_id for this chat, and user_message, the text the customer typed.
    Output: a SupportResponse with the reply, intent, confidence, and human-support flag.
    Example: "I want my money back" can return the intent "Refund".
    """
    # The Streamlit app leaves model empty, so the real ChatOpenAI model is created.
    # The test file can pass a fake model here and avoid an OpenAI API call.
    if model is None:
        model = create_chat_model()

    prompt = create_chat_prompt()
    parser = create_output_parser()

    # Read the old messages before saving the new question.
    # Saving first would place the same question in the prompt twice.
    history = get_messages(session_id)

    # The | operator builds a RunnableSequence.
    # The prompt is filled first, then those messages are sent to the model.
    chain = prompt | model

    try:
        # These keys match the placeholders in the prompt template.
        ai_message = chain.invoke(
            {
                "history": history,
                "user_message": user_message,
                "format_instructions": parser.get_format_instructions(),
            }
        )
    except Exception:
        # Connection failures, a rejected API key, and rate limits reach this branch.
        # Show a short explanation only. The raw error can contain request
        # details, so it stays off the chat page.
        parsed = SupportResponse(
            response=(
                "I could not reach the AI service. "
                "Check your internet connection and the OPENAI_API_KEY in your .env file, "
                "then try again."
            ),
            intent="Other",
            confidence=0.0,
            requires_human_support=True,
        )
    else:
        # else runs only when the model call succeeded.
        parsed = parse_support_response(parser, message_to_text(ai_message))

    # Save the customer text and the customer-facing reply for the next turn.
    add_user_message(session_id, user_message)
    add_ai_message(session_id, parsed.response)
    return parsed
