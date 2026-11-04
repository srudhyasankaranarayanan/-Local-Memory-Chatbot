# Cortex Chatbot

A simple chatbot built with **Ollama, Gemma 3:1B, LangChain, and Streamlit**. It runs locally and uses conversation memory to remember previous messages and answer follow-up questions.

## Demo Link

https://8prglpcnva4di5zmyyawqn.streamlit.app/

## Features

- Runs locally using Ollama
- Uses the Gemma 3:1B language model
- Maintains conversation history with LangChain
- Supports follow-up questions
- Provides a simple Streamlit chat interface
- Includes a button to clear the conversation
- Does not require an external LLM API key

## Technologies Used

- Python
- Streamlit
- Ollama
- Gemma 3:1B
- LangChain
- `langchain-ollama`

## Project Structure

```text
Local-Memory-Chatbot/
├── app.py
├── requirements.txt
└── README.md
```

## Prerequisites

Install the following:

- Python 3.10 or later
- [Ollama](https://ollama.com/)

## Setup and Installation

### 1. Download the model

Open a terminal and run:

```bash
ollama pull gemma3:1b
```

Make sure Ollama is running.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The chatbot will open in your browser.

## How It Works

1. The user enters a message in the Streamlit chat interface.
2. LangChain retrieves the conversation history.
3. The prompt and previous messages are sent to Gemma 3:1B through Ollama.
4. The model generates a response.
5. LangChain stores the user message and assistant response in memory.
6. The conversation is displayed in the chat interface.

## Memory

This project uses LangChain's `InMemoryChatMessageHistory`.

- Remembers previous messages during the current app session.
- Uses conversation history to answer follow-up questions.
- The **Clear conversation** button removes the current chat history.
- Memory is temporary and is not stored in a database.

## Limitations

- Response speed depends on your computer's hardware.
- Conversation history is cleared when the app session is reset.
- The model may occasionally generate inaccurate information.
- The chatbot only uses the locally installed model.

## Future Enhancements

- Save conversation history in SQLite.
- Add multiple chat sessions.
- Add downloadable chat transcripts.
- Support additional Ollama models.

## License

This project is intended for learning and educational purposes.

## Author

**Srudhya Sankaranarayanan**
