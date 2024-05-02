import streamlit as st
import google.generativeai as genai
from utils import *

genai.configure(api_key=st.secrets["textAPI"])

st.set_page_config(page_title="Script",
                   layout="wide",
                   page_icon="📈")

logo()
Title()

st.title("Script Making")
st.markdown("""
            Simply provide the key points you want to convey and the type of video you're aiming for, and we'll generate a sample script as a foundation. This springboard will help you organize your thoughts, establish a clear narrative flow, and get you started on the path to a captivating video.
            
            If you are not satisfied with the sample, simplly click Generate botton to redo it!
            
            You can also download the sample script to use as a starting point for your own script.
            """)

type = st.text_input("Enter the type of video you want to create:")
content = st.text_area("Enter all the content you want to present in the video here:")
inputs = None 

if type and content:
    inputs = "".join(['video content:',content,'video type:',type])
# else:
#     st.info("Please present your idea.")
    
ready = st.button("Generate Script")

if ready and inputs is not None:
      promptScript = ["I want to create a video of this type, and I want all these content to be in the video, please create a video script base on them:",inputs]
      
      model = genai.GenerativeModel('gemini-pro')
                  
      with st.spinner("Generating..."):
        responseScript = model.generate_content(promptScript,request_options={"timeout": 600})
        
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