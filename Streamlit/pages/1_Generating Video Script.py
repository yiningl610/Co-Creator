import streamlit as st
import google.generativeai as genai
from utils import *

genai.configure(api_key=st.secrets["textAPI"])

st.set_page_config(page_title="Script",
                   layout="wide",
                   page_icon="📈")

logo()
Title()

st.markdown("### This page help you to create a successful youtube video from just an idea")

type = st.text_input("Enter the type of video you want to create:")
idea = st.text_area("Enter your idea here:")
inputs = None 

if type and idea:
    inputs = "".join(['video content:',idea,'video type:',type])
else:
    st.info("Please present your idea.")
    
ready = st.button("Generate")

if ready and inputs is not None:
      promptScript = ["I want to create a video of this type, and I want all these content to be in the video, please create a video script base on them:",idea]
    #   promptDescription = ["Craft a captivating description under 150 words, weaving vivid language, intriguing questions, and a clear call to action for the YouTube video mentioned above. Think about the video's core theme, target audience, and desired emotional response (curiosity, excitement, etc.). Include specific keywords if relevant. Remember, the key is to make the video stand out as a hidden gem, enticing viewers to click play and delve deeper! Give me just 3 descriptions with no sub-categories or tips: ",inputs]
    #   promptThumbnail = ["Give me suggestions on how to make the thumbnail for this video idea attractive: ",inputs]
    #   promptTags = ["Create a list of 5 relevant hashtags for YouTube video. Include a mix of high-volume and low-volume hashtags, targeting the specific audience and niche of the video. based on idea: ",inputs]
      
      model = genai.GenerativeModel('gemini-pro')
                  
      with st.spinner("Generating..."):
        responseScript = model.generate_content(promptScript,request_options={"timeout": 600})
        # responseDescription = model.generate_content(promptDescription,request_options={"timeout": 600})
        # responseThumbnail = model.generate_content(promptThumbnail,request_options={"timeout": 600})
        # responseTags = model.generate_content(promptTags,request_options={"timeout": 600})
      
      with st.container():      
        st.write(responseScript.text)
      
      @st.cache_data
      def to_text():
        return "### Script ###\n\n" + responseScript.text

      btn = st.download_button(
              label="Download Sample",
              data=to_text(),
              file_name="sampleScript.txt"
            )