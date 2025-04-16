import streamlit as st
import requests

# Set page config FIRST
st.set_page_config(
    page_title="🧠 Ollama Chatbot", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Smooth Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: #b2bec3;
        border-radius: 10px;
    }

    /* Sticky Header */
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: linear-gradient(90deg, #e3f2fd, #fff);
        padding: 1rem 0;
        text-align: center;
        border-bottom: 1px solid #dfe6e9;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    .sticky-header h1 {
        font-size: 1.8rem;
        color: #0d47a1;
        font-weight: 600;
        margin: 0;
    }

    .main-content {
        padding-top: 6rem;
        padding-bottom: 5rem;
    }

    .sticky-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: #f1f2f6;
        padding: 0.8rem;
        border-top: 1px solid #dcdde1;
        text-align: center;
        font-size: 0.9rem;
        color: #636e72;
    }

    /* Chat Message Bubbles */
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        padding: 14px 20px;
        margin-bottom: 12px;
        border-radius: 18px;
        line-height: 1.6;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    [data-testid="stChatMessage"]:has(div[role="user"]) [data-testid="stMarkdownContainer"] {
        background-color: #dfe6e9;
        color: #2d3436;
        border-radius: 18px 18px 0 18px;
        align-self: flex-end;
    }

    [data-testid="stChatMessage"]:has(div[role="assistant"]) [data-testid="stMarkdownContainer"] {
        background-color: #e8f5e9;
        color: #1b5e20;
        border-radius: 18px 18px 18px 0;
        align-self: flex-start;
    }

    .stApp {
        background: linear-gradient(to bottom, #fdfefe, #f5f6fa);
    }

    .sidebar .sidebar-content {
        background-color: #2d3436 !important;
        color: #fff;
        padding-top: 5rem;
    }

    .sidebar .sidebar-content .st-emotion-cache-6qob1r {
        background: #2d3436 !important;
        color: #fff !important;
    }

    input[type="text"] {
        border-radius: 12px;
        padding: 12px;
        border: 1px solid #b2bec3;
        width: 100%;
        background: #ffffff;
    }

    input[type="text"]:focus {
        border-color: #74b9ff;
        outline: none;
        box-shadow: 0 0 4px rgba(116, 185, 255, 0.6);
    }

    button {
        border-radius: 10px !important;
        padding: 10px;
        background-color: #74b9ff !important;
        color: white !important;
        font-weight: 600 !important;
    }

    button:hover {
        transform: scale(1.03);
        background-color: #0984e3 !important;
        transition: 0.2s ease-in-out;
    }

    .st-emotion-cache-12fmjuu {
        top: 0px;
        left: 0px;
        right: 0px;
        height: 3.75rem;
        background: rgb(255, 255, 255);
        outline: none;
        z-index: 10;
        display: block;
    }

    .st-emotion-cache-4uzi61 {
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-radius: 0.5rem;
        padding: calc(-1px + 1rem);
        position: fixed;
        bottom: 3.5rem;
    }
</style>
""", unsafe_allow_html=True)



# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

def query_ollama(prompt, model="llama3"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["response"]

def build_prompt_with_memory(user_input):
    conversation = "\n".join(st.session_state.history)
    return f"{conversation}\nUser: {user_input}\nAssistant:"

# Sticky Header
st.markdown("""
<div class="sticky-header">
    <h1>💬 Ollama Chatbot</h1>
</div>
""", unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.title("⚙️ Settings")
    model_name = st.selectbox(
        "Select Model",
        ["llama3", "mistral", "gemma", "custom"],
        index=0,
        help="Choose which LLM model to use"
    )

    st.markdown("---")
    st.subheader("📘 About")
    st.markdown("This chatbot runs locally using **Ollama** and maintains your conversation during this session.")

    if st.button("🧹 Clear Conversation", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# Main content with spacing for sticky header/footer
st.markdown('<div class="main-content">', unsafe_allow_html=True)

chat_container = st.container()

# Display chat history
with chat_container:
    for entry in st.session_state.history:
        if entry.startswith("User:"):
            with st.chat_message("user"):
                st.markdown(entry[6:])
        elif entry.startswith("Assistant:"):
            with st.chat_message("assistant"):
                st.markdown(entry[10:])

# Input form
with st.form("chat_input_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input(
            "Your message",
            placeholder="Type your message here...",
            label_visibility="collapsed",
            key="user_input"
        )
    with col2:
        submit_button = st.form_submit_button("Send", use_container_width=True)

# Handle user input
if submit_button and user_input:
    full_prompt = build_prompt_with_memory(user_input)
    st.session_state.history.append(f"User: {user_input}")

    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("Thinking..."):
                try:
                    response = query_ollama(full_prompt, model=model_name)
                    response = response.strip()
                    response_placeholder.markdown(response)
                    st.session_state.history.append(f"Assistant: {response}")
                except Exception as e:
                    response_placeholder.error(f"Error: {e}")
                    st.session_state.history.pop()

# Close main-content div
st.markdown('</div>', unsafe_allow_html=True)

# Sticky Footer
st.markdown("""
<div class="sticky-footer">
    🚀 A locally-powered AI assistant with memory · Built with ❤️ using Streamlit & Ollama
</div>
""", unsafe_allow_html=True)