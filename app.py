import os
import streamlit as st

from langchain_ollama import ChatOllama
from langchain_classic.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory,
)
from langchain_core.prompts import ChatPromptTemplate


# ------------------------------------------
# Page setup
# ------------------------------------------
st.set_page_config(
    page_title="Cortex - AI Chatbot",
    page_icon="💬",
    layout="wide",
)


# ------------------------------------------
# Dark blue and bright blue theme
# ------------------------------------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #f8efff 0%,
        #fff0f5 50%,
        #fff8df 100%
    );
    color: #493653;
}

/* Main content */
.main .block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #e9d5ff 0%,
        #f8dce9 55%,
        #ffe8a3 100%
    );
    border-right: 2px solid #e6b94a;
}

[data-testid="stSidebar"] * {
    color: #55345f !important;
}

/* Title */
h1 {
    color: #8b5bb5 !important;
    font-weight: 800 !important;
}

/* Headings */
h2, h3 {
    color: #a05b91 !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.78);
    border: 1px solid #ead5f5;
    border-radius: 18px;
    padding: 14px;
    box-shadow: 0 4px 12px rgba(143, 91, 181, 0.08);
}

/* Chat input */
[data-testid="stChatInput"] {
    border: 2px solid #d9b8ed;
    border-radius: 18px;
    background: #fffaff;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #c9a7e8, #f2b8d0);
    color: #4d3158;
    border: 1px solid #e3c2ee;
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #b98add, #eda2c2);
    border-color: #d9a7e8;
    transform: translateY(-2px);
}

/* Gold accent buttons */
.gold-button {
    background: linear-gradient(135deg, #ffe9a8, #e6b94a);
    color: #684d18;
    border-radius: 12px;
}

/* Select boxes and other inputs */
[data-baseweb="select"],
[data-baseweb="input"],
[data-baseweb="textarea"] {
    border-radius: 12px;
}

/* Expanders */
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid #ead5f5;
    border-radius: 14px;
}

/* Divider */
hr {
    border-color: #e8c9ed;
}

/* Footer */
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------
# Session state
# ------------------------------------------
MEMORY_TYPES = [
    "Buffer Memory",
    "Summary Memory",
    "Window Memory",
]

if "chats" not in st.session_state:
    st.session_state.chats = {
        memory_type: [] for memory_type in MEMORY_TYPES
    }

if "memories" not in st.session_state:
    st.session_state.memories = {}


# ------------------------------------------
# Ollama configuration
# ------------------------------------------
def get_ollama_url():
    url = os.getenv("OLLAMA_BASE_URL")

    if not url:
        try:
            url = st.secrets.get(
                "OLLAMA_BASE_URL",
                "http://localhost:11434",
            )
        except Exception:
            url = "http://localhost:11434"

    return url.rstrip("/")


@st.cache_resource
def load_llm(model_name, base_url):
    return ChatOllama(
        model=model_name,
        base_url=base_url,
        temperature=0.7,
    )


# ------------------------------------------
# Create LangChain memory
# ------------------------------------------
def create_memory(memory_type, llm):
    if memory_type == "Buffer Memory":
        return ConversationBufferMemory(
            memory_key="history",
            input_key="input",
            output_key="output",
            return_messages=False,
        )

    if memory_type == "Summary Memory":
        return ConversationSummaryMemory(
            llm=llm,
            memory_key="history",
            input_key="input",
            output_key="output",
            return_messages=False,
        )

    if memory_type == "Window Memory":
        return ConversationBufferWindowMemory(
            k=3,
            memory_key="history",
            input_key="input",
            output_key="output",
            return_messages=False,
        )


def get_memory(memory_type, llm):
    if memory_type not in st.session_state.memories:
        st.session_state.memories[memory_type] = create_memory(
            memory_type,
            llm,
        )

    return st.session_state.memories[memory_type]


# ------------------------------------------
# Generate chatbot response
# ------------------------------------------
def generate_response(user_input, llm, memory):
    memory_data = memory.load_memory_variables({})
    history = memory_data.get("history", "")

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are Cortex, an intelligent and friendly AI assistant.

            Instructions:
            - Give clear and useful answers.
            - Remember relevant information from conversation history.
            - Answer in simple English.
            - Avoid repeating unnecessary information.
            - If you do not know something, say so.
            """
        ),
        (
            "human",
            """
            Previous Conversation:
            {history}

            Current Question:
            {input}
            """
        ),
    ])

    chain = prompt | llm

    response = chain.invoke({
        "history": history,
        "input": user_input,
    })

    answer = response.content

    memory.save_context(
        {"input": user_input},
        {"output": answer},
    )

    return answer


# ------------------------------------------
# Sidebar settings
# ------------------------------------------
with st.sidebar:
    st.title("⚙️ Cortex Settings")

    model_name = st.selectbox(
        "Select Local LLM",
        [
            "gemma3:1b",
            "llama3.2",
            "llama3.1",
            "mistral",
        ],
    )

    memory_type = st.selectbox(
        "Select Memory Type",
        MEMORY_TYPES,
    )

    memory_descriptions = {
        "Buffer Memory":
            "Stores the complete conversation history.",
        "Summary Memory":
            "Creates a running summary of earlier conversation.",
        "Window Memory":
            "Stores only the latest 3 conversation exchanges.",
    }

    st.markdown("---")
    st.subheader("🧠 Memory Information")
    st.info(memory_descriptions[memory_type])

    st.markdown("---")

    if st.button("Clear Current Chat", use_container_width=True):
        st.session_state.chats[memory_type] = []

        if memory_type in st.session_state.memories:
            st.session_state.memories[memory_type].clear()

        st.rerun()

    if st.button("Clear All Memories", use_container_width=True):
        st.session_state.chats = {
            name: [] for name in MEMORY_TYPES
        }
        st.session_state.memories = {}
        st.rerun()


# ------------------------------------------
# Main heading
# ------------------------------------------
st.markdown(
    '<div class="main-title">CORTEX AI CHATBOT</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Local LLM powered by Ollama and LangChain Memory'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="text-align:center; margin-bottom:20px;">
        <span class="memory-badge">Memory: {memory_type}</span>
        <span class="memory-badge">Model: {model_name}</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------
# Initialize model and memory
# ------------------------------------------
try:
    llm = load_llm(model_name, get_ollama_url())
    memory = get_memory(memory_type, llm)

except Exception as error:
    st.error(f"Model initialization failed: {error}")
    st.stop()


# ------------------------------------------
# Display conversation
# ------------------------------------------
for message in st.session_state.chats[memory_type]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ------------------------------------------
# Chat input
# ------------------------------------------
user_input = st.chat_input("Ask Cortex anything...")

if user_input:
    st.session_state.chats[memory_type].append({
        "role": "user",
        "content": user_input,
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Cortex is thinking..."):
            try:
                answer = generate_response(
                    user_input,
                    llm,
                    memory,
                )

                st.markdown(answer)

                st.session_state.chats[memory_type].append({
                    "role": "assistant",
                    "content": answer,
                })

            except Exception as error:
                st.error(f"Unable to generate response: {error}")
                st.info(
                    "Check whether Ollama is running and the selected "
                    "model is installed. For Gemma, run: "
                    "ollama pull gemma3:1b"
                )


# ------------------------------------------
# View memory contents
# ------------------------------------------
with st.expander("View Memory Contents"):
    memory_data = memory.load_memory_variables({})

    st.write("Selected Memory:", memory_type)
    st.write(
        memory_data.get(
            "history",
            "No memory available yet.",
        )
    )