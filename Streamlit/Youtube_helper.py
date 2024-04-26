import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

logo_html = f"""
<style>
img {{
  position: absolute;
  top: 0;
  left: 0;  /* Change to 'right: 0' for top-right corner */
}}
</style>
<img src="logo.png" alt="Logo" style="width: 100px; height: auto;">
"""
st.write(logo_html, unsafe_allow_html=True)

st.write("# Welcome to Youtuber Helper! 👋")

st.markdown(
    """
    I am Youtube Helper from GeminiAI!
    
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