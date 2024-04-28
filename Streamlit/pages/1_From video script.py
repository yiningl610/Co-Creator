import streamlit as st
import google.generativeai as genai
from utils import logo,Title

genai.configure(api_key="AIzaSyDQNefLOl-iHbpDc5omHuGgTkJVdGTX_PM")

st.set_page_config(page_title="Script", page_icon="📈")

logo()
Title()

st.markdown("# From video script")
st.write(
    """This page provides help you to create a successful youtube video from just an idea."""
)

options = ["Simple idea", "Specific video script"]
selection = st.selectbox("Choose the way you want to express your idea:", options)

idea = None
target = None
tone = None
inputs = None
if selection == "Simple idea":
  idea = st.text_input("Enter your idea here:")
  target = st.text_input("Enter your target audience here:")
  tone = st.text_input("Enter your desired tone here:")
  if idea and target and tone:
    inputs = "".join(['idea:',idea, 'target audience:', target, 'video tone:', tone])
  else:
    st.write("Please present your idea.")
elif selection == "Specific video script":
  uploaded_file = st.file_uploader("Upload your video script here", type="txt")
  if uploaded_file is not None:
    inputs = uploaded_file.read().decode("utf-8")
  else:
    st.write("Please upload your video script.")
    
if inputs is not None:
    promptTitle = ["Give me some attractive titles of youtube video for: ",inputs]
    promptDescription = ["Give me an example of youtube video description: ",inputs]
    promptThumbnail = ["Give me suggestions on how to make the thumbnail for this video idea attractive: ",inputs]
    promptTags = ["Give me some hastags I can use for this video of idea: ",inputs]

    model = genai.GenerativeModel('gemini-pro')
    with st.spinner("Generating..."):
      responseTitle = model.generate_content(promptTitle,request_options={"timeout": 600})
      responseDescription = model.generate_content(promptDescription,request_options={"timeout": 600})
      responseThumbnail = model.generate_content(promptThumbnail,request_options={"timeout": 600})
      responseTags = model.generate_content(promptTags,request_options={"timeout": 600})
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([ "Example", "Titles", "Thumbnails", "Tags","Ex"])
    with tab1:
        st.write(responseDescription.text)
    with tab2:
        st.write(responseTitle.text)
    with tab3:
        st.write(responseThumbnail.text)
    with tab4:
        st.write(responseTags.text)
    with tab5:
        st.write(inputs)


