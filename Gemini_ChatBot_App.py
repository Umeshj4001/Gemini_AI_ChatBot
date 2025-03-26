import streamlit as st
import os
import google.generativeai as genai

# API Key Configuration
os.environ['GEMINI_API_KEY'] = 'AIzaSyDNDO7PM8kB9oQZ_9raS0IDxVa94tsDBBc'
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# Categorized Models
image_models = [
    'gemini-2.0-flash-exp-image-generation'
]

text_models = [
    'gemini-2.0-flash-exp',
    'gemini-2.0-flash',
    'gemini-2.0-flash-001',
    'gemini-2.0-flash-lite-001',
    'gemini-2.0-flash-lite',
    'gemini-2.0-flash-lite-preview-02-05',
    'gemini-2.0-flash-lite-preview',
    'gemini-2.0-pro-exp',
    'gemini-2.0-flash-thinking-exp',
    'gemini-2.0-flash-thinking-exp-1219',
    'learnlm-1.5-pro-experimental',
    'gemma-3-27b-it'
]

# Streamlit setup
st.set_page_config(page_title="UJ's Gemini Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Gemini AI Chatbot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = None

# Sidebar for Chat History
with st.sidebar : 
    st.title("🤖 Gemini AI Chatbot")
    category = st.selectbox("Choose Model Type", ["Text Generation", "Image Generation"])
    filtered_models = image_models if category == "Image Generation" else text_models
    selected_model = st.selectbox("Select Model", filtered_models)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📜 Chat History")
    with col2:
        if st.button("🗑️ Clear"):
            st.session_state.chat_history.clear()
            st.session_state.selected_chat = None
            st.experimental_rerun()


    if st.session_state.chat_history:
        for idx, chat in enumerate(st.session_state.chat_history):
            if st.sidebar.button(f"🗨️ {chat['question']}", key=f"chat_{idx}"):
                st.session_state.selected_chat = chat
    else:
        st.sidebar.info("No chat history yet.")


# Function to get Gemini response
def get_gemini_response(question, model_name):
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    answer_text = ""
    for chunk in response:
        if hasattr(chunk, 'text'):
            answer_text += chunk.text
    return answer_text

# Chat input
chat_input = st.chat_input("Type your message and press Enter...")

if chat_input:
    st.write(f"Using Model : **{selected_model}**")
    answer = get_gemini_response(chat_input, selected_model)
    with st.chat_message("user"):
        st.write(chat_input)
    with st.chat_message("assistant"):
        st.write("The Response is :")
        st.write(answer)

    # Save to chat history
    st.session_state.chat_history.append({"question" : chat_input, "answer": answer})

# Display selected chat from history
if st.session_state.selected_chat:
    st.subheader("Selected Chat Response :")
    with st.chat_message("user"):
        st.session_state.selected_chat['question']
    with st.chat_message("assistant"):
        st.session_state.selected_chat['answer']
    
# Footer - Built by Umesh
# st.markdown("<hr>", unsafe_allow_html=True)
# st.markdown("<p style='text-align: right; color: grey;'>Built by Umesh</p>", unsafe_allow_html=True)

