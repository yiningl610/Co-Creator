import streamlit as st
import time
import numpy as np
import google.generativeai as genai
genai.configure(api_key="AIzaSyDQNefLOl-iHbpDc5omHuGgTkJVdGTX_PM")

st.set_page_config(page_title="Script", page_icon="📈")

logo_html = f"""
<style>
img {{
  position: absolute;
  top: 0;
  left: 0;  /* Change to 'right: 0' for top-right corner */
}}
</style>
<img src="logo.png" alt="Your Company Logo" style="width: 100px; height: auto;">
"""
st.write(logo_html, unsafe_allow_html=True)

# 大标题
st.markdown("# From video script")
# 边栏标题
st.sidebar.header("Helper from video script")
st.write(
    """This page provides help you to create a successful youtube video from just an idea."""
)

# Define options for selection
options = ["Simple idea", "Specific video script"]

# Use radio or selectbox for selection
selection = st.selectbox("Choose the way you want to express your idea:", options)
idea = None
target = None
tone = None
inputs = None

# Get user input based on selection

if selection == "Simple idea":
  # Text input section
  idea = st.text_input("Enter your idea here:")
  target = st.text_input("Enter your target audience here:")
  tone = st.text_input("Enter your desired tone here:")
  if idea and target and tone:
    inputs = "".join(['idea:',idea, 'target audience:', target, 'video tone:', tone])
  else:
    st.write("Please present your idea.")

    
elif selection == "Specific video script":
  # Text file upload section
  uploaded_file = st.file_uploader("Upload your video script here", type="txt")
  if uploaded_file is not None:
    inputs = uploaded_file.read().decode("utf-8")
  else:
    st.write("Please upload your video script.")

# Display user input

if inputs is not None:
# Things I want Gemini to do
    promptTitle = ["Give me some attractive titles of youtube video for: ",inputs]
    promptDescription = ["Give me an example of youtube video description: ",inputs]
    promptThumbnail = ["Give me suggestions on how to make the thumbnail for this video idea attractive: ",inputs]
    promptTags = ["Give me some hastags I can use for this video of idea: ",inputs]

    # Model response
    model = genai.GenerativeModel('gemini-pro')
    with st.spinner("Generating..."):
      responseTitle = model.generate_content(promptTitle,request_options={"timeout": 600})
      responseDescription = model.generate_content(promptDescription,request_options={"timeout": 600})
      responseThumbnail = model.generate_content(promptThumbnail,request_options={"timeout": 600})
      responseTags = model.generate_content(promptTags,request_options={"timeout": 600})
    

    tab1, tab2, tab3, tab4 = st.tabs([ "Example", "Titles", "Thumbnails", "Tags"])
    with tab1:
        st.write(responseDescription.text)
    with tab2:
        st.write(responseTitle.text)
    with tab3:
        st.write(responseThumbnail.text)
    with tab4:
        st.write(responseTags.text)

