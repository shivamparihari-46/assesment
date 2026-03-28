import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm =  ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=st.secrets["GOOGLE_API_KEY"],temperature=0
)
def check_relevance(user_input):
    prompt = f"""
    You are a classifier.

    User input: "{user_input}"

    Check if this input is relevant to a hiring assistant conversation 
    (like answering questions, giving details, etc.)

    Respond ONLY in one word:
    YES or NO
    """

    response = llm.invoke(prompt).content.strip()
    return response

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")

st.title("🤖 TalentScout Hiring Assistant")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.data = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

questions = [
    "What is your full name?",
    "Enter your email address:",
    "Enter your phone number:",
    "Years of experience?",
    "Desired role?",
    "Current location?",
    "List your tech stack (comma separated):"
]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if st.session_state.step == 0 and len(st.session_state.messages) == 0:
    greeting = "Hello! 👋 I am your Hiring Assistant. I will collect some details and then ask technical questions."
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.rerun()

user_input = st.chat_input("Type your response...")

if user_input:
    if st.session_state.step <=1:
        pass
    else:
        relevance = check_relevance(user_input)

        if relevance == "NO":
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Sorry, I did not understand your context. Could you please rephrase?"
            })
            st.rerun()
    if user_input.lower() in ["exit", "bye", "quit"]:
        st.session_state.messages.append({"role": "assistant", "content": "Thank you! We'll get back to you soon."})
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})

    if st.session_state.step > 0 and st.session_state.step <= len(questions):
        key = questions[st.session_state.step - 1]
        st.session_state.data[key] = user_input

    st.session_state.step += 1

    if st.session_state.step <= len(questions):
        next_q = questions[st.session_state.step - 1]
        st.session_state.messages.append({"role": "assistant", "content": next_q})

    elif st.session_state.step == len(questions) + 1:
        tech_stack = st.session_state.data.get("List your tech stack (comma separated):", "")

        prompt = f"""
        You are a technical interviewer.
        Based on this tech stack: {tech_stack}
        Generate 3-5 interview questions for each technology.
        Keep them medium difficulty.
        """

        response = llm.invoke(prompt)

        st.session_state.messages.append({"role": "assistant", "content": "Here are your technical questions:"})
        st.session_state.messages.append({"role": "assistant", "content": response.content})

        st.session_state.messages.append({
            "role": "assistant",
            "content": "Thanks for your time! Our team will review your responses."
        })

    st.rerun()


