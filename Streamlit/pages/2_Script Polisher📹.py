import streamlit as st
import google.generativeai as genai
import asyncio
from utils import *

genai.configure(api_key=st.secrets["textAPI"])

st.set_page_config(page_title="Script",
                   layout="wide",
                   page_icon="📈")

logo()
Title()

st.title("Script Polisher")
st.markdown("""
            Upload your script, tell us who you're aiming to reach and the emotions you want to evoke, and we'll provide insightful suggestions
            
            Click Generate botton to redo it if you are not satisfied with the suggestion.
            """)

inputs = None
script = None

target = st.text_input("Enter your target audience here:")
tone = st.text_input("Enter your desired tone here:")
uploaded_file = st.file_uploader("Upload your video script here", type="txt")
if uploaded_file is not None:
  script = uploaded_file.read().decode("utf-8")
else:
  st.info("Please upload your video script.")

ready = st.button("Generate")

if ready and script is not None:
    inputs = "".join(['script content:',script, 'target audience:', target, 'video tone:', tone])
    if inputs is not None:
      promptMusic = ["Based on the target audience, and the feeling it evokes. Focus on the benefits viewers will get. Give me three type of music and three example music of each type that I can use in the video based on the video script, with only the music type itself been listed.",inputs]
      promptColor = ["Based on the target audience, and the feeling it evokes. Focus on the benefits viewers will get. Give me some suggestion on the color palette and how I can use them for text based on the video script, present the color with name and Hex color codes.",inputs]
      promptEdit = ["Based on the target audience, and the feeling it evokes. Focus on the benefits viewers will get. Give me some suggestion on the editing style based on the video script, no need to present the benefits detail, but give editing suggestion for each section of the script.",inputs]
      
      model = genai.GenerativeModel('gemini-pro')
                  
      with st.spinner("Generating..."):
        responseMusic = model.generate_content(promptMusic,request_options={"timeout": 600})
        responseColor = model.generate_content(promptColor,request_options={"timeout": 600})
        responseThumbnail = model.generate_content(promptEdit,request_options={"timeout": 600})
        
      tab1, tab2, tab3 = st.tabs(["BGM Music", "Color Palette", "Editing Style"])
      with tab1:
          st.write(responseMusic.text)
      with tab2:
          st.write(responseColor.text)
      with tab3:
          st.write(responseThumbnail.text)


