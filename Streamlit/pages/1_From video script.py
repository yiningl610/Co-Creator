import streamlit as st
import google.generativeai as genai
from utils import logo,Title

genai.configure(api_key=st.secrets["textAPI"])

st.set_page_config(page_title="Script",
                   layout="wide",
                   page_icon="📈")

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
    promptTitle = ["Based on the target audience, and the feeling it evokes. Focus on the benefits viewers will get. Give me just 3 titles without sub categories and no tips, Brainstorm some click-worthy titles based on idea: ",inputs]
    promptDescription = ["Craft a captivating description under 150 words, weaving vivid language, intriguing questions, and a clear call to action for the YouTube video mentioned above. Think about the video's core theme, target audience, and desired emotional response (curiosity, excitement, etc.). Include specific keywords if relevant. Remember, the key is to make the video stand out as a hidden gem, enticing viewers to click play and delve deeper! Give me just 3 descriptions with no sub-categories or tips: ",inputs]
    promptThumbnail = ["Give me suggestions on how to make the thumbnail for this video idea attractive: ",inputs]
    promptTags = ["Create a list of 5 relevant hashtags for YouTube video. Include a mix of high-volume and low-volume hashtags, targeting the specific audience and niche of the video. based on idea: ",inputs]

    model = genai.GenerativeModel('gemini-pro')
    with st.spinner("Generating..."):
      responseTitle = model.generate_content(promptTitle,request_options={"timeout": 600})
      responseDescription = model.generate_content(promptDescription,request_options={"timeout": 600})
      responseThumbnail = model.generate_content(promptThumbnail,request_options={"timeout": 600})
      responseTags = model.generate_content(promptTags,request_options={"timeout": 600})
    
    tab1, tab2, tab3, tab4 = st.tabs(["Titles", "📍Description", "Thumbnails", "Tags"])
    with tab1:
        st.write(responseTitle.text)
    with tab2:
        st.write(responseDescription.text)
    with tab3:
        st.write(responseThumbnail.text)
    with tab4:
        st.write(responseTags.text)

