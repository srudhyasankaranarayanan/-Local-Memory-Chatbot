# Cortex – Personal AI Chatbot

Cortex is a personal AI chatbot built with **Streamlit**, **LangChain**, and **Ollama**. It provides an interactive chat interface with conversation memory and support for multiple locally running language models.

## Demo Link

https://8prglpcnva4di5zmyyawqn.streamlit.app/

## Features

- Chat with locally hosted AI models using Ollama
- Choose from supported models in the sidebar
- Select conversation memory modes:
  - **Buffer Memory:** remembers the full conversation
  - **Summary Memory:** maintains a summary of the conversation
  - **Window Memory:** remembers the most recent messages
- View stored conversation memory
- Clear the current conversation or all chat histories
- Colorful, interactive Streamlit interface

## Technologies Used

- Python
- Streamlit
- LangChain
- Ollama

## Prerequisites

- Python 3.10 or later
- [Ollama](https://ollama.com/) installed and running
- At least one supported model downloaded

## Installation

1. Clone or download this project.
2. Open a terminal in the project folder.
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Download the default model:

   ```bash
   ollama pull gemma3:1b
   ```

5. Start Ollama if it is not already running.

6. Launch Cortex:

   ```bash
   streamlit run app.py
   ```

7. Open the local URL displayed in your terminal.

## Project Structure

```text
Cortex/
├── app.py
├── requirements.txt
└── README.md
```

## Note

Cortex uses Ollama to run models locally. Make sure Ollama is running and the selected model is downloaded before chatting.

## Future Improvements

- Export conversations
- Add more model options
- Customize chatbot themes
- Add document-based question answering

## License

This project is intended for educational and personal use.

## Author

**Srudhya Sankaranarayanan**
