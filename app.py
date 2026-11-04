import streamlit as st

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Cortex Chatbot",
    page_icon="💬",
    layout="centered"
)

# -----------------------------
# Colorful lavender design
# -----------------------------
st.markdown(
    """
    <style>
    :root {
        --ink: #35234f;
        --lavender: #a78bfa;
        --purple: #7c3aed;
        --pink: #f0abfc;
        --blue: #a5b4fc;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 12%, rgba(240, 171, 252, .55) 0, transparent 25%),
            radial-gradient(circle at 92% 18%, rgba(165, 180, 252, .55) 0, transparent 27%),
            radial-gradient(circle at 80% 90%, rgba(196, 181, 253, .55) 0, transparent 30%),
            linear-gradient(135deg, #fbf7ff 0%, #f2eaff 48%, #e9e7ff 100%);
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #eee5ff 0%, #fce7f3 100%);
        border-right: 1px solid rgba(167, 139, 250, .35);
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] p {
        color: #4c2f70 !important;
    }

    /* Main title */
    h1 {
        color: #6d28d9 !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        text-shadow: 0 3px 18px rgba(167, 139, 250, .25);
    }

    h2, h3, p, label {
        color: var(--ink);
    }

    /* Subtitle */
    [data-testid="stCaptionContainer"] {
        color: #765b98;
    }

    /* Chat message cards */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, .72);
        border: 1px solid rgba(196, 181, 253, .65);
        border-radius: 20px;
        padding: 1rem 1.1rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 24px rgba(109, 40, 217, .08);
        margin-bottom: .8rem;
    }

    /* User and assistant avatar accents */
    [data-testid="stChatMessage"] [data-testid="stAvatar"] {
        background: linear-gradient(135deg, #c4b5fd, #f0abfc);
        border-radius: 50%;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, .9);
        border: 2px solid #d8b4fe;
        border-radius: 22px;
        box-shadow: 0 8px 24px rgba(124, 58, 237, .12);
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #a78bfa;
        box-shadow: 0 0 0 3px rgba(167, 139, 250, .18);
    }

    [data-testid="stChatInput"] textarea {
        color: #35234f !important;
    }

    /* Gradient buttons */
    .stButton > button {
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 50%, #f0abfc 100%);
        color: #ffffff !important;
        border: 0;
        border-radius: 14px;
        font-weight: 700;
        padding: .55rem 1rem;
        box-shadow: 0 6px 16px rgba(124, 58, 237, .18);
        transition: transform .2s ease, box-shadow .2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(124, 58, 237, .25);
        border: 0;
    }

    /* Info and error messages */
    [data-testid="stAlert"] {
        background: rgba(255, 255, 255, .72);
        border: 1px solid #e9d5ff;
        border-radius: 16px;
        color: #4c2f70;
    }

    /* Decorative heading panel */
    .hero-card {
        background: linear-gradient(120deg, rgba(196, 181, 253, .45), rgba(251, 207, 232, .55), rgba(191, 219, 254, .45));
        border: 1px solid rgba(255, 255, 255, .8);
        border-radius: 24px;
        padding: 1.1rem 1.3rem;
        margin: .5rem 0 1.2rem 0;
        box-shadow: 0 10px 30px rgba(124, 58, 237, .08);
    }

    .hero-card p {
        margin: 0;
        color: #624482;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-card">
      <h1 style="margin:0;">💬 Cortex Chatbot</h1>
      <p>Your local AI companion — powered by Gemma 3:1B and LangChain memory.</p>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Local LLM
# -----------------------------
llm = ChatOllama(
    model="gemma3:1b",
    temperature=0.7
)


# -----------------------------
# Prompt with conversation history
# -----------------------------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a friendly and helpful chatbot. "
        "Use the conversation history to understand follow-up questions. "
        "If you do not know something, say so."
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

chain = prompt | llm


# -----------------------------
# LangChain memory
# -----------------------------
if "chat_store" not in st.session_state:
    st.session_state.chat_store = {}

if "session_id" not in st.session_state:
    st.session_state.session_id = "streamlit_chat"


def get_session_history(session_id: str):
    if session_id not in st.session_state.chat_store:
        st.session_state.chat_store[session_id] = (
            InMemoryChatMessageHistory()
        )
    return st.session_state.chat_store[session_id]


chatbot = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.subheader("✨ Chat settings")

    if st.button("Clear conversation", use_container_width=True):
        get_session_history(
            st.session_state.session_id
        ).clear()
        st.rerun()

    st.info(
        "Your chat memory stays available during this app session. "
        "Restarting the app may clear it."
    )


# -----------------------------
# Display conversation
# -----------------------------
history = get_session_history(st.session_state.session_id)

for message in history.messages:
    role = "user" if message.type == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)


# -----------------------------
# User input and response
# -----------------------------
user_input = st.chat_input("✨ Ask Cortex anything...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Cortex is thinking..."):
            try:
                response = chatbot.invoke(
                    {"question": user_input},
                    config={
                        "configurable": {
                            "session_id": st.session_state.session_id
                        }
                    }
                )
                st.markdown(response.content)

            except Exception as error:
                st.error(
                    "Could not connect to Ollama. "
                    "Check that Ollama is running and Gemma is installed."
                )
                st.caption(str(error))
