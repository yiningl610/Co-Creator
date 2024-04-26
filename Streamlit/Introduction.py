import streamlit as st
from utils import logo,Title

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# st.sidebar.image("logo.png",width=100)
    
logo()
Title()

st.write("# Welcome to Co-Creater! 👋")

st.markdown(
    """
    I am Youtuber helper from GeminiAI!
    
    You can tell me your idea of a video, the exact video script you have or a finalized video.**👈 Select a way from the sidebar**
    I will suggest you with
    
    - An attractive title
    - The best time to upload the video
    - Thumbnail design tips
    - Description box examples
    - Hashtags you canuse to raise more views
    - Editing style tips (For undone videos only)
"""
)