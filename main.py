import streamlit as st
from chat_engine import ChatBot
import json

st.set_page_config(
    page_icon="🤖",
    page_title="Ask-Bot",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

def initialize_session_state():
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ChatBot(st.secrets["GROQ_API"])

initialize_session_state()

with st.sidebar:
    st.subheader("", divider="gray")
    st.header(':violet[Gen AI Assistant]') 
    selected_model = st.selectbox(
        ":grey-background[LLM Model]", 
        options=list(ChatBot.AVAILABLE_MODELS.keys()),
        format_func=lambda x: ChatBot.AVAILABLE_MODELS[x],
        key="model_select"
    )
    
    if selected_model != st.session_state.chatbot.model_name:
        st.session_state.chatbot.update_model(selected_model)
    thread_id = "1"
    
    if not st.session_state.chat_started:
        if st.button("Start Chat Session", use_container_width=True):
            st.session_state.chat_started = True
            st.session_state.messages = []
            st.rerun() 
    else:
        if st.button("End Chat Session", use_container_width=True, type="primary"):
            st.session_state.chat_started = False
            st.rerun()
        
        st.divider()
        
        # note : if u want to show the session history in json format uncomment below lines
        #with st.expander("Session History (JSON)", expanded=False):
            #st.json(st.session_state.messages)
        
        def set_input(suggestion):
            st.session_state.user_input = suggestion
            
        #for suggestion in suggestions:
        #    st.button(suggestion, on_click=set_input, args=(suggestion,), use_container_width=True)

st.subheader("၊၊||၊ :violet[ChatBot] ၊၊||၊", divider="gray")

if st.session_state.chat_started:
    if not st.session_state.messages:
        hello_message = ":sparkles: Hello, How can I help you ?"
        st.session_state.messages = [{"role": "assistant", "content": hello_message}]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is your message?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.session_state.chatbot.chat(prompt, thread_id)
            response_content = response["messages"][-1].content
            response_str = ""
            response_container = st.empty()
            for token in response_content:
                response_str += token
                response_container.markdown(response_str)
            st.session_state.messages.append(
                {"role": "assistant", "content": response["messages"][-1].content}
            )


# to hide the menue deployement from streamlit app add this code
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# to hide the anchor link from the header of streamlit app add this code
hide_anchor_link = """
    <style>
    /* Hide link icon next to headers */
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
    </style>
"""
st.markdown(hide_anchor_link, unsafe_allow_html=True)












