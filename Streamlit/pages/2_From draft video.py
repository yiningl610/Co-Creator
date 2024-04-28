import streamlit as st
import google.generativeai as genai
from utils import *

genai.configure(api_key="AIzaSyBs5rT5G2cM-d2p_Un15THLq1Q7tYsJ9kU")

logo()
Title()

st.title("YouTube Video Description & Improvement Assistant")

uploaded_file = st.file_uploader("Upload your video", type=['mp4'])

if uploaded_file is not None:

  st.write(f"**Uploaded video:** {uploaded_file.name}")

  # Extract frames from uploaded video
  extract_frame_from_video(uploaded_file)
  

    # Process each frame in the output directory
  files = os.listdir(FRAME_EXTRACTION_DIRECTORY)
  files = sorted(files)
  files_to_upload = []
  for file in files:
    files_to_upload.append(
        File(file_path=os.path.join(FRAME_EXTRACTION_DIRECTORY, file)))
  
  # Upload the files to the API
  # Only upload a 10 second slice of files to reduce upload time.
  # Change full_video to True to upload the whole video.
  full_video = True
  
  uploaded_files = []
  print(f'Uploading {len(files_to_upload) if full_video else 10} files. This might take a bit...')
  
  for file in files_to_upload if full_video else files_to_upload[:10]:
      print(f'Uploading: {file.file_path}...')
      response = genai.upload_file(path=file.file_path)
      file.set_file_response(response)
      uploaded_files.append(file)
  
  print(f"Completed file uploads!\n\nUploaded: {len(uploaded_files)} files")
# Description generation (placeholder using user input)
  # Create the prompt.
  promptTitle = "Give me some attractive titles of the video for posting youtube videos"
  promptDescription = "Give me some examples of the video description for posting on youtube"
  promptThumbnail = "Give me suggestions on how to make the thumbnail for this video idea attractive"
  promptTags = "Give me some hastags I can use for posting this video on youtube"

  # Set the model to Gemini 1.5 Pro.
  model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
  
  # Make the LLM request.
  requestTitle = make_request(promptTitle, uploaded_files)
  responseTitle = model.generate_content(requestTitle, request_options={"timeout": 600})

  requestDescription = make_request(promptDescription, uploaded_files)
  responseDescription = model.generate_content(requestDescription, request_options={"timeout": 600})

  requestThumbnail = make_request(promptThumbnail, uploaded_files)
  responseThumbnail = model.generate_content(requestThumbnail,request_options={"timeout": 600})

  requestTags = make_request(promptTags, uploaded_files)
  responseTags = model.generate_content(requestTags, request_options={"timeout": 600})
  
  tab1, tab2, tab3, tab4 = st.tabs(["Titles", "Descriptions", "Thumbnails", "Tags"])
  with tab1:
      st.write(responseTitle.text)
  with tab2:
      st.write(responseDescription.text)
  with tab3:
      st.write(responseThumbnail.text)
  with tab4:
      st.write(responseTags.text)

