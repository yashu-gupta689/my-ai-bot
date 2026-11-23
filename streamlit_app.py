import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL = "gemini-flash-latest"
SYSTEM_PROMPT = "You are Jarvis, my personal assistant. Reply in Hinglish. Be concise."

st.title("Jarvis")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Kuch poochho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages[-20:]
    try:
        reply = client.chat.completions.create(model=MODEL, messages=msgs).choices[0].message.content
    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)