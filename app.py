import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model
model = genai.GenerativeModel("gemini-2.5-flash")

# Page Configuration
st.set_page_config(page_title="Be-Rozgaari", page_icon="💼")
st.title("Be-Rozgaari Bot 💼")
st.write("Helping you find your next career move based on your skills and interests.")

# 1. Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Sidebar: Download and Management
with st.sidebar:
    st.header("Chat Options")
    
    # Download Chat History
    if st.session_state.messages:
        # Convert list of dicts to a single string for the file
        full_chat = ""
        for m in st.session_state.messages:
            full_chat += f"{m['role'].upper()}: {m['content']}\n\n"
        
        st.download_button(
            label="📩 Download Chat History",
            data=full_chat,
            file_name="job_recommendations_log.txt",
            mime="text/plain"
        )
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Input Logic
if user_input := st.chat_input("Tell me about your skills, education, or preferred role..."):
    
    # Add user message to history and UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 5. Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing job markets..."):
            # System instructions tailored for job recommendations
            system_instruction = """
            You are a professional Career Advisor. Your goal is to provide specific job recommendations 
            based on the user's skills, interests, and background. 
            - Suggest roles that match their profile.
            - Provide brief descriptions of why these jobs fit.
            - Mention 1-2 key skills they might need to improve.
            - Keep the tone professional and encouraging.
            """
            
            # Combine history for context
            prompt = f"{system_instruction}\n\nUser Question: {user_input}\nAssistant Recommendation:"
            
            try:
                response = model.generate_content(prompt)
                ai_text = response.text
                st.markdown(ai_text)
                
                # Save assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": ai_text})
            except Exception as e:
                st.error(f"Error: {e}")