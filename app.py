import streamlit as st
import json, os

from utils.summarizer import summarize
from utils.quiz import generate_quiz
from utils.flashcards import generate_flashcards
from utils.pdf_generator import create_pdf
from utils.llm import generate_ai

# ---------------- FILES ----------------
HISTORY_FILE = "history.json"
IMPORTANT_FILE = "important.json"

# ---------------- SESSION ----------------
if "result" not in st.session_state:
    st.session_state.result = ""

# ---------------- FUNCTIONS ----------------
def save_history(text, result):
    data = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

    data.append({"query": text, "answer": result})

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_important(text, result):
    data = []
    if os.path.exists(IMPORTANT_FILE):
        try:
            with open(IMPORTANT_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

    data.append({"query": text, "answer": result})

    with open(IMPORTANT_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_important():
    if os.path.exists(IMPORTANT_FILE):
        try:
            with open(IMPORTANT_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

# ---------------- UI ----------------
st.set_page_config(page_title="AI Study Buddy", layout="wide")
st.title("📘 AI Study Buddy")

option = st.sidebar.selectbox("Choose Feature", [
    "Explain Topic",
    "Summarize Notes",
    "Generate Quiz",
    "Flashcards"
])

text = st.text_area("Enter your topic / notes", height=300)

# ---------------- GENERATE ----------------
if st.button("Generate"):

    if option == "Explain Topic":
        st.session_state.result = generate_ai("Explain in simple words:\n" + text)

    elif option == "Summarize Notes":
        st.session_state.result = summarize(text)

    elif option == "Generate Quiz":
        st.session_state.result = generate_quiz(text)

    elif option == "Flashcards":
        st.session_state.result = generate_flashcards(text)

    st.write(st.session_state.result)

    save_history(text, st.session_state.result)

# ---------------- RESULT ACTIONS ----------------
if st.session_state.result:

    st.subheader("Result:")
    st.write(st.session_state.result)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⭐ Save as Important"):
            save_important(text, st.session_state.result)
            st.success("Saved to Important Notes!")

    with col2:
        pdf = create_pdf(st.session_state.result)
        with open(pdf, "rb") as f:
            st.download_button(
                label="📥 Download PDF",
                data=f.read(),
                file_name=pdf,
                mime="application/pdf"
            )

# ---------------- SIDEBAR HISTORY ----------------
st.sidebar.subheader("🔍 Search History")

history = load_history()

for idx, h in enumerate(history):
    if st.sidebar.button("👉 " + h["query"], key="his"+str(idx)):
        st.session_state.result = h["answer"]
if st.sidebar.button("🗑 Clear History"):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)
    st.rerun()
# ---------------- SIDEBAR IMPORTANT ---------------
st.sidebar.subheader("⭐ Important Notes")

important_notes = load_important()

for idx, i in enumerate(important_notes):
    col1, col2 = st.sidebar.columns([3,1])

    with col1:
        if st.button("⭐ " + i["query"], key="imp"+str(idx)):
            st.session_state.result = i["answer"]

    with col2:
        if st.button("❌", key="del"+str(idx)):
            important_notes.pop(idx)
            with open(IMPORTANT_FILE, "w") as f:
                json.dump(important_notes, f, indent=4)
            st.rerun()