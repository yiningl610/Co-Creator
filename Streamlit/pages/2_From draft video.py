import streamlit as st
import cv2
import os
import shutil
import google.generativeai as genai
import tempfile
from utils import logo,Title

genai.configure(api_key="AIzaSyBs5rT5G2cM-d2p_Un15THLq1Q7tYsJ9kU")

logo()
Title()

# Function to create or cleanup the frame extraction directory
def create_frame_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

# Function to extract frames from video (1 frame/second for demonstration)
def extract_frame_from_video(upload_file):
    create_frame_output_dir(FRAME_EXTRACTION_DIRECTORY)
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
      temp_file.write(uploaded_file.read())
      file_path = temp_file.name
    #bytes_data = upload_file.read()
    vidcap = cv2.VideoCapture(file_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_duration = 1 / fps
    output_file_prefix = os.path.basename(upload_file.name).replace('.', '_')
    frame_count = 0
    count = 0
    while vidcap.isOpened():
      success, frame = vidcap.read()
      if not success:
        break
      if int(count / fps) == frame_count:
        min = frame_count // 60
        sec = frame_count % 60
        time_string = f"{min:02d}:{sec:02d}"
        image_name = f"{output_file_prefix}{FRAME_PREFIX}{time_string}.jpg"
        output_filename = os.path.join(FRAME_EXTRACTION_DIRECTORY, image_name)
        cv2.imwrite(output_filename, frame)
        frame_count += 1
      count += 1
    vidcap.release()
    print(f"Completed video frame extraction!\n\nExtracted: {frame_count} frames")

# Constants
FRAME_EXTRACTION_DIRECTORY = "./pages/content/frames"
FRAME_PREFIX = "_frame"

st.title("YouTube Video Description & Improvement Assistant")

uploaded_file = st.file_uploader("Upload your video", type=['mp4'])

if uploaded_file is not None:

  st.write(f"**Uploaded video:** {uploaded_file.name}")

  # Extract frames from uploaded video
  extract_frame_from_video(uploaded_file)
  class File:
      def __init__(self, file_path: str, display_name: str = None):
        self.file_path = file_path
        if display_name:
          self.display_name = display_name
        self.timestamp = get_timestamp(file_path)
    
      def set_file_response(self, response):
        self.response = response

  def get_timestamp(filename):
    parts = filename.split(FRAME_PREFIX)
    if len(parts) != 2:
        return None  # Indicates the filename might be incorrectly formatted
    return parts[1].split('.')[0]

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
  
  # Make GenerateContent request with the structure described above.
  def make_request(prompt, files):
    request = [prompt]
    for file in files:
      request.append(file.timestamp)
      request.append(file.response)
    return request
  
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

