import streamlit as st
from utils import logo,Title

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# st.sidebar.image("logo.png",width=100)
    
logo()
Title()

st.write("# Welcome to Co-Creator, your Gemini-Powered Video Creation Companion!")

st.markdown(
    """
    Co-Creator is your one-stop shop for crafting the perfect video, from start to finish. Whether you're a seasoned content creator or a complete beginner, we're here to empower your creativity and streamline the process.
    
    Here's how Co-Creator can be your partner in video creation:

    ### Scriptwriting Made Easy

    Struggling with writer's block? No problem! Simply input your desired video type (e.g., explainer, product demo, vlog) and the key information you want to convey. Co-Creator will generate a sample script, giving you a solid foundation to build upon.

    ### Script Refinement and Style Suggestions

    Already have a script in mind? Upload it and tell Co-Creator about your target audience and the tone you want to achieve. Co-Creator will analyze your script and suggest music styles, color palettes, and editing techniques that perfectly complement your vision.

    ### Video Optimization for Maximum Reach

    Uploaded a finished video but need that extra polish? Co-Creator will analyze your video and suggest an eye-catching title, engaging description content, relevant hashtags, and even generate a thumbnail design to grab attention.

    Think of Co-Creator as your creative collaborator, offering intelligent suggestions and Gemini-powered tools to streamline your video creation process. So, let's get started! Tell us your vision; Co-Creator will help you turn it into a captivating video.
"""
)
