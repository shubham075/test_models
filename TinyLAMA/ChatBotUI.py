import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="TinyLlama Chat",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #111827);
}

.main-title {
    text-align: center;
    color: white;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0;
}

.sub-title {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

.bot-card {
    background-color: rgba(255,255,255,0.05);
    padding: 12px;
    border-radius: 15px;
    margin-bottom: 15px;
}

.user-card {
    background-color: rgba(59,130,246,0.15);
    padding: 12px;
    border-radius: 15px;
    margin-bottom: 15px;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD ENV
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------
@st.cache_resource
def load_model():

    llm = HuggingFacePipeline.from_model_id(
        model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        task="text-generation",
        pipeline_kwargs={
            "max_new_tokens": 100,
            "temperature": 0.1,
        }
    )

    return ChatHuggingFace(llm=llm)

chat_model = load_model()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    '<div class="main-title">🤖 TinyLlama Chat</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Local LLM Powered by Hugging Face</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:

    st.title("⚙️ Settings")

    st.success("Model Running Locally")

    st.markdown("""
    **Model**
    - TinyLlama-1.1B-Chat

    **Temperature**
    - 0.1

    **Inference**
    - Local Machine
    """)

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# --------------------------------------------------
# DISPLAY HISTORY
# --------------------------------------------------
for chat in st.session_state.chat_history:

    if chat["role"] == "user":
        st.markdown(
            f"""
            <div class="user-card">
                <b>🧑 You</b><br>
                {chat["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"""
            <div class="bot-card">
                <b>🤖 TinyLlama</b><br>
                {chat["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------------------------------
# INPUT
# --------------------------------------------------
prompt = st.chat_input("Ask TinyLlama something...")

if prompt:

    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt
    })

    with st.spinner("Thinking..."):

        response = chat_model.invoke(prompt)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response.content
    })

    st.rerun()