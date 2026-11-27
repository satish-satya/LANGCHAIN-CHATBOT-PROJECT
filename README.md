# AI Customer Support Chatbot

A customer support chatbot built with **LangChain**, **OpenAI**, and **Streamlit**. This project demonstrates how prompts, memory, output parsers, and chat models work together in a real LangChain application.

**GitHub Repository:**  
https://github.com/satish-satya/LANGCHAIN-CHATBOT-PROJECT

---

## Project Overview

This chatbot answers customer support questions through a Streamlit web interface. It maintains conversation history, classifies user intent, assigns a confidence score, and recommends when human support may be required.

This is an educational project designed for learning LangChain fundamentals. It does not connect to customer databases, payment systems, or real support platforms.

---

## Features

- Customer support chatbot interface
- Conversation memory
- Intent classification
- Confidence score generation
- Human-support recommendation
- Structured responses using Pydantic
- Streamlit web interface
- OpenAI model integration through LangChain
- Clear Chat functionality

---

## Technology Stack

- Python 3.11+
- LangChain
- LangChain Core
- LangChain OpenAI
- OpenAI API
- Streamlit
- Pydantic
- Python Dotenv

---

## Project Structure

```text
LANGCHAIN-CHATBOT-PROJECT/
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

---

## Module Description

### app.py

Creates the Streamlit user interface and displays chat responses.

### config.py

Loads environment variables such as:

- OPENAI_API_KEY
- OPENAI_MODEL

### models.py

Creates and configures the ChatOpenAI model.

### prompts.py

Builds the prompt template used by the chatbot.

### memory.py

Stores and retrieves conversation history.

### output_parser.py

Defines the structured response schema using Pydantic.

### chat.py

Connects prompts, model, memory, and output parser into a complete LangChain workflow.

---

## Prerequisites

Before running the project, install:

- Python 3.11 or newer
- OpenAI API Key
- Git
- PowerShell or Terminal

Check Python version:

```powershell
python --version
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/satish-satya/LANGCHAIN-CHATBOT-PROJECT.git
cd LANGCHAIN-CHATBOT-PROJECT
```

### Create Virtual Environment

```powershell
python -m venv myenv
```

### Activate Virtual Environment

```powershell
.\myenv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
```

Example:

```env
OPENAI_API_KEY=sk-your-real-key
OPENAI_MODEL=gpt-4.1-mini
```

> Never upload your `.env` file to GitHub.

---

## Run the Application

```powershell
streamlit run app.py
```

Streamlit will start a local server:

```text
http://localhost:8501
```

Open that URL in your browser.

---

## Example Questions

```text
I was charged twice for my order.
```

```text
I want a refund.
```

```text
My account is not working.
```

```text
The payment was deducted but the order failed.
```

---

## How the Workflow Works

1. User enters a question in Streamlit.
2. Chat history is loaded from memory.
3. Prompt template is generated.
4. Prompt is sent to the OpenAI model.
5. Model generates a structured response.
6. Output parser extracts:
   - Response
   - Intent
   - Confidence
   - Human Support Recommendation
7. Memory stores the conversation.
8. Streamlit displays the final result.

---

## Testing

Run local integration checks:

```powershell
python test_integration.py
```

Expected output:

```text
All local integration checks passed.
```

---

## Troubleshooting

### API Key Missing

Verify the `.env` file contains a valid API key.

### Streamlit Not Found

Run:

```powershell
python -m streamlit run app.py
```

### Virtual Environment Activation Error

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again.

### AI Service Not Reachable

Check:

- Internet connection
- API key validity
- OpenAI billing status
- Model name in `.env`

---

## Learning Objectives

This project demonstrates:

- LangChain Fundamentals
- Prompt Engineering
- Chat Models
- Memory Management
- Output Parsing
- Environment Variables
- Streamlit Integration
- Project Structure Best Practices

---

## Future Improvements

- Ollama Integration
- Llama 3.2 Support
- RAG (Retrieval-Augmented Generation)
- Vector Database Integration
- Chat History Persistence
- Multi-user Support
- Conversation Analytics

---

## Author

**Satish Kumar**

GitHub:
https://github.com/satish-satya

Project Repository:
https://github.com/satish-satya/LANGCHAIN-CHATBOT-PROJECT
