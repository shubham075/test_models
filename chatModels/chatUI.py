import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Personality ChatBot",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

.main {
    background: linear-gradient(135deg,#0f172a,#111827);
}

.title {
    text-align:center;
    font-size:42px;
    font-weight:700;
    color:white;
    margin-bottom:5px;
}

.subtitle {
    text-align:center;
    color:#94a3b8;
    margin-bottom:25px;
}

.stChatMessage {
    border-radius:15px;
}

.personality-box {
    padding:15px;
    border-radius:15px;
    background-color:#1e293b;
    color:white;
    text-align:center;
    margin-bottom:10px;
}

[data-testid="stSidebar"] {
    background-color:#0f172a;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD ENV
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# MODEL
# --------------------------------------------------
@st.cache_resource
def load_model():
    return ChatMistralAI(
        model_name="mistral-medium-3-5",
        temperature=0.9
    )

model = load_model()

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    '<div class="title">🤖 AI Personality ChatBot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Choose a personality and start chatting</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:

    st.header("🎭 Select Personality")

    personality = st.radio(
        "",
        [
            "😡 Angry",
            "😂 Funny",
            "😢 Sad"
        ]
    )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        if personality == "😡 Angry":
            mode = "You are a Angry and impatience AI agent"

        elif personality == "😂 Funny":
            mode = "You are a funny AI agent"

        else:
            mode = "You are a Sad AI agent"

        st.session_state.messages = [
            SystemMessage(content=mode)
        ]

        st.rerun()

# --------------------------------------------------
# PERSONALITY LOGIC
# --------------------------------------------------
if personality == "😡 Angry":
    mode = "You are a Angry and impatience AI agent"

elif personality == "😂 Funny":
    mode = "You are a funny AI agent"

else:
    mode = "You are a Sad AI agent"

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]

# Reset if personality changes
if (
    len(st.session_state.messages) > 0 and
    st.session_state.messages[0].content != mode
):
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]

# --------------------------------------------------
# CURRENT PERSONALITY CARD
# --------------------------------------------------
st.markdown(
    f"""
    <div class="personality-box">
        Current Personality: <b>{personality}</b>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------
for msg in st.session_state.messages[1:]:

    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------
prompt = st.chat_input("Type your message...")

if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    response = model.invoke(
        st.session_state.messages
    )

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    with st.chat_message("assistant"):
        st.markdown(response.content)