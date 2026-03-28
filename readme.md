# TalentScout Hiring Assistant 🤖

## Overview
This is an AI-powered chatbot that collects candidate information and generates technical interview questions based on their tech stack.

## Features
- Collect candidate details
- Tech stack-based question generation
- Context-aware chat
- Exit handling

## Setup
1. Clone repo
2. Install requirements:
   pip install -r requirements.txt

3. Add .env file:
   GOOGLE_API_KEY=your_key_here

4. Run:
   streamlit run app.py

## Tech Used
- Streamlit
- LangChain
- Google Gemini API

## Prompt Design
- Separate prompt for question generation
- Controlled output format

## Challenges
- Managing conversation flow
- Handling user exits
- Maintaining session state