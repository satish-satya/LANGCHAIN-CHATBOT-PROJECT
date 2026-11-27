import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT= Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT/".env")

class ConfigurationError(Exception):
    """
    Raised when a required setting in the .env file is 
    missing The Streamlit page catches it and shows the
    setup steps.
    """

def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY","").strip()

    if api_key == "" or api_key == "your_openai_api_key":
        raise ConfigurationError("The OpenAI key is missing.")
    return api_key    

# def get_openai_model() -> str:
#     """
#     Return the OpenAI model name loaded from the environment
#     Input: none. The value comes from OPENAI_MODEL in the .env file.
#     Output: the  model name. Raises configurationError when it is missing.
#     """
#     os.getenv()

def get_openai_model() -> str:
    model = os.getenv("OPENAI_MODEL")

    if not model:
        raise ConfigurationError(
            "OPENAI_MODEL is missing in the .env file."
        )

    return model