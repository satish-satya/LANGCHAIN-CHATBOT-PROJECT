# AI Customer Support Chatbot

This is a learning project . It shows how a chat model, a prompt template, message history, and an output parser work together in one small application.

The chatbot answers customer questions in a Streamlit page. It remembers the current conversation, labels each question, and shows whether a human support agent is recommended. It is a demonstration. It does not look up customer accounts or process refunds.

## Project features

- Chat with a customer support assistant in the browser.
- The assistant remembers earlier messages in the same Streamlit session.
- Each reply is labeled as Billing, Refund, Technical Support, General Inquiry, or Other.
- Each reply includes a confidence score from 0 to 1.
- Each reply says whether human support is recommended.
- A **Clear Chat** button starts the conversation over.
- A missing API key shows setup steps for the `.env` file.

## Technology stack

- Python 3.11 or newer
- LangChain (`langchain`, `langchain-core`, and `langchain-openai`)
- OpenAI chat models through LangChain's `ChatOpenAI`
- Streamlit for the web page
- python-dotenv for the `.env` file
- Pydantic for the structured reply

OpenAI is the only model provider used by this project.

## Project folder structure

```text
PW-LangChain-Customer-Support/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── prompts.py
│   ├── memory.py
│   ├── chat.py
│   └── output_parser.py
│
├── app.py
├── test_integration.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

`test_integration.py` is a small local check. It is not part of the chatbot page. It uses a fake model, so it does not call OpenAI.

## Explanation of each Python module

| File | What it does |
| --- | --- |
| `app.py` | The Streamlit page. It draws the chat, sends the customer's text to `src/chat.py`, and shows the reply, intent, confidence, and human-support flag. |
| `src/config.py` | Loads `OPENAI_API_KEY` and `OPENAI_MODEL` from the `.env` file. |
| `src/models.py` | Creates one `ChatOpenAI` model with `temperature=0.3`. |
| `src/prompts.py` | Builds a `ChatPromptTemplate`. The filled prompt starts with a `SystemMessage` (the instructions) and ends with a `HumanMessage` (the customer's question). |
| `src/memory.py` | Stores each session's `HumanMessage` and `AIMessage` objects with `InMemoryChatMessageHistory` (the simple in-memory `ChatMessageHistory`). Newer agent tutorials use a checkpointer instead. This project keeps the list-based history so the lesson stays small. |
| `src/output_parser.py` | Defines the `SupportResponse` schema and uses `PydanticOutputParser` to read the model's JSON. |
| `src/chat.py` | Connects the pieces. The LCEL pipe `prompt \| model` builds a `RunnableSequence`, then the parser turns the reply into a `SupportResponse`. |

## Prerequisites

Install these before you start:

1. **Python 3.11 or newer.** This project was written for Python 3.11. Python 3.12 and 3.13 also work with the packages in `requirements.txt`.
2. **An OpenAI API key.** Create one at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys). A key usually starts with `sk-`.
3. **A terminal.** On Windows, use PowerShell.

Check Python from PowerShell:

```powershell
py -3.11 --version
```

If that command says Python was not found, try:

```powershell
py -3 --version
```

You want a version number of 3.11 or higher. If Python is missing, download it from [https://www.python.org/downloads/](https://www.python.org/downloads/) and turn on **Add python.exe to PATH** during setup. Then close and reopen PowerShell.

## Installation instructions

The steps below use Windows PowerShell. Run them from the project folder, the folder that contains `app.py`.

### 1. Open the project folder

```powershell
cd "C:\path\to\PW-LangChain-Customer-Support"
```

Replace that path with the real folder on your computer.

## Virtual environment setup

A virtual environment keeps this project's packages separate from other Python projects.

Create it with Python 3.11 when that version is installed:

```powershell
py -3.11 -m venv .venv
```

If `py -3.11` is not available, use your installed Python 3.11+ launcher instead:

```powershell
py -3 -m venv .venv
```

Turn the environment on:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the script, run this once in the same window and then try the activate command again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

The start of the line should change to `(.venv)`. That means later `python` and `pip` commands use this project.

You can also skip activation and call the virtual environment by its full path:

```powershell
.\.venv\Scripts\python.exe --version
```

## Dependency installation

With the virtual environment turned on, install the libraries:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`pip` also installs libraries that these packages need. The `langchain` package installs LangGraph for other LangChain features. This chatbot does not use agents, tools, or LangGraph in its own code.

## OpenAI API key configuration

The application reads the key and the model name from environment variables. Copy the example file and then edit the copy.

```powershell
copy .env.example .env
notepad .env
```

`.env.example` contains:

```text
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
```

In `.env`, replace `your_openai_api_key` with your real key. Leave the model line as it is unless your course tells you to use another OpenAI chat model. Save the file.

Example after editing:

```text
OPENAI_API_KEY=sk-your-real-key-here
OPENAI_MODEL=gpt-4.1-mini
```

Keep the `.env` file private. `.gitignore` already excludes it, so a normal `git add` will not pick it up.

If the key is missing or still says `your_openai_api_key`, the Streamlit page shows the same setup steps and waits there.

## How to run the application

From the project folder, with the virtual environment turned on:

```powershell
python -m streamlit run app.py
```

Streamlit prints a local address, usually `http://localhost:8501`. Open that address in your browser if it does not open on its own.

