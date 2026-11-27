"""
This module turns the model's text into a predictable Python object.
The chatbot uses that object to show the reply, the detected intent,
and whether a human support agent is recommended.
"""

from typing import Literal

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, ValidationError


class SupportResponse(BaseModel):
    """
    The structured result produced for one customer message.
    response is the text shown in the chat. intent is the question category.
    """

    # Field descriptions are included in the JSON instructions sent to the model.
    response: str = Field(description="The reply that should be shown to the customer.")
    intent: Literal[
        "Billing",
        "Refund",
        "Technical Support",
        "General Inquiry",
        "Other",
    ] = Field(description="The category of the customer's latest message.")
    # ge and le mean the score must be from 0 through 1.
    confidence: float = Field(
        ge=0,
        le=1,
        description="How sure the category is, as a number from 0 to 1.",
    )
    requires_human_support: bool = Field(
        description="True when a human support agent should help the customer."
    )


def create_output_parser() -> PydanticOutputParser:
    """
    Creates the parser that converts model text into a SupportResponse.
    Input: none.
    Output: a PydanticOutputParser configured with the SupportResponse schema.
    """
    # pydantic_object tells the parser which fields to expect.
    return PydanticOutputParser(pydantic_object=SupportResponse)


def parse_support_response(parser: PydanticOutputParser, model_text: str) -> SupportResponse:
    """
    Converts the model's text into a SupportResponse object.
    Input: parser, and model_text such as JSON with intent "Refund".
    Output: a SupportResponse, or a safe fallback when the text is invalid or incomplete.
    """
    text = model_text.strip()

    # Some model replies wrap the JSON in a markdown fence: ```json ... ```
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[1:-1]
        else:
            lines = lines[1:]
        text = "\n".join(lines).strip()

    try:
        return parser.parse(text)
    except (OutputParserException, ValidationError, ValueError):
        # Invalid JSON or a missing field should not crash the chat page.
        return SupportResponse(
            response=(
                "I'm sorry, I could not prepare a complete answer. "
                "Please try again, or contact human support if you still need help."
            ),
            intent="Other",
            confidence=0.0,
            requires_human_support=True,
        )