Try a question such as:

```text
I was charged twice for the same order.
```

The page shows the reply, the intent, the confidence score, and whether human support is recommended. Ask a follow-up in the same page. The assistant can use the earlier messages. **Clear Chat** in the sidebar removes the bubbles and the saved history.

Stop the app from the terminal with `Ctrl+C`.

### Full Windows command list

Use this list when you want every command in one place:

```powershell
cd "C:\path\to\PW-LangChain-Customer-Support"
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
notepad .env
python -m streamlit run app.py
```

## How the LangChain components interact

Here is one customer message, from the browser back to the browser:

1. You type a question in `app.py`. Streamlit stores the chat bubbles in `st.session_state` for this browser tab.
2. `app.py` calls `get_chat_response` in `src/chat.py` and passes the session id plus your text.
3. `src/chat.py` asks `src/memory.py` for the earlier `HumanMessage` and `AIMessage` objects from this session.
4. `src/prompts.py` builds a `ChatPromptTemplate`. When it is filled in, the result is:
   - a `SystemMessage` with the support instructions and the JSON format rules
   - the earlier messages, if any
   - a `HumanMessage` with your new question
5. `src/models.py` provides a `ChatOpenAI` model. The model name and API key come from `src/config.py`.
6. `src/chat.py` connects the prompt and the model with the pipe operator: `prompt | model`. That object is a `RunnableSequence`. The prompt output flows into the model.
7. The model returns text that should be a JSON object.
8. `src/output_parser.py` uses `PydanticOutputParser` to turn that JSON into a `SupportResponse` with `response`, `intent`, `confidence`, and `requires_human_support`. If the text is invalid, the parser returns a safe fallback reply.
9. `src/memory.py` saves your question and the customer-facing reply so the next question can see them.
10. `app.py` draws the reply and the three extra fields under it.

The page bubbles and the LangChain history are two lists that stay in step:

- `st.session_state.messages` is what the page draws, including intent and confidence.
- `InMemoryChatMessageHistory` is what the model reads on the next turn.

**Clear Chat** empties both lists for that session. Nothing is written to a database.

## Run the local checks

`test_integration.py` checks syntax, imports, settings, the prompt, memory, parsing, and a two-message conversation. It passes a fake model into the chat workflow, so it does not spend API credits.

```powershell
python test_integration.py
```

A successful run prints `All local integration checks passed.` A real answer from OpenAI still requires a valid key and the Streamlit page.

## Troubleshooting

**The page says the API key is missing.**  
Repeat the `.env` steps above. The file must be named `.env`, and it must sit in the same folder as `app.py`. Restart Streamlit after you save it.

**`streamlit` is not recognized.**  
Turn on the virtual environment, then run `python -m streamlit run app.py`.

**PowerShell will not run `Activate.ps1`.**  
Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that window, then run the activate command again.

**The reply says it could not reach the AI service.**  
Check the internet connection, the key in `.env`, and that the OpenAI account can call the model named by `OPENAI_MODEL`.

**`pip` says `WinError 206` or the filename is too long.**  
This happens on Windows when the project sits in a deep folder, such as a long OneDrive path. Create the virtual environment in a short folder, then install and run from the project folder:

```powershell
py -3.11 -m venv C:\venvs\customer-support
C:\venvs\customer-support\Scripts\Activate.ps1
cd "C:\path\to\PW-LangChain-Customer-Support"
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
